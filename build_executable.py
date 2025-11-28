#!/usr/bin/env python3
"""
Script pentru crearea executabilului Certificate Manager
Versiune STABILĂ - fără excluderi problematice
"""
import os
import sys
import shutil
import subprocess


def clean_build_files():
    """Curăță fișierele de build anterioare"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    print("🧹 Curățare fișiere build anterioare...")
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ Șters: {dir_name}/")
    
    for pattern in files_to_clean:
        for file in os.listdir('.'):
            if file.endswith(pattern.replace('*', '')):
                os.remove(file)
                print(f"  ✓ Șters: {file}")
    
    print()


def build_executable():
    """Creează executabilul folosind PyInstaller"""
    print("=" * 70)
    print("Certificate Manager - Build Executabil")
    print("=" * 70)
    print()
    
    # Curăță fișierele vechi
    clean_build_files()
    
    # Detectează sistemul de operare
    is_windows = sys.platform.startswith('win')
    exe_name = "CertificateManager.exe" if is_windows else "CertificateManager"
    
    print(f"Platform: {sys.platform}")
    print(f"Executabil: {exe_name}")
    print()
    
    # Opțiuni PyInstaller - VERSIUNE SIGURĂ
    pyinstaller_args = [
        'pyinstaller',
        '--name=CertificateManager',
        '--onefile',  # Un singur fișier executabil
        '--windowed',  # Fără consolă (GUI)
        '--clean',  # Curăță cache
        '--noconfirm',  # Nu cere confirmare
        
        # OPTIMIZĂRI SIGURE
        '--noupx',  # NU folosi UPX (evită probleme)
        
        # EXCLUDERI SIGURE - doar module care sigur nu sunt folosite
        '--exclude-module=tkinter',  # Nu folosim tkinter
        '--exclude-module=matplotlib',  # Nu folosim matplotlib
        
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
    
    print()
    print("🔨 Pornire build PyInstaller...")
    print(f"Comandă: {' '.join(pyinstaller_args)}")
    print()
    print("-" * 70)
    
    # Rulează PyInstaller
    try:
        result = subprocess.run(pyinstaller_args, check=True)
        
        print("-" * 70)
        print()
        print("=" * 70)
        print("✅ BUILD REUȘIT!")
        print("=" * 70)
        print()
        
        # Verifică dimensiunea executabilului
        exe_path = os.path.join('dist', exe_name)
        if os.path.exists(exe_path):
            size_bytes = os.path.getsize(exe_path)
            size_mb = size_bytes / (1024 * 1024)
            print(f"📦 Executabil: {exe_path}")
            print(f"📊 Dimensiune: {size_mb:.1f} MB ({size_bytes:,} bytes)")
            print()
            print("ℹ️  Nota: PyQt6 + pandas ocupă ~250-350 MB (normal pentru aplicații GUI)")
            print("   Aceasta este dimensiunea standard pentru aplicații desktop moderne.")
        else:
            print(f"❌ Executabilul nu a fost găsit: {exe_path}")
        
        print()
        print("=" * 70)
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 70)
        print("❌ BUILD EȘUAT!")
        print("=" * 70)
        print(f"Eroare: {e}")
        print()
        print("Verificați:")
        print("1. PyInstaller este instalat: pip install pyinstaller")
        print("2. Toate dependențele sunt instalate: pip install -r requirements.txt")
        print("3. Nu există erori în cod")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Eroare neașteptată: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_executable()
