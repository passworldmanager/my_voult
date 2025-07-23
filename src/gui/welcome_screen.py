# PasswordGenerate/src/gui/welcome_screen.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

class WelcomeScreen(QWidget):
    """
    Tela de boas-vindas com opções para criar uma nova conta ou fazer login.
    """

    create_account_requested = pyqtSignal()
    login_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome_label = QLabel("Bem-vindo ao Gerenciador de Senhas!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(welcome_label)

        message_label = QLabel("Sua segurança em primeiro lugar.")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setStyleSheet("font-size: 16px; margin-bottom: 30px;")
        layout.addWidget(message_label)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        create_button = QPushButton("Criar Nova Conta")
        create_button.setFixedSize(150, 40)
        create_button.setStyleSheet("""
            QtPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        create_button.clicked.connect(self.create_account_requested.emit)
        btn_layout.addWidget(create_button)

        login_button = QPushButton("Fazer Login")
        login_button.setFixedSize(150, 40)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA; /* Azul */
                color: white;
                border-radius: 10px;
                font-size: 14px;
                padding: 8px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #007bb5;
            }
        """)
        login_button.clicked.connect(self.login_requested.emit)
        btn_layout.addWidget(login_button)


        layout.addLayout(btn_layout)
        self.setLayout(layout)
