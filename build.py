import os
import platform
import subprocess

# --- Configurações ---
APP_NAME = "GerenciadorDeSenhas"
ENTRY_POINT = "main_app.py"
DATA_FOLDER = "data"

def build():
    # Detecta o separador correto
    data_separator = os.pathsep

    # Monta a flag --add-data
    add_data_flag = f'--add-data="{DATA_FOLDER}{data_separator}{DATA_FOLDER}"'

    # Define a flag de ícone com base no SO
    icon_flag = ""
    if platform.system() == "Windows":
        icon_flag = '--icon="assets/icone.ico"'
    elif platform.system() == "Darwin": # Darwin é o nome do kernel do macOS
        icon_flag = '--icon="assets/icone.icns"'

    # Monta o comando final
    command = f"""
        pyinstaller --name="{APP_NAME}" \
                    --onefile \
                    --windowed \
                    {icon_flag} \
                    {add_data_flag} \
                    {ENTRY_POINT}
    """

    print("--- Executando o comando de build ---")
    print(command)
    print("------------------------------------")

    # Executa o comando
    subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    build()