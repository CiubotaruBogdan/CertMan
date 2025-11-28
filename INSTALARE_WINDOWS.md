# Ghid Instalare Windows

## Problemă Comună: Python 3.13 și pandas

Dacă întâmpinați eroarea:
```
ERROR: Failed to build 'pandas' when installing build dependencies for pandas
```

**Cauza:** Python 3.13 este foarte nou și pandas necesită compilare C++ care lipsește pe Windows.

## Soluții

### Opțiunea 1: Folosiți Python 3.11 sau 3.12 (RECOMANDAT)

1. **Descărcați Python 3.12:**
   - Mergeți la: https://www.python.org/downloads/
   - Descărcați Python 3.12.x (nu 3.13)
   - Instalați cu opțiunea "Add Python to PATH"

2. **Instalați dependențele:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Rulați aplicația:**
   ```powershell
   python main.py
   ```

### Opțiunea 2: Instalare Manuală cu Wheel-uri Pre-compilate

Dacă trebuie să folosiți Python 3.13:

```powershell
# Instalați PyQt6 (funcționează fără probleme)
pip install PyQt6

# Instalați pandas cu versiune mai nouă (are wheel pentru 3.13)
pip install pandas --upgrade

# Instalați openpyxl
pip install openpyxl
```

### Opțiunea 3: Folosiți Executabilul (CEL MAI SIMPLU)

Rulați scriptul de build pentru a crea executabil standalone:

```powershell
python build_executable.py
```

După build, executabilul va fi în `dist/CertificateManager.exe` și nu mai necesită Python instalat!

## Verificare Instalare

După instalare, testați:

```powershell
python -c "import PyQt6; import pandas; import openpyxl; print('✓ Toate dependențele sunt instalate!')"
```

## Rulare Aplicație

```powershell
# Din folderul certificate_manager
python main.py
```

sau folosiți scriptul:

```powershell
.\run.bat
```

## Suport

Dacă problemele persistă:
- Verificați versiunea Python: `python --version`
- Reinstalați cu Python 3.12 în loc de 3.13
- Sau folosiți executabilul creat cu `build_executable.py`
