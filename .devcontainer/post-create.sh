#!/usr/bin/env bash
# Draait eenmalig nadat de Codespace is aangemaakt.
set -e

echo "==> Python-pakketten installeren"
pip install --user --upgrade pip
pip install --user -r requirements.txt

echo "==> Wachten op de database"
for i in $(seq 1 30); do
  pg_isready -d "$DATABASE_URL" -q && break
  sleep 1
done

echo "==> Database en vertalingen klaarzetten"
python manage.py migrate --no-input
python manage.py compilemessages -l nl

echo "==> Claude Code installeren"
curl -fsSL https://claude.ai/install.sh | bash

echo "==> Klaar. Typ 'claude' in de terminal om verder te bouwen."
