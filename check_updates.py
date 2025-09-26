#!/usr/bin/env python3
"""
Script para verificar novas versões do GitButler e atualizar o PKGBUILD automaticamente.
"""

import json
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

# Configurações
REPO_OWNER = "gitbutlerapp"
REPO_NAME = "gitbutler"
PKGBUILD_PATH = Path(__file__).parent / "PKGBUILD"
CURRENT_VERSION_FILE = Path(__file__).parent / ".current_version"

def get_latest_release():
    """Obtém a última release do GitHub."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"

    try:
        request = Request(url)
        request.add_header('User-Agent', 'AUR-GitButler-Bot/1.0')

        with urlopen(request) as response:
            data = json.loads(response.read().decode())
            # Remove prefixos como 'v', 'release/' etc.
            version = data['tag_name'].lstrip('v').replace('release/', '')
            return version, data['html_url']

    except URLError as e:
        print(f"Erro ao verificar releases: {e}")
        return None, None

def get_current_version():
    """Lê a versão atual do arquivo de controle."""
    if CURRENT_VERSION_FILE.exists():
        return CURRENT_VERSION_FILE.read_text().strip()
    return None

def update_current_version(version):
    """Salva a nova versão no arquivo de controle."""
    CURRENT_VERSION_FILE.write_text(version)

def get_download_url(version):
    """Gera a URL de download baseada na versão."""
    # Você pode precisar ajustar isso baseado no padrão de URL do GitButler
    build_number = "2433"  # Pode precisar ser dinâmico
    return f"https://releases.gitbutler.com/releases/release/{version}-{build_number}/linux/x86_64/GitButler_{version}_amd64.AppImage.tar.gz"

def verify_download_url(url):
    """Verifica se a URL de download existe."""
    try:
        request = Request(url)
        request.get_method = lambda: 'HEAD'
        with urlopen(request):
            return True
    except URLError:
        return False

def update_pkgbuild(new_version):
    """Atualiza o PKGBUILD com a nova versão."""
    if not PKGBUILD_PATH.exists():
        print("PKGBUILD não encontrado!")
        return False

    content = PKGBUILD_PATH.read_text()

    # Atualizar pkgver
    content = re.sub(r'^pkgver=.*', f'pkgver={new_version}', content, flags=re.MULTILINE)

    # Resetar pkgrel para 1
    content = re.sub(r'^pkgrel=.*', 'pkgrel=1', content, flags=re.MULTILINE)

    # Verificar se precisa atualizar a URL (se contém build number)
    download_url = get_download_url(new_version)
    if not verify_download_url(download_url):
        print(f"URL de download não encontrada: {download_url}")
        # Tentar URLs alternativas ou notificar para verificação manual
        return False

    PKGBUILD_PATH.write_text(content)
    return True

def generate_srcinfo():
    """Gera o arquivo .SRCINFO."""
    try:
        subprocess.run(['makepkg', '--printsrcinfo'],
                      stdout=open('.SRCINFO', 'w'),
                      cwd=PKGBUILD_PATH.parent,
                      check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def test_build():
    """Testa se o pacote compila corretamente."""
    try:
        subprocess.run(['makepkg', '-f'],
                      cwd=PKGBUILD_PATH.parent,
                      check=True,
                      capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro no build: {e}")
        return False

def send_notification(message):
    """Envia notificação (implementar conforme preferência)."""
    print(f"NOTIFICAÇÃO: {message}")
    # Aqui você pode implementar:
    # - Envio de email
    # - Notificação do desktop
    # - Webhook para Discord/Slack
    # - etc.

def main():
    print("Verificando novas versões do GitButler...")

    latest_version, release_url = get_latest_release()
    if not latest_version:
        print("Não foi possível verificar a versão mais recente")
        return

    current_version = get_current_version()

    if current_version == latest_version:
        print(f"Já está na versão mais recente: {latest_version}")
        return

    print(f"Nova versão encontrada: {latest_version}")
    print(f"Versão atual: {current_version or 'desconhecida'}")

    # Atualizar PKGBUILD
    if not update_pkgbuild(latest_version):
        send_notification(f"Falha ao atualizar PKGBUILD para versão {latest_version}")
        return

    # Gerar .SRCINFO
    if not generate_srcinfo():
        send_notification(f"Falha ao gerar .SRCINFO para versão {latest_version}")
        return

    # Testar build
    print("Testando build...")
    if not test_build():
        send_notification(f"Build falhou para versão {latest_version}")
        return

    # Salvar nova versão
    update_current_version(latest_version)

    send_notification(f"GitButler atualizado para versão {latest_version}! Build testado com sucesso.")
    print(f"Arquivos atualizados. Faça commit e push para o AUR:")
    print(f"git add PKGBUILD .SRCINFO")
    print(f"git commit -m 'Update to v{latest_version}'")
    print(f"git push")

if __name__ == "__main__":
    main()