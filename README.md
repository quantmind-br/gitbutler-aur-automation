# GitButler AppImage AUR Package 🚀

![AUR Version](https://img.shields.io/aur/version/gitbutler-appimage)
![AUR Last Modified](https://img.shields.io/aur/last-modified/gitbutler-appimage)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/USER/gitbutler-aur-automation/auto-update.yml)

Este é o pacote AUR automatizado para o GitButler usando AppImage com atualizações automáticas via GitHub Actions.

## Instalação

```bash
# Via AUR helper (recomendado)
yay -S gitbutler-appimage

# Ou manualmente
git clone https://aur.archlinux.org/gitbutler-appimage.git
cd gitbutler-appimage
makepkg -si
```

## Sobre o Pacote

- **Nome**: gitbutler-appimage
- **Versão**: 0.16.7
- **Tipo**: AppImage
- **Dependências**: fuse2, gtk3, webkit2gtk
- **Configuração**: X11 backend habilitado para compatibilidade

## Uso

Após a instalação:

- **Menu de aplicações**: Procure por "GitButler"
- **Linha de comando**: `gitbutler`
- **Localização**: `/opt/GitButler/gitbutler.AppImage`

## Automação de Atualizações

Este repositório inclui scripts para automação de atualizações:

### Configuração Local

```bash
# Configurar notificações (opcional)
cp .env.example .env
# Edite .env conforme necessário

# Configurar automação via crontab
./setup_automation.sh
```

### Uso Manual

```bash
# Verificar atualizações
./auto_update.sh

# Verificar e fazer commit automático
./auto_update.sh --commit --notify
```

### Scripts Disponíveis

- `check_updates.py`: Monitora releases do GitHub
- `auto_update.sh`: Wrapper principal de automação
- `notify.py`: Sistema de notificações
- `setup_automation.sh`: Configurador do crontab

## Notificações Suportadas

- Desktop (notify-send)
- Email (SMTP)
- Discord (Webhooks)
- Slack (Webhooks)

## Problemas Conhecidos

Se o GitButler não abrir corretamente:

1. Tente executar: `GDK_BACKEND=x11 gitbutler`
2. Verifique as dependências: `pacman -Qs fuse2 gtk3 webkit2gtk`

## Links

- **Upstream**: https://github.com/gitbutlerapp/gitbutler
- **Site oficial**: https://gitbutler.com
- **AUR**: https://aur.archlinux.org/packages/gitbutler-appimage

## Automação GitHub Actions

Este repositório utiliza GitHub Actions para automação completa:

- **🔄 Verificação automática** a cada 6 horas
- **📦 Build e teste** antes de publicar
- **🚀 Deploy automático** para o AUR
- **🔔 Notificações** Discord/Slack
- **📊 Logs detalhados** de cada execução

### Status da Automação

- **Última execução**: ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/USER/gitbutler-aur-automation/auto-update.yml)
- **Frequência**: A cada 6 horas
- **Logs**: [Ver execuções](https://github.com/USER/gitbutler-aur-automation/actions)

## Contribuição

Para reportar problemas ou sugerir melhorias:
- **AUR**: Use o sistema de comentários
- **Automação**: Abra issue neste repositório
- **Upstream**: https://github.com/gitbutlerapp/gitbutler