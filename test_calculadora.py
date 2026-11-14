import unittest
from decimal import Decimal

from calculadora import (
    MAX_DISPLAY_LENGTH,
    Calculator,
    calculate,
    format_number,
    parse_number,
)


class CalculatorTests(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(calculate(Decimal("8"), "+", Decimal("3")), Decimal("11"))
        self.assertEqual(calculate(Decimal("8"), "-", Decimal("3")), Decimal("5"))
        self.assertEqual(calculate(Decimal("8"), "*", Decimal("3")), Decimal("24"))
        self.assertEqual(calculate(Decimal("8"), "/", Decimal("4")), Decimal("2"))

    def test_decimal_operation(self):
        calculator = Calculator()
        for digit in "1.5":
            if digit == ".":
                calculator.input_decimal()
            else:
                calculator.input_digit(digit)
        calculator.set_operator("*")
        calculator.input_digit("2")
        self.assertEqual(calculator.calculate(), "3")
        self.assertEqual(calculator.history[0], "1.5 * 2 = 3")

    def test_chained_operations_are_sequential(self):
        calculator = Calculator()
        calculator.input_digit("2")
        calculator.set_operator("+")
        calculator.input_digit("3")
        calculator.set_operator("*")
        calculator.input_digit("4")
        self.assertEqual(calculator.calculate(), "20")

    def test_division_by_zero_is_reported_without_losing_state(self):
        calculator = Calculator()
        calculator.input_digit("9")
        calculator.set_operator("/")
        calculator.input_digit("0")
        with self.assertRaisesRegex(ZeroDivisionError, "dividir por zero"):
            calculator.calculate()
        self.assertEqual(calculator.display, "0")
        self.assertEqual(calculator.history, [])

    def test_invalid_input_and_operator_are_rejected(self):
        with self.assertRaises(ValueError):
            parse_number("abc")
        with self.assertRaises(ValueError):
            parse_number("NaN")
        with self.assertRaises(ValueError):
            calculate(Decimal("1"), "%", Decimal("2"))
        calculator = Calculator()
        with self.assertRaises(ValueError):
            calculator.input_digit("12")

    def test_consecutive_operators_are_rejected_without_changing_operation(self):
        calculator = Calculator()
        calculator.input_digit("8")
        calculator.set_operator("+")
        with self.assertRaisesRegex(ValueError, "operadores consecutivos"):
            calculator.set_operator("*")
        calculator.input_digit("2")
        self.assertEqual(calculator.calculate(), "10")

    def test_display_input_and_results_are_limited_to_sixteen_characters(self):
        calculator = Calculator()
        for digit in "12345678901234567890":
            calculator.input_digit(digit)
        self.assertEqual(len(calculator.display), MAX_DISPLAY_LENGTH)
        self.assertEqual(
            len(format_number(Decimal("12345678901234567890"))),
            MAX_DISPLAY_LENGTH,
        )

    def test_backspace_and_clear_also_clear_history(self):
        calculator = Calculator()
        calculator.input_digit("1")
        calculator.input_digit("2")
        calculator.backspace()
        self.assertEqual(calculator.display, "1")
        calculator.set_operator("+")
        calculator.input_digit("1")
        calculator.calculate()
        self.assertTrue(calculator.history)
        calculator.clear()
        self.assertEqual(calculator.display, "0")
        self.assertEqual(calculator.history, [])

    def test_history_keeps_at_least_five_recent_calculations(self):
        calculator = Calculator()
        for digit in "12345678901":
            calculator.input_digit(digit)
            calculator.set_operator("+")
            calculator.input_digit("1")
            calculator.calculate()
        self.assertEqual(len(calculator.history), 10)
        self.assertTrue(calculator.history[0].endswith("= 2"))


if __name__ == "__main__":
    unittest.main()
