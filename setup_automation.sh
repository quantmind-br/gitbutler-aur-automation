#!/bin/bash
"""
Script para configurar automação local via crontab
"""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 Configurando automação do GitButler AUR..."

# Criar entrada no crontab
CRON_JOB="0 */6 * * * cd $SCRIPT_DIR && ./auto_update.sh --notify >> /tmp/gitbutler-aur-update.log 2>&1"

# Verificar se já existe
if crontab -l 2>/dev/null | grep -q "gitbutler-aur-update"; then
    echo "⚠️  Automação já configurada no crontab"
else
    # Adicionar ao crontab
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Crontab configurado - verificará a cada 6 horas"
fi

echo ""
echo "📋 Comandos disponíveis:"
echo "  ./auto_update.sh              - Verificar manualmente"
echo "  ./auto_update.sh --commit     - Verificar e fazer commit automático"
echo "  ./auto_update.sh --notify     - Com notificações desktop"
echo ""
echo "📊 Para monitorar logs:"
echo "  tail -f /tmp/gitbutler-aur-update.log"
echo ""
echo "🗑️  Para remover automação:"
echo "  crontab -l | grep -v 'gitbutler-aur-update' | crontab -"