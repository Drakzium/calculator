import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from ui.buttons import CalculatorButton
from ui.main_window import MainWindow


class CalculatorButtonInteractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.window = MainWindow()
        self.window.show()
        self.app.processEvents()

    def tearDown(self) -> None:
        self.window.close()

    def click(self, label: str) -> None:
        button = next(
            button
            for button in self.window.findChildren(CalculatorButton)
            if button.text() == label
        )
        button.click()
        self.app.processEvents()

    def test_digits_operators_and_equals(self) -> None:
        for key in ("1", "+", "2", "="):
            self.click(key)

        self.assertEqual(self.window.result_display.text(), "3")
        self.assertEqual(self.window.expression_display.text(), "1 + 2 =")

    def test_decimal_calculation(self) -> None:
        for key in ("0", ".", "1", "+", "0", ".", "2", "="):
            self.click(key)

        self.assertEqual(self.window.result_display.text(), "0.3")

    def test_percentage_button_scales_the_current_entry(self) -> None:
        for key in ("2", "5", "%"):
            self.click(key)

        self.assertEqual(self.window.result_display.text(), "0.25")

    def test_unary_negative_input(self) -> None:
        for key in ("−", "5", "+", "2", "="):
            self.click(key)

        self.assertEqual(self.window.result_display.text(), "-3")

    def test_clear_and_backspace(self) -> None:
        for key in ("1", "2", "⌫"):
            self.click(key)
        self.assertEqual(self.window.result_display.text(), "1")

        self.click("C")
        self.assertEqual(self.window.result_display.text(), "0")
        self.assertEqual(self.window.expression_display.text(), "")

    def test_result_can_be_used_in_the_next_calculation(self) -> None:
        for key in ("3", "+", "2", "=", "+", "4", "="):
            self.click(key)

        self.assertEqual(self.window.result_display.text(), "9")

    def test_division_by_zero_is_shown_without_crashing(self) -> None:
        for key in ("4", "÷", "0", "="):
            self.click(key)

        self.assertEqual(self.window.result_display.text(), "Error")
        self.assertEqual(self.window.expression_display.text(), "Cannot divide by zero.")


if __name__ == "__main__":
    unittest.main()
