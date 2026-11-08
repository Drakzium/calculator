from functools import partial
from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from core.calculator import (
    CalculatorError,
    evaluate_expression,
    percentage,
)
from ui.buttons import BUTTON_ROWS, CalculatorButton


_OPERATOR_SYMBOLS = {
    "÷": "/",
    "×": "*",
    "−": "-",
    "+": "+",
}


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self._expression = ""
        self._current_entry = ""
        self._just_calculated = False
        self._has_error = False

        self.setWindowTitle("NO ONE Calculator")
        self.resize(980, 680)
        self.setMinimumSize(780, 560)

        root = QWidget()
        root.setObjectName("root")
        page_layout = QHBoxLayout(root)
        page_layout.setContentsMargins(24, 22, 24, 22)
        page_layout.setSpacing(18)

        calculator_panel = self._create_calculator_panel()
        history_panel = self._create_history_panel()
        page_layout.addWidget(calculator_panel, 3)
        page_layout.addWidget(history_panel, 1)

        self.setCentralWidget(root)

    def _create_calculator_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        title = QLabel("NO ONE Calculator")
        title.setObjectName("appTitle")
        layout.addWidget(title)

        display_card = QFrame()
        display_card.setObjectName("displayCard")
        display_layout = QVBoxLayout(display_card)
        display_layout.setContentsMargins(18, 14, 18, 14)
        display_layout.setSpacing(8)

        self.expression_display = QLabel("")
        self.expression_display.setObjectName("expressionDisplay")
        self.expression_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        display_layout.addWidget(self.expression_display)

        self.result_display = QLabel("0")
        self.result_display.setObjectName("resultDisplay")
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        display_layout.addWidget(self.result_display)
        layout.addWidget(display_card)

        keypad = QGridLayout()
        keypad.setSpacing(10)
        for row_index, row in enumerate(BUTTON_ROWS):
            column_index = 0
            for label in row:
                column_span = (
                    2 if row_index == len(BUTTON_ROWS) - 1 and label == "0" else 1
                )
                button = CalculatorButton(label)
                button.pressed.connect(partial(self._handle_button, label))
                keypad.addWidget(
                    button,
                    row_index,
                    column_index,
                    1,
                    column_span,
                )
                column_index += column_span
        for column_index in range(4):
            keypad.setColumnStretch(column_index, 1)
        layout.addLayout(keypad, 1)

        return panel

    def _handle_button(self, key: str) -> None:
        if key == "C":
            self._clear()
        elif key == "⌫":
            self._backspace()
        elif key == "%":
            self._apply_percentage()
        elif key == "=":
            self._calculate()
        elif key in _OPERATOR_SYMBOLS:
            self._append_operator(key)
        elif key.isdigit():
            self._append_digit(key)
        elif key == ".":
            self._append_decimal()

    def _append_digit(self, digit: str) -> None:
        if self._has_error or self._just_calculated:
            self._start_new_calculation()

        if self._current_entry in ("0", "-0"):
            self._expression = self._expression[:-1] + digit
            self._current_entry = self._current_entry[:-1] + digit
        else:
            self._expression += digit
            self._current_entry += digit
        self._update_display()

    def _append_decimal(self) -> None:
        if self._has_error or self._just_calculated:
            self._start_new_calculation()
        if "." in self._current_entry:
            return

        if self._current_entry in ("", "-"):
            self._expression += "0."
            self._current_entry += "0."
        else:
            self._expression += "."
            self._current_entry += "."
        self._update_display()

    def _append_operator(self, symbol: str) -> None:
        if self._has_error:
            self._start_new_calculation()
        if self._just_calculated:
            self._just_calculated = False

        operation = _OPERATOR_SYMBOLS[symbol]
        if not self._expression:
            if operation == "-":
                self._expression = "-"
                self._current_entry = "-"
                self._update_display()
            return

        if self._current_entry == "-":
            if len(self._expression) > 1 and self._expression[-2] in "+-*/":
                self._expression = self._expression[:-2] + operation
                self._current_entry = ""
        elif not self._current_entry and self._expression[-1] in "+-*/":
            if operation == "-":
                self._expression += operation
                self._current_entry = "-"
            else:
                self._expression = self._expression[:-1] + operation
        else:
            self._expression += operation
            self._current_entry = ""
        self._update_display()

    def _apply_percentage(self) -> None:
        if self._has_error:
            self._start_new_calculation()
            return
        if self._just_calculated:
            self._just_calculated = False
        if not self._current_entry or self._current_entry == "-":
            return

        try:
            result = percentage(self._current_entry)
        except CalculatorError as error:
            self._show_calculation_error(error)
            return

        prefix = self._expression[: -len(self._current_entry)]
        self._current_entry = self._format_decimal(result)
        self._expression = prefix + self._current_entry
        self._update_display()

    def _calculate(self) -> None:
        if not self._expression or self._has_error:
            return
        try:
            result = evaluate_expression(self._expression)
        except CalculatorError as error:
            self._show_calculation_error(error)
            return

        displayed_expression = self._format_expression(self._expression)
        result_text = self._format_decimal(result)
        self.expression_display.setText(f"{displayed_expression} =")
        self.result_display.setText(result_text)
        self._expression = result_text
        self._current_entry = result_text
        self._just_calculated = True

    def _backspace(self) -> None:
        self._has_error = False
        self._just_calculated = False
        if not self._expression:
            return

        if self._current_entry:
            self._expression = self._expression[:-1]
            self._current_entry = self._current_entry[:-1]
        else:
            self._expression = self._expression[:-1]
            self._current_entry = self._last_entry(self._expression)
        self._update_display()

    def _clear(self) -> None:
        self._expression = ""
        self._current_entry = ""
        self._just_calculated = False
        self._has_error = False
        self._update_display()

    def _start_new_calculation(self) -> None:
        self._expression = ""
        self._current_entry = ""
        self._just_calculated = False
        self._has_error = False
        self._update_display()

    def _show_calculation_error(self, error: CalculatorError) -> None:
        self._has_error = True
        self.expression_display.setText(str(error))
        self.result_display.setText("Error")

    def _update_display(self) -> None:
        self.expression_display.setText(self._format_expression(self._expression))
        if self._current_entry:
            self.result_display.setText(self._current_entry)
        elif not self._expression:
            self.result_display.setText("0")

    @staticmethod
    def _format_expression(expression: str) -> str:
        symbols = {"+": "+", "-": "−", "*": "×", "/": "÷"}
        formatted: list[str] = []
        for index, character in enumerate(expression):
            if character not in symbols:
                formatted.append(character)
                continue

            is_unary = character in "+-" and (
                index == 0 or expression[index - 1] in "+-*/eE"
            )
            symbol = symbols[character]
            formatted.append(symbol if is_unary else f" {symbol} ")
        return "".join(formatted)

    @staticmethod
    def _format_decimal(value: Decimal) -> str:
        if value == 0:
            return "0"
        return str(value.normalize())

    @staticmethod
    def _last_entry(expression: str) -> str:
        index = len(expression) - 1
        while index >= 0:
            character = expression[index]
            if character.isdigit() or character == ".":
                index -= 1
                continue
            if character in "eE":
                index -= 1
                if index >= 0 and expression[index] in "+-":
                    index -= 1
                continue
            if character in "+-" and index > 0 and expression[index - 1] in "eE":
                index -= 1
                continue
            if character in "+-" and (
                index == 0 or expression[index - 1] in "+-*/"
            ):
                index -= 1
                continue
            break
        return expression[index + 1 :]

    def _create_history_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("historyPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        heading = QLabel("History")
        heading.setObjectName("sectionTitle")
        layout.addWidget(heading)

        empty_message = QLabel("Your calculations will appear here.")
        empty_message.setObjectName("historyEmpty")
        empty_message.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        empty_message.setWordWrap(True)
        layout.addWidget(empty_message, 1)

        return panel
