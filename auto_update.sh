#!/bin/bash
"""
Script wrapper para automatizar atualizações do GitButler AUR
Uso: ./auto_update.sh [--commit] [--notify]
"""

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

COMMIT=false
NOTIFY=false

# Parse argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --commit)
            COMMIT=true
            shift
            ;;
        --notify)
            NOTIFY=true
            shift
            ;;
        *)
            echo "Uso: $0 [--commit] [--notify]"
            echo "  --commit: Faz commit automático se houver atualizações"
            echo "  --notify: Envia notificações desktop"
            exit 1
            ;;
    esac
done

echo "🔍 Verificando atualizações do GitButler..."

# Executar script Python
if python3 check_updates.py; then
    echo "✅ Verificação concluída"

    # Verificar se houve mudanças
    if git diff --quiet PKGBUILD .SRCINFO; then
        echo "📄 Nenhuma atualização necessária"
        exit 0
    fi

    echo "🔄 Arquivos foram atualizados!"

    # Mostrar diferenças
    echo "Mudanças no PKGBUILD:"
    git diff PKGBUILD || true

    if [ "$COMMIT" = true ]; then
        # Extrair nova versão do PKGBUILD
        NEW_VERSION=$(grep "^pkgver=" PKGBUILD | cut -d= -f2)

        echo "💾 Fazendo commit das mudanças..."
        git add PKGBUILD .SRCINFO
        git commit -m "Update GitButler to v${NEW_VERSION}"

        echo "📤 Fazendo push para o AUR..."
        git push

        if [ "$NOTIFY" = true ]; then
            notify-send "GitButler AUR" "Atualizado para v${NEW_VERSION} e enviado para o AUR!"
        fi

        echo "🎉 GitButler v${NEW_VERSION} publicado no AUR!"
    else
        echo "📋 Para fazer commit das mudanças:"
        echo "  git add PKGBUILD .SRCINFO"
        echo "  git commit -m 'Update to v$(grep "^pkgver=" PKGBUILD | cut -d= -f2)'"
        echo "  git push"

        if [ "$NOTIFY" = true ]; then
            notify-send "GitButler AUR" "Nova versão disponível! Execute com --commit para publicar."
        fi
    fi
else
    echo "❌ Erro durante verificação de atualizações"

    if [ "$NOTIFY" = true ]; then
        notify-send "GitButler AUR" "Erro ao verificar atualizações!" -u critical
    fi

    exit 1
fi