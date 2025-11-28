#!/usr/bin/env python3
"""
Script pentru crearea executabilului Certificate Manager
OPTIMIZAT MAXIM pentru dimensiune minimă
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
    """Creează executabilul folosind PyInstaller cu optimizări MAXIME"""
    print("=" * 70)
    print("Certificate Manager - Build Executabil OPTIMIZAT MAXIM")
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
    
    # Opțiuni PyInstaller - OPTIMIZARE MAXIMĂ
    pyinstaller_args = [
        'pyinstaller',
        '--name=CertificateManager',
        '--onefile',  # Un singur fișier executabil
        '--windowed',  # Fără consolă (GUI)
        '--clean',  # Curăță cache
        '--noconfirm',  # Nu cere confirmare
        
        # OPTIMIZĂRI DIMENSIUNE
        '--noupx',  # NU folosi UPX
        
        # EXCLUDERI MAXIME - Module care NU sunt folosite
        # GUI frameworks (nu folosim)
        '--exclude-module=tkinter',
        '--exclude-module=_tkinter',
        
        # Plotting/Visualization (nu folosim)
        '--exclude-module=matplotlib',
        '--exclude-module=plotly',
        '--exclude-module=seaborn',
        '--exclude-module=bokeh',
        
        # Scientific computing (pandas le include dar nu le folosim)
        '--exclude-module=scipy',
        '--exclude-module=sklearn',
        '--exclude-module=scikit-learn',
        '--exclude-module=statsmodels',
        
        # Image processing (nu folosim)
        '--exclude-module=PIL',
        '--exclude-module=Pillow',
        '--exclude-module=cv2',
        '--exclude-module=skimage',
        
        # Development tools (nu sunt necesare în executabil)
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        '--exclude-module=notebook',
        '--exclude-module=nbconvert',
        '--exclude-module=pytest',
        '--exclude-module=unittest',
        '--exclude-module=test',
        '--exclude-module=tests',
        
        # Pandas optional dependencies (nu le folosim)
        '--exclude-module=tables',
        '--exclude-module=pytables',
        '--exclude-module=xlrd',
        '--exclude-module=xlwt',
        '--exclude-module=xlsxwriter',
        '--exclude-module=pyarrow',
        '--exclude-module=fastparquet',
        '--exclude-module=sqlalchemy',
        '--exclude-module=psycopg2',
        '--exclude-module=pymysql',
        
        # Numpy optional (reducere dimensiune)
        '--exclude-module=numpy.distutils',
        '--exclude-module=numpy.f2py',
        '--exclude-module=numpy.testing',
        
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
    print(f"Comandă: {' '.join(pyinstaller_args[:10])}... ({len(pyinstaller_args)} argumente)")
    print()
    print("-" * 70)
    
    # Rulează PyInstaller
    try:
        result = subprocess.run(pyinstaller_args, check=True, capture_output=True, text=True)
        
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
            
            if size_mb < 150:
                print("✅ EXCELENT! Dimensiune optimă (< 150 MB)")
            elif size_mb < 250:
                print("✅ BUN! Dimensiune acceptabilă (< 250 MB)")
            else:
                print("⚠️  Dimensiune mare (> 250 MB)")
                print("   PyQt6 + pandas + numpy ocupă majoritatea spațiului")
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
        if e.stderr:
            print("STDERR:")
            print(e.stderr[-2000:])  # Ultimele 2000 caractere
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
