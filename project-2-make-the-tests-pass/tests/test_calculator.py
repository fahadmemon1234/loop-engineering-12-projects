"""
Test suite for calculator module.

This is the "checker" in the maker-checker pattern.
These tests define the correct behavior and determine whether
the implementation is acceptable.
"""

import pytest
import sys
import os

# Add parent directory to path so we can import calculator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator import add, subtract, multiply, divide


class TestAdd:
    """Tests for the add function."""

    def test_add_positive_numbers(self):
        """2 + 3 should equal 5"""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        """-1 + -1 should equal -2"""
        assert add(-1, -1) == -2

    def test_add_zero(self):
        """5 + 0 should equal 5"""
        assert add(5, 0) == 5


class TestSubtract:
    """Tests for the subtract function."""

    def test_subtract_positive_numbers(self):
        """10 - 4 should equal 6"""
        assert subtract(10, 4) == 6

    def test_subtract_resulting_in_zero(self):
        """7 - 7 should equal 0"""
        assert subtract(7, 7) == 0

    def test_subtract_negative_result(self):
        """3 - 8 should equal -5"""
        assert subtract(3, 8) == -5


class TestMultiply:
    """Tests for the multiply function."""

    def test_multiply_positive_numbers(self):
        """3 * 4 should equal 12"""
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        """5 * 0 should equal 0"""
        assert multiply(5, 0) == 0

    def test_multiply_by_one(self):
        """7 * 1 should equal 7"""
        assert multiply(7, 1) == 7


class TestDivide:
    """Tests for the divide function."""

    def test_divide_positive_numbers(self):
        """10 / 2 should equal 5"""
        assert divide(10, 2) == 5

    def test_divide_resulting_in_float(self):
        """7 / 2 should equal 3.5"""
        assert divide(7, 2) == 3.5

    def test_divide_by_one(self):
        """9 / 1 should equal 9"""
        assert divide(9, 1) == 9

    def test_divide_by_zero(self):
        """Division by zero should raise ValueError"""
        with pytest.raises(ValueError):
            divide(10, 0)
