APP_STYLESHEET = """
QMainWindow,
QWidget#root {
    background-color: #080A10;
    color: #F3F5FA;
}

QWidget {
    color: #F3F5FA;
    font-family: "Segoe UI";
    font-size: 14px;
}

QLabel#appTitle {
    color: #F3F5FA;
    font-size: 22px;
    font-weight: 600;
}

QFrame#displayCard,
QFrame#historyPanel {
    background-color: #111522;
    border: 1px solid #202638;
    border-radius: 18px;
}

QLabel#expressionDisplay {
    color: #969EB0;
    font-size: 16px;
}

QLabel#resultDisplay {
    color: #FFFFFF;
    font-size: 42px;
    font-weight: 600;
}

QLabel#sectionTitle {
    color: #F3F5FA;
    font-size: 18px;
    font-weight: 600;
}

QLabel#historyEmpty {
    color: #858DA0;
    font-size: 14px;
}

QPushButton {
    background-color: #151A28;
    border: 1px solid #252C3E;
    border-radius: 14px;
    color: #F3F5FA;
    font-size: 20px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #20283A;
    border-color: #39445E;
}

QPushButton:pressed {
    background-color: #29334A;
}

QPushButton[buttonRole="operator"] {
    background-color: #151D30;
    color: #69A8FF;
}

QPushButton[buttonRole="operator"]:hover {
    background-color: #1D2A43;
}

QPushButton[buttonRole="utility"] {
    background-color: #191E2C;
    color: #B5A4FF;
}

QPushButton[buttonRole="utility"]:hover {
    background-color: #25243B;
}

QPushButton[buttonRole="equals"] {
    background-color: #3478F6;
    border-color: #3478F6;
    color: #FFFFFF;
}

QPushButton[buttonRole="equals"]:hover {
    background-color: #5590FF;
    border-color: #5590FF;
}
"""
