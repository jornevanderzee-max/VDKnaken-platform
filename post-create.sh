#!/usr/bin/env bash
# Draait eenmalig nadat de Codespace is aangemaakt.
set -e

echo "==> Python-pakketten installeren"
pip install --user --upgrade pip
pip install --user -r requirements.txt

echo "==> Claude Code installeren"
curl -fsSL https://claude.ai/install.sh | bash

echo "==> Klaar. Typ 'claude' in de terminal om verder te bouwen."
