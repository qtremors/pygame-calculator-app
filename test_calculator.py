"""
Comprehensive tests for the CalculatorEngine.
Tests basic operations, edge cases, and error handling.
"""
import pytest
from calculator_engine import (
    CalculatorEngine, 
    DivisionByZeroError, 
    InvalidExpressionError
)


class TestBasicOperations:
    """Tests for basic arithmetic operations."""
    
    def setup_method(self):
        """Create a fresh engine for each test."""
        self.engine = CalculatorEngine()
    
    def test_addition(self):
        """Test basic addition."""
        self.engine.expression = "2+3"
        result = self.engine.calculate()
        assert result == "5"
    
    def test_subtraction(self):
        """Test basic subtraction."""
        self.engine.expression = "10-4"
        result = self.engine.calculate()
        assert result == "6"
    
    def test_multiplication(self):
        """Test basic multiplication."""
        self.engine.expression = "7*8"
        result = self.engine.calculate()
        assert result == "56"
    
    def test_division(self):
        """Test basic division."""
        self.engine.expression = "20/4"
        result = self.engine.calculate()
        assert result == "5"
    
    def test_decimal_division(self):
        """Test division with decimal result."""
        self.engine.expression = "10/4"
        result = self.engine.calculate()
        assert result == "2.5"
    
    def test_modulo(self):
        """Test modulo operation."""
        self.engine.expression = "17%5"
        result = self.engine.calculate()
        assert result == "2"


class TestOperatorPrecedence:
    """Tests for correct operator precedence."""
    
    def setup_method(self):
        self.engine = CalculatorEngine()
    
    def test_multiply_before_add(self):
        """Multiplication before addition."""
        self.engine.expression = "2+3*4"
        result = self.engine.calculate()
        assert result == "14"  # Not 20
    
    def test_divide_before_subtract(self):
        """Division before subtraction."""
        self.engine.expression = "10-6/2"
        result = self.engine.calculate()
        assert result == "7"  # Not 2
    
    def test_complex_precedence(self):
        """Complex expression with multiple operators."""
        self.engine.expression = "2+3*4-10/2"
        result = self.engine.calculate()
        assert result == "9"  # 2+12-5 = 9
    
    def test_left_to_right_same_precedence(self):
        """Same precedence operators: left to right."""
        self.engine.expression = "20-5-3"
        result = self.engine.calculate()
        assert result == "12"  # (20-5)-3, not 20-(5-3)


class TestNegativeNumbers:
    """Tests for negative number handling."""
    
    def setup_method(self):
        self.engine = CalculatorEngine()
    
    def test_negative_start(self):
        """Expression starting with negative number."""
        self.engine.expression = "-5+3"
        result = self.engine.calculate()
        assert result == "-2"
    
    def test_negative_result(self):
        """Calculation resulting in negative."""
        self.engine.expression = "3-10"
        result = self.engine.calculate()
        assert result == "-7"
    
    def test_multiply_negative(self):
        """Multiplying by negative number."""
        self.engine.expression = "5*-3"
        result = self.engine.calculate()
        assert result == "-15"
    
    def test_double_negative(self):
        """Subtracting a negative (should add)."""
        self.engine.expression = "5--3"
        result = self.engine.calculate()
        assert result == "8"


class TestDecimalNumbers:
    """Tests for decimal number handling."""
    
    def setup_method(self):
        self.engine = CalculatorEngine()
    
    def test_decimal_input(self):
        """Decimal numbers in input."""
        self.engine.expression = "1.5+2.5"
        result = self.engine.calculate()
        assert result == "4"
    
    def test_decimal_result(self):
        """Result is decimal."""
        self.engine.expression = "1/3"
        result = self.engine.calculate()
        # Should be truncated to reasonable precision
        assert result.startswith("0.333")
    
    def test_small_decimals(self):
        """Very small decimal numbers."""
        self.engine.expression = "0.001+0.002"
        result = self.engine.calculate()
        assert result == "0.003"


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def setup_method(self):
        self.engine = CalculatorEngine()
    
    def test_zero_operations(self):
        """Operations with zero."""
        self.engine.expression = "0+5"
        assert self.engine.calculate() == "5"
        
        self.engine.clear()
        self.engine.expression = "5*0"
        assert self.engine.calculate() == "0"
    
    def test_large_numbers(self):
        """Very large numbers."""
        self.engine.expression = "999999999+1"
        result = self.engine.calculate()
        assert result == "1000000000"
    
    def test_empty_expression(self):
        """Empty expression returns None."""
        self.engine.expression = ""
        result = self.engine.calculate()
        assert result is None
    
    def test_single_number(self):
        """Single number without operator."""
        self.engine.expression = "42"
        result = self.engine.calculate()
        assert result == "42"


