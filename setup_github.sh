#!/bin/bash
"""
Script para configurar GitHub Actions para automação AUR
"""

set -euo pipefail

REPO_NAME="gitbutler-aur-automation"

echo "🚀 Configurando GitHub Actions para GitButler AUR"
echo "=============================================="

# Verificar se git está configurado
if ! git config user.name >/dev/null 2>&1; then
    echo "⚠️  Git não configurado. Configurando..."
    read -p "Seu nome para commits: " git_name
    read -p "Seu email: " git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
fi

# Verificar se tem GitHub CLI
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI encontrado"

    # Autenticar se necessário
    if ! gh auth status &> /dev/null; then
        echo "🔐 Autenticando no GitHub..."
        gh auth login
    fi

    # Criar repositório
    echo "📦 Criando repositório no GitHub..."
    if gh repo create "$REPO_NAME" --public --source=. --remote=github --push; then
        echo "✅ Repositório criado e código enviado!"
        REPO_URL=$(gh repo view --json url -q .url)
    else
        echo "⚠️  Repositório pode já existir. Tentando adicionar remote..."
        git remote add github "https://github.com/$(gh api user -q .login)/$REPO_NAME.git" || true
        git push -u github master
        REPO_URL="https://github.com/$(gh api user -q .login)/$REPO_NAME"
    fi

else
    echo "❌ GitHub CLI não encontrado"
    echo "📝 Você precisa:"
    echo "   1. Ir para https://github.com/new"
    echo "   2. Nome: $REPO_NAME"
    echo "   3. Público: ✅"
    echo "   4. Não inicializar com README"
    echo ""
    read -p "Qual seu usuário GitHub? " github_user
    REPO_URL="https://github.com/$github_user/$REPO_NAME"

    echo "🔗 Adicionando remote..."
    git remote add github "$REPO_URL.git" || true

    echo "📤 Enviando código..."
    git push -u github master
fi

echo ""
echo "🔐 CONFIGURAR SECRETS"
echo "===================="
echo ""
echo "Acesse: $REPO_URL/settings/secrets/actions"
echo ""
echo "1️⃣ Adicionar secret AUR_SSH_KEY:"
echo "   Nome: AUR_SSH_KEY"
echo "   Valor: (cole sua chave SSH privada abaixo)"
echo ""
echo "📋 Sua chave SSH privada:"
echo "------------------------"
cat ~/.ssh/id_ed25519
echo ""
echo "------------------------"
echo ""

# Verificar se há webhooks configurados
if [[ -f .env ]]; then
    echo "2️⃣ Secrets opcionais encontrados em .env:"
    while IFS= read -r line; do
        if [[ $line =~ ^([^=]+)=(.*)$ ]]; then
            key="${BASH_REMATCH[1]}"
            echo "   - $key (valor em .env)"
        fi
    done < .env
else
    echo "2️⃣ Secrets opcionais (se quiser notificações):"
    echo "   - DISCORD_WEBHOOK"
    echo "   - SLACK_WEBHOOK"
fi

echo ""
echo "⚡ HABILITAR ACTIONS"
echo "==================="
echo ""
echo "1. Acesse: $REPO_URL/actions"
echo "2. Clique 'I understand my workflows, go ahead and enable them'"
echo "3. Verifique se 'Auto Update GitButler AUR' aparece"
echo ""

echo "🧪 TESTAR"
echo "========="
echo ""
echo "1. Actions → Auto Update GitButler AUR → Run workflow"
echo "2. Acompanhar logs em tempo real"
echo "3. Verificar se commit aparece no AUR"
echo ""

echo "📊 MONITORAR"
echo "============"
echo ""
echo "- Workflow: $REPO_URL/actions"
echo "- AUR: https://aur.archlinux.org/packages/gitbutler-appimage"
echo "- Logs: Executam a cada 6 horas automaticamente"
echo ""

echo "✅ Configuração GitHub concluída!"
echo ""
echo "📋 Próximos passos:"
echo "   1. Configurar secrets (obrigatório)"
echo "   2. Habilitar Actions (obrigatório)"
echo "   3. Testar workflow (recomendado)"
echo "   4. Configurar webhooks (opcional)"