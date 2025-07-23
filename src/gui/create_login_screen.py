# PasswordGenerate/src/gui/create_login_screen.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

class CreateLoginScreen(QWidget):
    """
    Tela para o usuário criar sua senha mestra.
    """
    login_success = pyqtSignal() # Sinal emitido ao criar a conta com sucesso
    back_to_welcome = pyqtSignal() # Sinal para voltar à tela de boas-vindas

    def __init__(self, security_service):
        super().__init__()
        self.security_service = security_service # Injeção de dependência do serviço de segurança
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Crie sua Senha Mestra")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua nova senha mestra")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password) # Esconde o texto
        self.password_input.setFixedSize(250, 30)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirme sua senha mestra")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password) # Esconde o texto
        self.confirm_password_input.setFixedSize(250, 30)
        layout.addWidget(self.confirm_password_input, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        create_button = QPushButton("Criar Login")
        create_button.setFixedSize(120, 35)
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        create_button.clicked.connect(self.create_login)
        btn_layout.addWidget(create_button)

        back_button = QPushButton("Voltar")
        back_button.setFixedSize(120, 35)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336; /* Vermelho */
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
        """Limpa os campos de entrada de senha."""
        self.password_input.clear()
        self.confirm_password_input.clear()

    def create_login(self):
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not password or not confirm_password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem. Tente novamente.")
            return

        # Tenta registrar a senha mestra
        if self.security_service.register_master_password(password):
            # Se o registro for bem-sucedido, TENTA FAZER O LOGIN AUTOMATICAMENTE
            if self.security_service.login_with_master_password(password): # <--- ADICIONE ESTA LINHA
                QMessageBox.information(self, "Sucesso", "Sua conta foi criada e você está logado!")
                self.clear_fields()
                self.login_success.emit() # Emite sinal para navegar para a tela de opções
            else:
                # Isso só deve acontecer se houver um erro inesperado no login logo após o registro
                QMessageBox.critical(self, "Erro Crítico", "Conta criada, mas falha no login automático. Tente fazer login manualmente.")
                self.clear_fields()
                self.back_to_welcome.emit() # Volta para a tela de boas-vindas
        else:
            QMessageBox.critical(self, "Erro", "Não foi possível criar a conta. A senha mestra pode já estar definida.")