class TestErrorHandling:
    """Tests for error handling."""
    
    def setup_method(self):
        self.engine = CalculatorEngine()
    
    def test_division_by_zero(self):
        """Division by zero shows error."""
        self.engine.expression = "5/0"
        self.engine.calculate()
        assert self.engine.is_error
        assert "zero" in self.engine.display_text.lower()
    
    def test_modulo_by_zero(self):
        """Modulo by zero shows error."""
        self.engine.expression = "5%0"
        self.engine.calculate()
        assert self.engine.is_error
    
    def test_invalid_expression_consecutive_operators(self):
        """Multiple consecutive operators should be handled."""
        # The engine should allow replacing operators
        self.engine.append("5")
        self.engine.append("+")
        self.engine.append("*")  # Should replace +
        self.engine.append("3")
        result = self.engine.calculate()
        assert result == "15"  # 5*3


class TestStateManagement:
    """Tests for calculator state management."""
    
    def setup_method(self):
        self.engine = CalculatorEngine()
    
    def test_clear(self):
        """Clear resets expression."""
        self.engine.expression = "123"
        self.engine.clear()
        assert self.engine.expression == ""
        assert self.engine.display_text == "0"
    
    def test_backspace(self):
        """Backspace removes last character."""
        self.engine.expression = "123"
        self.engine.backspace()
        assert self.engine.expression == "12"
    
    def test_backspace_empty(self):
        """Backspace on empty is safe."""
        self.engine.expression = ""
        self.engine.backspace()  # Should not raise
        assert self.engine.expression == ""
    
    def test_toggle_sign(self):
        """Toggle sign adds/removes minus."""
        self.engine.expression = "5"
        self.engine.toggle_sign()
        assert self.engine.expression == "-5"
        self.engine.toggle_sign()
        assert self.engine.expression == "5"
    
    def test_percentage(self):
        """Percentage divides by 100."""
        self.engine.expression = "50"
        self.engine.percentage()
        assert self.engine.expression == "0.5"
    
    def test_history(self):
        """History stores calculations."""
        self.engine.expression = "2+2"
        self.engine.calculate()
        assert len(self.engine.history) == 1
        assert "2+2 = 4" in self.engine.history[0]
    
    def test_clear_history(self):
        """Clear history empties list."""
        self.engine.expression = "1+1"
        self.engine.calculate()
        self.engine.clear_history()
        assert len(self.engine.history) == 0


class TestInputBehavior:
    """Tests for input handling behavior."""
    
    def setup_method(self):
        self.engine = CalculatorEngine()
    
    def test_cant_start_with_operator(self):
        """Cannot start expression with operator (except minus)."""
        self.engine.append("+")
        assert self.engine.expression == ""
        
        self.engine.append("*")
        assert self.engine.expression == ""
    
    def test_result_then_number_clears(self):
        """Typing number after result starts fresh."""
        self.engine.expression = "5+5"
        self.engine.calculate()
        assert self.engine.expression == "10"
        
        self.engine.append("3")
        assert self.engine.expression == "3"
    
    def test_result_then_operator_continues(self):
        """Typing operator after result continues calculation."""
        self.engine.expression = "5+5"
        self.engine.calculate()
        assert self.engine.expression == "10"
        
        self.engine.append("+")
        self.engine.append("5")
        result = self.engine.calculate()
        assert result == "15"
