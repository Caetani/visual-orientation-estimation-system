#!/bin/bash
set -e

# Diretório de origem (onde está o código-fonte)
SOURCE_DIR="$HOME/projects/systems/visual-orientation-estimation-system/orientation_estimator"

# Diretório de destino do zip gerado
DEST_DIR="$HOME/projects/systems/visual-orientation-estimation-system/prod/orientation_estimator"

ZIP_NAME="deploy.zip"

cd "$SOURCE_DIR"

# Garante que a pasta de destino existe
mkdir -p "$DEST_DIR"

# Remove o zip anterior no destino, se existir
if [ -f "$DEST_DIR/$ZIP_NAME" ]; then
    echo "Removendo zip anterior: $DEST_DIR/$ZIP_NAME"
    rm "$DEST_DIR/$ZIP_NAME"
fi

echo "Gerando $ZIP_NAME a partir de $SOURCE_DIR ..."

zip -r "$ZIP_NAME" . \
    -x "*__pycache__*" \
    -x "*.pyc" \
    -x "*.git*" \
    -x "*venv*"

# Move o zip gerado para a pasta de destino
mv "$ZIP_NAME" "$DEST_DIR/$ZIP_NAME"

echo "Zip gerado e movido com sucesso para: $DEST_DIR/$ZIP_NAME"
echo "Conteúdo do zip:"
unzip -l "$DEST_DIR/$ZIP_NAME"
