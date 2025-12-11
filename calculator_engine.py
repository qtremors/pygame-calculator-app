"""
Safe calculator engine with expression parsing.
Replaces unsafe eval() with a tokenizer and parser approach.
"""
import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when dividing by zero."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised for invalid mathematical expressions."""
    pass


class TokenType(Enum):
    """Types of tokens in a mathematical expression."""
    NUMBER = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()


@dataclass
class Token:
    """Represents a single token in the expression."""
    type: TokenType
    value: str


@dataclass
class CalculatorState:
    """Encapsulates the calculator's current state."""
    expression: str = ""
    history: List[str] = field(default_factory=list)
    is_result_displayed: bool = False
    error_message: Optional[str] = None


class CalculatorEngine:
    """
    A safe calculator engine that parses and evaluates mathematical expressions.
    
    Supports: +, -, *, /, %, +/- (sign toggle), and floating-point numbers.
    """
    
    OPERATORS = {'+', '-', '*', '/', '%'}
    OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
    
    def __init__(self) -> None:
        self.state = CalculatorState()
    
    @property
    def expression(self) -> str:
        """Current expression string."""
        return self.state.expression
    
    @expression.setter
    def expression(self, value: str) -> None:
        self.state.expression = value
        self.state.error_message = None
    
    @property
    def display_text(self) -> str:
        """Text to show on the display."""
        if self.state.error_message:
            return self.state.error_message
        return self.state.expression or "0"
    
    @property
    def is_error(self) -> bool:
        """Whether the display shows an error."""
        return self.state.error_message is not None
    
    @property
    def history(self) -> List[str]:
        """Calculation history."""
        return self.state.history
    
    def clear(self) -> None:
        """Clear the current expression and any error state."""
        self.state.expression = ""
        self.state.error_message = None
        self.state.is_result_displayed = False
    
    def clear_history(self) -> None:
        """Clear the calculation history."""
        self.state.history.clear()
    
    def append(self, value: str) -> None:
        """Append a character to the current expression."""
        # If result is displayed and user types a number, start fresh
        if self.state.is_result_displayed:
            if value in "0123456789.":
                self.state.expression = ""
            self.state.is_result_displayed = False
        
        # Clear error on new input
        if self.state.error_message:
            self.state.expression = ""
            self.state.error_message = None
        
        # Don't start with an operator (except minus for negative)
        if not self.state.expression and value in "+*/%":
            return
        
        # Prevent consecutive operators (replace last)
        if self.state.expression and value in self.OPERATORS:
            if self.state.expression[-1] in self.OPERATORS:
                self.state.expression = self.state.expression[:-1]
        
        self.state.expression += value
    
    def backspace(self) -> None:
        """Remove the last character from the expression."""
        if self.state.is_result_displayed or self.state.error_message:
            self.clear()
        else:
            self.state.expression = self.state.expression[:-1]
    
    def toggle_sign(self) -> None:
        """Toggle the sign of the current expression/result."""
        if self.state.error_message:
            return
        
        if self.state.expression.startswith('-'):
            self.state.expression = self.state.expression[1:]
        elif self.state.expression:
            self.state.expression = '-' + self.state.expression
    
    def percentage(self) -> None:
        """Convert the current value to a percentage (divide by 100)."""
        if not self.state.expression or self.state.error_message:
            return
        
        try:
            value = float(self.state.expression)
            result = value / 100
            self.state.expression = self._format_result(result)
            self.state.is_result_displayed = True
        except ValueError:
            self.state.error_message = "Error: Invalid input"
            self.state.is_result_displayed = True
    
    def calculate(self) -> Optional[str]:
        """
        Evaluate the current expression and return the result.
        Returns None if expression is empty.
        """
        if not self.state.expression:
            return None
        
        if self.state.error_message:
            return None
        
        try:
            result = self._evaluate(self.state.expression)
            formatted = self._format_result(result)
            
            # Add to history
            history_entry = f"{self.state.expression} = {formatted}"
            self.state.history.append(history_entry)
            
            self.state.expression = formatted
            self.state.is_result_displayed = True
            
            return formatted
            
        except DivisionByZeroError:
            self.state.error_message = "Error: Division by zero"
            self.state.is_result_displayed = True
        except InvalidExpressionError:
            self.state.error_message = "Error: Invalid expression"
            self.state.is_result_displayed = True
        except Exception:
            self.state.error_message = "Error"
            self.state.is_result_displayed = True
        
        return None
    
    def _tokenize(self, expression: str) -> List[Token]:
        """Convert expression string into tokens."""
        tokens: List[Token] = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
            
            # Numbers (including decimals)
            if char.isdigit() or char == '.':
                num_str = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    float(num_str)
                    tokens.append(Token(TokenType.NUMBER, num_str))
                except ValueError:
                    raise InvalidExpressionError(f"Invalid number: {num_str}")
                continue
            
            # Operators
            if char in '+-*/%':
                tokens.append(Token(TokenType.OPERATOR, char))
                i += 1
                continue
            
            # Parentheses
            if char == '(':
                tokens.append(Token(TokenType.LPAREN, char))
                i += 1
                continue
            if char == ')':
                tokens.append(Token(TokenType.RPAREN, char))
                i += 1
                continue
            
            raise InvalidExpressionError(f"Invalid character: {char}")
        
        return tokens
    
    def _evaluate(self, expression: str) -> float:
        """
        Evaluate expression using the Shunting Yard algorithm.
        Handles operator precedence and unary minus correctly.
        """
        expression = expression.strip()
        tokens = self._tokenize(expression)
        
        if not tokens:
            raise InvalidExpressionError("Empty expression")
        
        # Handle unary minus by wrapping in parentheses: "5--3" -> "5-(0-3)"
        # - At the start of expression
        # - After an opening parenthesis
        # - After another operator
        processed: List[Token] = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == TokenType.OPERATOR and token.value == '-':
                # Check if this is a unary minus
                is_unary = (len(processed) == 0 or 
                           processed[-1].type == TokenType.OPERATOR or
                           processed[-1].type == TokenType.LPAREN)
                if is_unary:
                    # Wrap the unary expression: -(x) becomes (0-x)
                    # We need to grab the next token (the number) and wrap it
                    processed.append(Token(TokenType.LPAREN, "("))
                    processed.append(Token(TokenType.NUMBER, "0"))
                    processed.append(Token(TokenType.OPERATOR, "-"))
                    i += 1
                    if i < len(tokens):
                        processed.append(tokens[i])
                    processed.append(Token(TokenType.RPAREN, ")"))
                    i += 1
                    continue
            processed.append(token)
            i += 1
        
        tokens = processed
        
        # Shunting Yard: convert to postfix notation and evaluate
        output: List[float] = []
        operators: List[str] = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output.append(float(token.value))
            
            elif token.type == TokenType.OPERATOR:
                while (operators and 
                       operators[-1] != '(' and
                       self.OPERATOR_PRECEDENCE.get(operators[-1], 0) >= 
                       self.OPERATOR_PRECEDENCE.get(token.value, 0)):
                    self._apply_operator(operators.pop(), output)
                operators.append(token.value)
            
            elif token.type == TokenType.LPAREN:
                operators.append('(')
            
            elif token.type == TokenType.RPAREN:
                while operators and operators[-1] != '(':
                    self._apply_operator(operators.pop(), output)
                if operators:
                    operators.pop()  # Remove the '('
        
        # Apply remaining operators
        while operators:
            op = operators.pop()
            if op in '()':
                raise InvalidExpressionError("Mismatched parentheses")
            self._apply_operator(op, output)
        
        if len(output) != 1:
            raise InvalidExpressionError("Invalid expression")
        
        return output[0]
    
    def _apply_operator(self, op: str, stack: List[float]) -> None:
        """Apply an operator to the top values on the stack."""
        if len(stack) < 2:
            raise InvalidExpressionError("Not enough operands")
        
        b = stack.pop()
        a = stack.pop()
        
        if op == '+':
            stack.append(a + b)
        elif op == '-':
            stack.append(a - b)
        elif op == '*':
            stack.append(a * b)
        elif op == '/':
            if b == 0:
                raise DivisionByZeroError()
            stack.append(a / b)
        elif op == '%':
            if b == 0:
                raise DivisionByZeroError()
            stack.append(a % b)
    
    def _format_result(self, value: float) -> str:
        """Format the result, removing unnecessary decimal places."""
        if value == int(value):
            return str(int(value))
        # Limit to 10 decimal places to avoid floating point noise
        formatted = f"{value:.10f}".rstrip('0').rstrip('.')
        return formatted
