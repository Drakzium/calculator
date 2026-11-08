from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


BUTTON_ROWS = (
    ("C", "⌫", "%", "÷"),
    ("7", "8", "9", "×"),
    ("4", "5", "6", "−"),
    ("1", "2", "3", "+"),
    ("0", ".", "="),
)


class CalculatorButton(QPushButton):
    def __init__(self, label: str) -> None:
        super().__init__(label)

        if label in ("÷", "×", "−", "+"):
            role = "operator"
        elif label == "=":
            role = "equals"
        elif label in ("C", "⌫", "%"):
            role = "utility"
        else:
            role = "number"

        self.setProperty("buttonRole", role)
        self.setMinimumHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if label == "⌫":
            self.setAccessibleName("Backspace")
