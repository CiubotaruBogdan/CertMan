#!/usr/bin/env python3
"""
Script pentru crearea executabilului aplicației
Folosește PyInstaller pentru a crea un executabil standalone
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build_dirs():
    """Curăță directoarele de build anterioare"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    print("🧹 Curățare directoare build...")
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ Șters {dir_name}/")
    
    # Șterge fișiere .spec
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"  ✓ Șters {spec_file}")
    
    print()


def build_executable():
    """Construiește executabilul"""
    print("🔨 Construire executabil...")
    print()
    
    # Detectează sistemul de operare
    is_windows = sys.platform.startswith('win')
    exe_name = "CertificateManager.exe" if is_windows else "CertificateManager"
    
    # Opțiuni PyInstaller
    pyinstaller_args = [
        'pyinstaller',
        '--name=CertificateManager',
        '--onefile',  # Un singur fișier executabil
        '--windowed',  # Fără consolă (GUI)
        '--clean',  # Curăță cache
        '--noconfirm',  # Nu cere confirmare
        'main.py'
    ]
    
    # Adaugă icon dacă există
    if is_windows and os.path.exists('assets/icon.ico'):
        pyinstaller_args.insert(-1, '--icon=assets/icon.ico')
        pyinstaller_args.insert(-1, '--add-data=assets;assets')
        print("✅ Icon Windows adăugat: assets/icon.ico")
    elif not is_windows and os.path.exists('assets/icon.png'):
        pyinstaller_args.insert(-1, '--icon=assets/icon.png')
        pyinstaller_args.insert(-1, '--add-data=assets:assets')
        print("✅ Icon Linux/macOS adăugat: assets/icon.png")
    
    print(f"Platform: {sys.platform}")
    print(f"Executabil: {exe_name}")
    print(f"Comandă: {' '.join(pyinstaller_args)}")
    print()
    
    try:
        # Rulează PyInstaller
        result = subprocess.run(
            pyinstaller_args,
            check=True,
            capture_output=False
        )
        
        print()
        print("✅ Build complet!")
        print()
        print(f"📦 Executabil creat: dist/{exe_name}")
        print()
        
        # Verifică dimensiunea
        exe_path = Path('dist') / exe_name
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📊 Dimensiune: {size_mb:.1f} MB")
        
        print()
        print("🚀 Pentru a rula executabilul:")
        if is_windows:
            print("   dist\\CertificateManager.exe")
        else:
            print("   ./dist/CertificateManager")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print(f"❌ Eroare la build: {e}")
        return False
    except FileNotFoundError:
        print()
        print("❌ PyInstaller nu este instalat!")
        print()
        print("Instalați cu:")
        print("  pip install pyinstaller")
        return False


def main():
    """Funcția principală"""
    print("=" * 60)
    print("  Certificate Manager - Build Executabil")
    print("=" * 60)
    print()
    
    # Verifică că suntem în directorul corect
    if not os.path.exists('main.py'):
        print("❌ Eroare: main.py nu a fost găsit!")
        print("   Rulați acest script din directorul certificate_manager/")
        sys.exit(1)
    
    # Curăță build-uri anterioare
    clean_build_dirs()
    
    # Construiește executabilul
    success = build_executable()
    
    print()
    print("=" * 60)
    
    if success:
        print("✅ Build finalizat cu succes!")
    else:
        print("❌ Build eșuat!")
        sys.exit(1)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
