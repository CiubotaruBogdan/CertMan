#!/bin/bash
# Script de pornire pentru Manager Certificate Securitate - Linux/macOS

echo "========================================"
echo "Manager Certificate Securitate"
echo "========================================"
echo ""

# Verifică dacă Python3 este instalat
if ! command -v python3 &> /dev/null; then
    echo "EROARE: Python3 nu este instalat"
    echo ""
    echo "Instalați Python3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora/RHEL: sudo dnf install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo ""
    exit 1
fi

# Verifică versiunea Python
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python versiune: $PYTHON_VERSION"
echo ""

# Pornește aplicația
echo "Pornire aplicație..."
echo ""
python3 main.py

# Verifică codul de ieșire
if [ $? -ne 0 ]; then
    echo ""
    echo "EROARE: Aplicația s-a închis cu erori"
    echo ""
    read -p "Apăsați Enter pentru a închide..."
fi
