#!/usr/bin/env python3
"""
Sistema de notificações para atualizações do GitButler AUR
"""

import json
import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from urllib.request import urlopen, Request

def send_desktop_notification(title, message, urgency="normal"):
    """Envia notificação desktop via notify-send."""
    try:
        subprocess.run(['notify-send', '-u', urgency, title, message], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def send_email_notification(subject, body, to_email, smtp_config=None):
    """Envia notificação por email."""
    if not smtp_config:
        smtp_config = {
            'server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'port': int(os.getenv('SMTP_PORT', '587')),
            'username': os.getenv('SMTP_USERNAME'),
            'password': os.getenv('SMTP_PASSWORD'),
            'from_email': os.getenv('SMTP_FROM_EMAIL')
        }

    if not all([smtp_config['username'], smtp_config['password'], smtp_config['from_email']]):
        print("Configuração SMTP incompleta")
        return False

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = smtp_config['from_email']
        msg['To'] = to_email

        server = smtplib.SMTP(smtp_config['server'], smtp_config['port'])
        server.starttls()
        server.login(smtp_config['username'], smtp_config['password'])
        server.sendmail(smtp_config['from_email'], [to_email], msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

def send_discord_webhook(webhook_url, message, username="GitButler AUR Bot"):
    """Envia notificação via Discord webhook."""
    try:
        data = {
            "content": message,
            "username": username
        }

        request = Request(webhook_url,
                         data=json.dumps(data).encode(),
                         headers={'Content-Type': 'application/json'})

        with urlopen(request) as response:
            return response.status == 204

    except Exception as e:
        print(f"Erro ao enviar webhook Discord: {e}")
        return False

def send_slack_webhook(webhook_url, message):
    """Envia notificação via Slack webhook."""
    try:
        data = {"text": message}

        request = Request(webhook_url,
                         data=json.dumps(data).encode(),
                         headers={'Content-Type': 'application/json'})

        with urlopen(request) as response:
            return response.status == 200

    except Exception as e:
        print(f"Erro ao enviar webhook Slack: {e}")
        return False

def notify_update_available(version, release_url):
    """Notifica que uma nova versão está disponível."""
    title = "GitButler AUR - Nova Versão"
    message = f"Nova versão {version} disponível!\n{release_url}"

    methods = []

    # Desktop notification
    if send_desktop_notification(title, f"Nova versão {version} disponível!"):
        methods.append("desktop")

    # Email (se configurado)
    email = os.getenv('NOTIFICATION_EMAIL')
    if email:
        if send_email_notification(title, message, email):
            methods.append("email")

    # Discord (se configurado)
    discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
    if discord_webhook:
        if send_discord_webhook(discord_webhook, f"🔄 {title}\n{message}"):
            methods.append("discord")

    # Slack (se configurado)
    slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
    if slack_webhook:
        if send_slack_webhook(slack_webhook, f"{title}\n{message}"):
            methods.append("slack")

    return methods

def notify_update_published(version):
    """Notifica que uma atualização foi publicada com sucesso."""
    title = "GitButler AUR - Publicado"
    message = f"Versão {version} publicada com sucesso no AUR!"

    methods = []

    if send_desktop_notification(title, message, "low"):
        methods.append("desktop")

    email = os.getenv('NOTIFICATION_EMAIL')
    if email:
        if send_email_notification(title, message, email):
            methods.append("email")

    discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
    if discord_webhook:
        if send_discord_webhook(discord_webhook, f"✅ {title}\n{message}"):
            methods.append("discord")

    slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
    if slack_webhook:
        if send_slack_webhook(slack_webhook, f"{title}\n{message}"):
            methods.append("slack")

    return methods

def notify_error(error_message):
    """Notifica sobre erro durante atualização."""
    title = "GitButler AUR - Erro"
    message = f"Erro durante atualização: {error_message}"

    methods = []

    if send_desktop_notification(title, error_message, "critical"):
        methods.append("desktop")

    email = os.getenv('NOTIFICATION_EMAIL')
    if email:
        if send_email_notification(title, message, email):
            methods.append("email")

    discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
    if discord_webhook:
        if send_discord_webhook(discord_webhook, f"❌ {title}\n{message}"):
            methods.append("discord")

    slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
    if slack_webhook:
        if send_slack_webhook(slack_webhook, f"{title}\n{message}"):
            methods.append("slack")

    return methods

if __name__ == "__main__":
    # Teste das notificações
    print("Testando sistema de notificações...")
    methods = notify_update_available("0.16.8", "https://github.com/gitbutlerapp/gitbutler/releases/tag/v0.16.8")
    print(f"Notificações enviadas via: {', '.join(methods)}")