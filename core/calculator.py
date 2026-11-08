import ast
import operator
from collections.abc import Callable
from decimal import Decimal, DecimalException, InvalidOperation


class CalculatorError(ValueError):
    """Base error for invalid or unrepresentable calculations."""


class InvalidExpressionError(CalculatorError):
    """Raised when an expression contains unsupported or invalid input."""


class DivisionByZeroError(CalculatorError):
    """Raised when an expression attempts to divide by zero."""


_BINARY_OPERATORS: dict[
    type[ast.operator], Callable[[Decimal, Decimal], Decimal]
] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_MAX_EXPRESSION_LENGTH = 256
_MAX_EXPRESSION_NODES = 100


def evaluate_expression(expression: str) -> Decimal:
    """Evaluate numeric literals and the +, -, *, and / operators safely."""
    if not isinstance(expression, str) or not expression.strip():
        raise InvalidExpressionError("Enter a calculation first.")
    if len(expression) > _MAX_EXPRESSION_LENGTH:
        raise InvalidExpressionError("The calculation is too long.")

    try:
        syntax_tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError) as error:
        raise InvalidExpressionError("Enter a valid arithmetic expression.") from error

    if sum(1 for _ in ast.walk(syntax_tree)) > _MAX_EXPRESSION_NODES:
        raise InvalidExpressionError("The calculation is too complex.")

    return _evaluate_node(syntax_tree.body, expression)


def percentage(value: Decimal | int | float | str) -> Decimal:
    """Return one percent-scaled value (for example, 25 becomes 0.25)."""
    number = _to_decimal(value)
    try:
        return number / Decimal("100")
    except DecimalException as error:
        raise CalculatorError("The percentage is outside the supported range.") from error


def _evaluate_node(node: ast.AST, expression: str) -> Decimal:
    if isinstance(node, ast.Constant):
        if type(node.value) not in (int, float):
            raise InvalidExpressionError("Only numeric values are allowed.")

        literal = ast.get_source_segment(expression, node)
        if literal is None:
            raise InvalidExpressionError("The numeric value could not be read.")
        try:
            number = Decimal(literal)
        except InvalidOperation as error:
            raise InvalidExpressionError("Enter a valid numeric value.") from error
        if not number.is_finite():
            raise InvalidExpressionError("The numeric value must be finite.")
        return number

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        operand = _evaluate_node(node.operand, expression)
        return operand if isinstance(node.op, ast.UAdd) else -operand

    if isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise InvalidExpressionError("Only +, -, *, and / are supported.")

        left = _evaluate_node(node.left, expression)
        right = _evaluate_node(node.right, expression)
        if isinstance(node.op, ast.Div) and right == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        try:
            return operation(left, right)
        except DecimalException as error:
            raise CalculatorError("The result is outside the supported range.") from error

    raise InvalidExpressionError("Only basic arithmetic expressions are allowed.")


def _to_decimal(value: Decimal | int | float | str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (Decimal, int, float, str)):
        raise InvalidExpressionError("Enter a numeric value.")
    try:
        number = Decimal(str(value))
    except InvalidOperation as error:
        raise InvalidExpressionError("Enter a valid numeric value.") from error
    if not number.is_finite():
        raise InvalidExpressionError("The numeric value must be finite.")
    return number
