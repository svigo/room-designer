#!/bin/bash
# Script de actualización rápida a GitHub
# Uso: ./update.sh "mensaje opcional"

clear
echo "🚀 Actualizando GitHub..."
echo ""

# Si hay mensaje, usarlo; sino usar fecha
if [ -z "$1" ]; then
    MSG="Actualización $(date '+%Y-%m-%d %H:%M')"
else
    MSG="$1"
fi

# Todo en un solo paso
git add . && \
git commit -m "$MSG" && \
git push origin main

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Listo! Código actualizado en GitHub"
    echo "   Mensaje: $MSG"
else
    echo ""
    echo "❌ Hubo un error. Posibles causas:"
    echo "   1. No hay cambios para subir"
    echo "   2. Problemas de conexión"
    echo "   3. Conflictos con versión remota"
    echo ""
    echo "Solución rápida:"
    echo "   git pull origin main"
    echo "   ./update.sh"
fi
