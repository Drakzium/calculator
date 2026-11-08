import unittest
from decimal import Decimal

from core.calculator import (
    DivisionByZeroError,
    InvalidExpressionError,
    evaluate_expression,
    percentage,
)


class EvaluateExpressionTests(unittest.TestCase):
    def test_operator_precedence_and_parentheses(self) -> None:
        self.assertEqual(evaluate_expression("2 + 3 * 4"), Decimal("14"))
        self.assertEqual(evaluate_expression("(2 + 3) * 4"), Decimal("20"))

    def test_decimal_arithmetic_is_exact(self) -> None:
        self.assertEqual(evaluate_expression("0.1 + 0.2"), Decimal("0.3"))

    def test_subtraction_division_and_unary_signs(self) -> None:
        self.assertEqual(evaluate_expression("9 - 12"), Decimal("-3"))
        self.assertEqual(evaluate_expression("-6 / +2"), Decimal("-3"))

    def test_division_by_zero_raises_a_specific_error(self) -> None:
        with self.assertRaises(DivisionByZeroError):
            evaluate_expression("1 / 0")

    def test_unsupported_or_invalid_input_is_rejected(self) -> None:
        invalid_expressions = (
            "",
            "1 +",
            "2 ** 8",
            "1 + '2'",
            "__import__('os')",
        )
        for expression in invalid_expressions:
            with self.subTest(expression=expression):
                with self.assertRaises(InvalidExpressionError):
                    evaluate_expression(expression)

    def test_expression_size_is_limited(self) -> None:
        with self.assertRaises(InvalidExpressionError):
            evaluate_expression("1" * 257)


class PercentageTests(unittest.TestCase):
    def test_percentage_scales_value_by_one_hundred(self) -> None:
        self.assertEqual(percentage("25"), Decimal("0.25"))
        self.assertEqual(percentage(Decimal("12.5")), Decimal("0.125"))


if __name__ == "__main__":
    unittest.main()
