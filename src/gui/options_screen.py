# src/gui/options_screen.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QInputDialog, QLineEdit, QHBoxLayout, QFormLayout, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial

from src.password_generate.password_generator import password_generator

class OptionsScreen(QWidget):
    """
    Tela principal de opções, com widgets integrados para gerar, cadastrar,
    consultar, listar e deletar senhas, priorizando a acessibilidade.
    """
    logout_requested = pyqtSignal()

    def __init__(self, security_service):
        super().__init__()
        self.security_service = security_service
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        # Centraliza a criação de todos os sub-widgets
        self._create_all_widgets()

        # Adicionar todos os widgets ao layout principal
        self.main_layout.addWidget(self.options_widget)
        self.main_layout.addWidget(self.password_display_widget)
        self.main_layout.addWidget(self.manual_entry_widget)
        self.main_layout.addWidget(self.all_passwords_view_widget)

        # Garante que apenas o menu principal seja visível ao iniciar
        self.show_main_options()

    def _create_all_widgets(self):
        """
        Cria e configura todos os widgets que funcionarão como "telas" alternativas.
        """
        # --- 1. Widget do Menu de Opções Principal ---
        self.options_widget = QWidget()
        options_layout = QVBoxLayout(self.options_widget)
        options_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label = QLabel("Escolha uma Opção", self.options_widget)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        options_layout.addWidget(title_label)

        buttons = {
            "Gerar e Salvar Nova Senha": self.show_generated_password,
            "Cadastrar Senha Manualmente": self.show_manual_entry_form,
            "Consultar Senha Existente": self.consult_password,
            "Deletar Senha Salva": self.delete_password
        }
        for text, func in buttons.items():
            btn = QPushButton(text)
            btn.setFixedSize(280, 40)
            if "Deletar" in text:
                btn.setStyleSheet("background-color: #c0392b; color: white; border-radius: 8px;")
            btn.clicked.connect(func)
            options_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_logout = QPushButton("Sair / Deslogar")
        btn_logout.setFixedSize(280, 40)
        btn_logout.setStyleSheet(
            "background-color: #f44336; color: white; border-radius: 8px; font-size: 14px; margin-top: 30px;")
        btn_logout.clicked.connect(self.logout_requested.emit)
        options_layout.addWidget(btn_logout, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- 2. Widget de Exibição de Senha Única (Gerada/Consultada) ---
        self.password_display_widget = QWidget()
        display_layout = QVBoxLayout(self.password_display_widget)
        display_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.display_title_label = QLabel()
        self.display_title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        display_layout.addWidget(self.display_title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.password_output_field = QLineEdit()
        self.password_output_field.setReadOnly(True)
        self.password_output_field.setFixedSize(320, 35)
        self.password_output_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        display_layout.addWidget(self.password_output_field, alignment=Qt.AlignmentFlag.AlignCenter)
        display_buttons_layout = QHBoxLayout()
        self.btn_save_password = QPushButton("Salvar Senha")
        self.btn_save_password.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 8px; padding: 8px 15px;")
        display_buttons_layout.addWidget(self.btn_save_password)
        btn_hide_display = QPushButton("Voltar")
        btn_hide_display.setStyleSheet(
            "background-color: #f44336; color: white; border-radius: 8px; padding: 8px 15px;")
        btn_hide_display.clicked.connect(self.show_main_options)
        display_buttons_layout.addWidget(btn_hide_display)
        display_layout.addLayout(display_buttons_layout)

        # --- 3. Widget de Formulário para Cadastro Manual ---
        self.manual_entry_widget = QWidget()
        manual_layout = QVBoxLayout(self.manual_entry_widget)
        manual_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manual_title_label = QLabel("Cadastrar Senha Manualmente")
        manual_title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        manual_layout.addWidget(manual_title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.manual_name_input = QLineEdit()
        self.manual_name_input.setPlaceholderText("Ex: Conta de Email")
        self.manual_password_input = QLineEdit()
        self.manual_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.manual_password_input.setPlaceholderText("Digite a senha aqui")
        form_layout.addRow(QLabel("Nome do Serviço:"), self.manual_name_input)
        form_layout.addRow(QLabel("Senha:"), self.manual_password_input)
        manual_layout.addLayout(form_layout)
        manual_buttons_layout = QHBoxLayout()
        btn_save_manual = QPushButton("Salvar")
        btn_save_manual.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 8px; padding: 8px 15px;")
        btn_save_manual.clicked.connect(self.process_manual_entry)
        manual_buttons_layout.addWidget(btn_save_manual)
        btn_cancel_manual = QPushButton("Cancelar")
        btn_cancel_manual.setStyleSheet(
            "background-color: #f44336; color: white; border-radius: 8px; padding: 8px 15px;")
        btn_cancel_manual.clicked.connect(self.show_main_options)
        manual_buttons_layout.addWidget(btn_cancel_manual)
        manual_layout.addLayout(manual_buttons_layout)

        # --- 4. Widget de Visualização de Todas as Senhas ---
        self.all_passwords_view_widget = QWidget()
        all_passwords_layout = QVBoxLayout(self.all_passwords_view_widget)
        all_passwords_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        all_passwords_title = QLabel("Todas as Senhas Salvas")
        all_passwords_title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        all_passwords_layout.addWidget(all_passwords_title)
        self.all_passwords_text_edit = QTextEdit()
        self.all_passwords_text_edit.setReadOnly(True)
        self.all_passwords_text_edit.setMinimumSize(450, 300)
        self.all_passwords_text_edit.setStyleSheet(
            "font-size: 14px; font-family: 'Courier New'; background-color: #f0f0f0; border: 1px solid #ccc;")
        all_passwords_layout.addWidget(self.all_passwords_text_edit)
        btn_back_from_list = QPushButton("Voltar")
        btn_back_from_list.setStyleSheet(
            "background-color: #008CBA; color: white; border-radius: 8px; padding: 8px 15px; margin-top: 10px;")
        btn_back_from_list.clicked.connect(self.show_main_options)
        all_passwords_layout.addWidget(btn_back_from_list, alignment=Qt.AlignmentFlag.AlignCenter)

    def _switch_view(self, widget_to_show: QWidget):
        """Oculta todos os widgets da tela e mostra apenas o especificado."""
        for widget in [self.options_widget, self.password_display_widget, self.manual_entry_widget,
                       self.all_passwords_view_widget]:
            widget.hide()
        widget_to_show.show()

    def show_main_options(self):
        """Mostra o menu de opções principal e limpa os campos de outros widgets."""
        # Limpa os campos para evitar que dados antigos reapareçam
        self.password_output_field.clear()
        self.manual_name_input.clear()
        self.manual_password_input.clear()
        self.all_passwords_text_edit.clear()
        self._switch_view(self.options_widget)

    def show_generated_password(self):
        """Gera uma senha e a exibe na área de exibição para salvamento."""
        generated_pwd = password_generator()
        self.display_title_label.setText("Senha Gerada:")
        self.password_output_field.setText(generated_pwd)
        self.password_output_field.setStyleSheet("font-size: 18px; color: #008CBA; font-weight: bold;")

        try:
            self.btn_save_password.clicked.disconnect()
        except TypeError:
            pass  # Ignora erro se não houver conexão prévia

        self.btn_save_password.clicked.connect(partial(self.save_password, generated_pwd))
        self.btn_save_password.show()
        self._switch_view(self.password_display_widget)

    def consult_password(self):
        """Pede o nome da senha, a busca e exibe o resultado na tela."""
        password_name, ok = QInputDialog.getText(self, "Consultar Senha", "Digite o nome da senha:")
        if ok and password_name:
            retrieved_pwd = self.security_service.retrieve_password_by_name(password_name.strip())
            if retrieved_pwd:
                self.display_title_label.setText(f"Senha de '{password_name.strip()}':")
                self.password_output_field.setText(retrieved_pwd)
                self.password_output_field.setStyleSheet("font-size: 18px; color: #4CAF50; font-weight: bold;")
                self.btn_save_password.hide()
                self._switch_view(self.password_display_widget)
            else:
                QMessageBox.warning(self, "Não Encontrada",
                                    f"Senha com o nome '{password_name.strip()}' não encontrada.")
        elif ok:
            QMessageBox.warning(self, "Aviso", "O nome da senha não pode ser vazio.")

    def save_password(self, password_to_save: str):
        """Pede um nome e salva a senha fornecida (usado pela geração de senha)."""
        password_name, ok = QInputDialog.getText(self, "Nome da Senha", "Digite um nome para esta senha:")
        if ok and password_name:
            if self.security_service.save_password_entry(password_name.strip(), password_to_save):
                QMessageBox.information(self, "Sucesso", f"Senha para '{password_name.strip()}' salva com sucesso!")
                self.show_main_options()
            else:
                QMessageBox.critical(self, "Erro", f"O nome '{password_name.strip()}' já existe ou ocorreu um erro.")
        elif ok:
            QMessageBox.warning(self, "Aviso", "O nome da senha não pode ser vazio. Senha não salva.")

    def delete_password(self):
        """Solicita o nome da senha, pede confirmação e a deleta."""
        password_name, ok = QInputDialog.getText(self, "Deletar Senha", "Digite o nome da senha que deseja DELETAR:")
        if ok and password_name:
            confirm_reply = QMessageBox.question(self, 'Confirmar Exclusão',
                                                 f"Você tem certeza que deseja deletar a senha para '{password_name.strip()}'?\n\nEsta ação não pode ser desfeita.",
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            if confirm_reply == QMessageBox.StandardButton.Yes:
                if self.security_service.delete_password_by_name(password_name.strip()):
                    QMessageBox.information(self, "Sucesso", f"A senha para '{password_name.strip()}' foi deletada.")
                else:
                    QMessageBox.warning(self, "Erro",
                                        f"A senha com o nome '{password_name.strip()}' não foi encontrada.")
        elif ok:
            QMessageBox.warning(self, "Aviso", "O nome da senha não pode ser vazio.")

    def show_manual_entry_form(self):
        """Exibe o formulário de cadastro manual."""
        self._switch_view(self.manual_entry_widget)

    def process_manual_entry(self):
        """Pega os dados do formulário e salva a nova entrada de senha."""
        name = self.manual_name_input.text().strip()
        password = self.manual_password_input.text()
        if not name or not password:
            QMessageBox.warning(self, "Campos Vazios", "Por favor, preencha o nome e a senha.")
            return
        if self.security_service.save_password_entry(name, password):
            QMessageBox.information(self, "Sucesso", f"Senha para '{name}' cadastrada com sucesso!")
            self.show_main_options()
        else:
            QMessageBox.critical(self, "Erro ao Salvar",
                                 f"O nome '{name}' já existe ou ocorreu um erro ao salvar a senha.")

