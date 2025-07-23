# PasswordGenerate/src/gui/login_screen.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

class LoginScreen(QWidget):
    """
    Tela para o usuário fazer login com sua senha mestra.
    """
    login_success = pyqtSignal() # Sinal emitido ao fazer login com sucesso
    back_to_welcome = pyqtSignal() # Sinal para voltar à tela de boas-vindas

    def __init__(self, security_service):
        super().__init__()
        self.security_service = security_service # Injeção de dependência do serviço de segurança
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Faça Login")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha mestra")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password) # Esconde o texto
        self.password_input.setFixedSize(250, 30)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_button = QPushButton("Entrar")
        login_button.setFixedSize(120, 35)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #007bb5;
            }
        """)
        login_button.clicked.connect(self.perform_login)
        btn_layout.addWidget(login_button)

        back_button = QPushButton("Voltar")
        back_button.setFixedSize(120, 35)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 8px;
                font-size: 13px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        back_button.clicked.connect(self.back_to_welcome.emit)
        btn_layout.addWidget(back_button)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def clear_fields(self):
        """Limpa o campo de entrada de senha."""
        self.password_input.clear()

    def perform_login(self):
        password = self.password_input.text()

        if not password:
            QMessageBox.warning(self, "Erro", "Por favor, digite sua senha mestra.")
            return

        # Tenta fazer login usando o SecurityService
        # O SecurityService agora gerencia a leitura do salt da senha mestra do DB
        if self.security_service.login_with_master_password(password):
            self.clear_fields()
            self.login_success.emit() # Emite sinal para navegar para a tela de opções
        else:
            QMessageBox.critical(self, "Erro de Login", "Senha mestra incorreta. Tente novamente.")

