# Configuração do GitHub Actions

Este guia explica como configurar a automação do GitHub Actions para manter o pacote AUR atualizado.

## 🔧 Configuração Inicial

### 1. Criar Repositório GitHub

```bash
# Opção A: Via GitHub CLI
gh repo create gitbutler-aur-automation --public --source=. --remote=github --push

# Opção B: Via web (github.com/new) + manual
git remote add github https://github.com/SEU_USUARIO/gitbutler-aur-automation.git
git push -u github master
```

### 2. Configurar Secrets

Acesse: **Settings** → **Secrets and variables** → **Actions**

#### Secrets Obrigatórios:

- **`AUR_SSH_KEY`**: Sua chave SSH privada para o AUR
  ```bash
  cat ~/.ssh/id_ed25519
  ```

#### Secrets Opcionais:

- **`DISCORD_WEBHOOK`**: URL do webhook Discord
- **`SLACK_WEBHOOK`**: URL do webhook Slack

### 3. Habilitar Actions

1. Acesse: **Actions** tab
2. Clique **"I understand my workflows, go ahead and enable them"**
3. Verifique se o workflow `auto-update.yml` aparece

## 🚀 Funcionamento

### Triggers Automáticos:

- **Cron**: A cada 6 horas (`0 */6 * * *`)
- **Manual**: Via botão "Run workflow"
- **Webhook**: Via `repository_dispatch`

### O que o Workflow Faz:

1. **🔍 Verifica** novas releases do GitButler
2. **📝 Atualiza** PKGBUILD e .SRCINFO
3. **🧪 Valida** sintaxe e configurações
4. **📦 Clona** repositório AUR via SSH
5. **💾 Commit** mudanças no AUR
6. **📢 Notifica** via Discord/Slack
7. **📊 Cria** release no GitHub

## 🔔 Configurar Notificações

### Discord Webhook:

1. Server Settings → Integrations → Webhooks
2. New Webhook → Copy URL
3. Adicionar como secret `DISCORD_WEBHOOK`

### Slack Webhook:

1. Slack App Directory → Incoming Webhooks
2. Add to Slack → Choose channel
3. Copy URL → Adicionar como `SLACK_WEBHOOK`

## 🛠️ Testes

### Teste Manual:

1. Actions → Auto Update GitButler AUR
2. **Run workflow** → **Run workflow**
3. Acompanhar logs em tempo real

### Teste de SSH:

```bash
# Verificar se chave funciona
ssh -T aur@aur.archlinux.org
# Deve retornar: "interactive shell is disabled"
```

## 📊 Monitoramento

### Logs Disponíveis:

- **GitHub Actions**: Logs completos de execução
- **AUR History**: Commits no repositório AUR
- **Notificações**: Discord/Slack confirmações

### Status Badges:

Adicione ao seu README:

```markdown
![Workflow Status](https://img.shields.io/github/actions/workflow/status/SEU_USUARIO/gitbutler-aur-automation/auto-update.yml)
![AUR Version](https://img.shields.io/aur/version/gitbutler-appimage)
```

## 🔧 Troubleshooting

### Erro de SSH:

- Verifique se `AUR_SSH_KEY` está configurado
- Confirme que a chave SSH está ativa no AUR
- Teste conexão local primeiro

### Erro de Build:

- Verifique logs do workflow
- Teste `makepkg` localmente
- Verifique URL de download

### Notificações não Funcionam:

- Confirme webhooks no Discord/Slack
- Verifique se secrets estão configurados
- Teste URLs manualmente

## 🔄 Atualizações

Para atualizar o workflow:

1. Edite `.github/workflows/auto-update.yml`
2. Commit e push
3. Workflow será atualizado automaticamente

---

**✅ Depois de configurado, o sistema funcionará 100% automaticamente!**