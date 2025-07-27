#!/bin/bash
# ==============================================================================
# SCRIPT DE BUILD FINAL (V3) - PASSANDO VARIÁVEIS DIRETAMENTE
# ==============================================================================

# Nome do arquivo de log
LOG_FILE="saida.txt"
rm -f "$LOG_FILE"

{
    set -x

    echo "--- INICIANDO O PROCESSO DE BUILD (V3) ---"
    echo "Data e Hora: $(date)"
    echo ""

    echo "--- [ETAPA 0/6] Verificando Ambiente ---"
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "ERRO CRÍTICO: Ambiente virtual não está ativo."
        exit 1
    fi
    echo "Ambiente virtual detectado."
    echo ""

    echo "--- [ETAPA 1/6] Limpeza Total ---"
    rm -rf AppDir dist build Guardian_Wolf-x86_64.AppImage
    echo ""

    echo "--- [ETAPA 2/6] Executando o PyInstaller ---"
    pyinstaller --name="GuardianWolf" --noconfirm --add-data="data:data" main_app.py
    echo ""

    echo "--- [ETAPA 3/6] Montando a AppDir e Criando .desktop ---"
    mv dist/GuardianWolf AppDir
    cp assets/App.png AppDir/GuardianWolf.png
    cat > AppDir/GuardianWolf.desktop <<EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Guardian Wolf
Comment=Seu gerenciador de senhas seguro e fácil de usar
Exec=AppRun
Icon=GuardianWolf
Categories=Utility;Security;
EOL
    echo "Arquivo GuardianWolf.desktop criado."
    echo ""

    echo "--- [ETAPA 4/6] Encontrando Caminhos ---"
    SITE_PACKAGES=$(python3 -c "import sysconfig; print(sysconfig.get_paths()['purelib'])")
    QMAKE_PATH="$SITE_PACKAGES/PyQt6_Qt6/Qt6/bin/qmake"
    QT_LIBS_PATH="$SITE_PACKAGES/PyQt6_Qt6/Qt6/lib"

    echo "Caminho do qmake: $QMAKE_PATH"
    echo "Caminho das bibliotecas: $QT_LIBS_PATH"
    echo ""

    echo "--- [ETAPA 5/6] Executando o linuxdeploy com Variáveis Diretas ---"

    # ** A MUDANÇA ESTÁ AQUI **
    # Passamos as variáveis diretamente na mesma linha de comando,
    # o que é a forma mais confiável de garantir que o linuxdeploy as veja.
    QMAKE="$QMAKE_PATH" LD_LIBRARY_PATH="$QT_LIBS_PATH" ./linuxdeploy-x86_64.AppImage -v 3 --appdir AppDir --plugin qt --desktop-file AppDir/GuardianWolf.desktop --output appimage

    LINUXDEPLOY_EXIT_CODE=$?
    echo "linuxdeploy finalizado com o código de saída: $LINUXDEPLOY_EXIT_CODE"
    echo ""
    
    echo "--- [ETAPA 6/6] Verificação Final ---"
    set +x
    
} > "$LOG_FILE" 2>&1

# --- MENSAGENS FINAIS ---

echo ""
echo "=================================================================="
echo " Processo de build concluído. Log salvo em: saida.txt "
echo "=================================================================="
echo ""

if [ -f "Guardian_Wolf-x86_64.AppImage" ]; then
    echo "✅ SUCESSO: O arquivo 'Guardian_Wolf-x86_64.AppImage' foi gerado!"
else
    echo "❌ FALHA: O arquivo AppImage não foi encontrado. Revise o 'saida.txt'."
fi
echo ""