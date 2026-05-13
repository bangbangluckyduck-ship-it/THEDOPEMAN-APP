#!/bin/bash
set -e

echo ""
echo "================================================"
echo "  Installation TikTok Shop Analyzer"
echo "================================================"

# Virtual environment
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip --quiet

echo "Installation des dépendances..."
pip install -r requirements.txt --quiet

# .env
if [ ! -f .env ]; then
  cp .env.example .env
fi

echo ""
echo "================================================"
echo "  Installation terminée !"
echo ""
echo "  Prochaine étape :"
echo "  1. Ouvre le fichier .env et colle ta clé API :"
echo "     ANTHROPIC_API_KEY=sk-ant-api03-..."
echo ""
echo "  2. Lance l'app :"
echo "     source venv/bin/activate"
echo "     python main.py"
echo "================================================"
echo ""
