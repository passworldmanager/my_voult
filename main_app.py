import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt

from src.database.repositories.repository import PasswordRepository
from src.database.repositories.repository_config import ConfigRepository
from src.database.services.security_service import SecurityService

from src.gui.welcome_screen import WelcomeScreen
from src.gui.create_login_screen import CreateLoginScreen
from src.gui.login_screen import LoginScreen
from src.gui.options_screen import OptionsScreen

class MainWindow(QMainWindow):
    """
    Janela principal da aplicação que gerencia a navegação entre as diferentes telas.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Senhas")
        self.setGeometry(100, 100, 500, 400)
        self.password_repo = PasswordRepository()
        self.config_repo = ConfigRepository()

        # Instanciar a camada de serviço, injetando os repositórios
        self.security_service = SecurityService(
            password_repository=self.password_repo,
            config_repository=self.config_repo
        )

        # ... O resto do arquivo permanece exatamente o mesmo ...
        # QStackedWidget para gerenciar as diferentes telas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Criar instâncias das telas e adicioná-las ao QStackedWidget
        self.welcome_screen = WelcomeScreen()
        self.create_login_screen = CreateLoginScreen(self.security_service)
        self.login_screen = LoginScreen(self.security_service)
        self.options_screen = OptionsScreen(self.security_service)

        self.stacked_widget.addWidget(self.welcome_screen)
        self.stacked_widget.addWidget(self.create_login_screen)
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.options_screen)

        # Conectar sinais de navegação das telas
        self.welcome_screen.create_account_requested.connect(self.show_create_login_screen)
        self.welcome_screen.login_requested.connect(self.show_login_screen)
        self.create_login_screen.login_success.connect(self.show_options_screen)
        self.create_login_screen.back_to_welcome.connect(self.show_welcome_screen)
        self.login_screen.login_success.connect(self.show_options_screen)
        self.login_screen.back_to_welcome.connect(self.show_welcome_screen)
        self.options_screen.logout_requested.connect(self.show_welcome_screen)

        # Determinar qual tela mostrar inicialmente
        if self.security_service.is_master_password_set():
            self.show_login_screen()
        else:
            self.show_welcome_screen()

    def show_welcome_screen(self):
        self.stacked_widget.setCurrentWidget(self.welcome_screen)

    def show_create_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.create_login_screen)
        self.create_login_screen.clear_fields()

    def show_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)
        self.login_screen.clear_fields()

    def show_options_screen(self):
        self.stacked_widget.setCurrentWidget(self.options_screen)
        QMessageBox.information(self, "Login Bem-Sucedido", "Você está logado!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())