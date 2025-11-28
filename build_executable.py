#!/usr/bin/env python3
"""
Script pentru crearea executabilului cu PyInstaller
Creează .exe pe Windows, executabil pe Linux/macOS
"""
import subprocess
import sys
import shutil
import platform
from pathlib import Path


def main():
    """Funcția principală de build"""
    print("╔════════════════════════════════════════════════╗")
    print("║  Build Executabil - Certificate Manager       ║")
    print("╚════════════════════════════════════════════════╝")
    print()
    
    # Verifică că PyInstaller este instalat
    try:
        import PyInstaller
        print(f"✓ PyInstaller versiune: {PyInstaller.__version__}")
    except ImportError:
        print("✗ PyInstaller nu este instalat!")
        print()
        print("Instalare:")
        print("  pip install pyinstaller")
        print("  sau")
        print("  pip3 install pyinstaller")
        return 1
    
    print(f"✓ Python versiune: {sys.version.split()[0]}")
    print(f"✓ Platformă: {platform.system()} {platform.machine()}")
    print()
    
    # Directorul curent
    project_dir = Path(__file__).parent
    print(f"Director proiect: {project_dir}")
    print()
    
    # Curăță directoarele de build anterioare
    print("Curățare directoare build anterioare...")
    for dir_name in ['build', 'dist', '__pycache__']:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            print(f"  Ștergere: {dir_name}/")
            shutil.rmtree(dir_path)
    
    # Curăță cache Python în subdirectoare
    for subdir in ['models', 'views', 'controllers', 'utils']:
        cache_dir = project_dir / subdir / '__pycache__'
        if cache_dir.exists():
            print(f"  Ștergere: {subdir}/__pycache__/")
            shutil.rmtree(cache_dir)
    
    # Șterge fișiere .spec vechi
    for spec_file in project_dir.glob('*.spec'):
        print(f"  Ștergere: {spec_file.name}")
        spec_file.unlink()
    
    print("✓ Curățare completă")
    print()
    
    # Determină numele executabilului bazat pe platformă
    if platform.system() == 'Windows':
        exe_name = 'CertificateManager.exe'
        print("📦 Construire executabil pentru Windows (.exe)")
    else:
        exe_name = 'CertificateManager'
        print(f"📦 Construire executabil pentru {platform.system()}")
    
    print()
    print("═" * 60)
    print("Construire executabil cu PyInstaller...")
    print("Acest proces poate dura câteva minute...")
    print("═" * 60)
    print()
    
    # Comandă PyInstaller
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--clean',
        '--onefile',
        '--windowed',
        '--name=CertificateManager',
        # Hidden imports pentru dependențe
        '--hidden-import=openpyxl',
        '--hidden-import=openpyxl.cell',
        '--hidden-import=openpyxl.cell._writer',
        '--hidden-import=pandas',
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        'main.py'
    ]
    
    try:
        # Rulează PyInstaller
        result = subprocess.run(
            cmd, 
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Afișează output-ul
        for line in result.stdout.split('\n'):
            if any(keyword in line for keyword in ['INFO:', 'WARNING:', 'ERROR:', 'Building', 'completed']):
                print(line)
        
        if result.returncode != 0:
            print()
            print("✗ Build eșuat!")
            print("Output complet:")
            print(result.stdout)
            return 1
        
        print()
        print("═" * 60)
        print("✓ Build completat cu succes!")
        print("═" * 60)
        print()
        
        # Verifică executabilul
        dist_dir = project_dir / 'dist'
        exe_path = dist_dir / exe_name
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✓ Executabil creat: {exe_path}")
            print(f"✓ Dimensiune: {size_mb:.2f} MB")
            print()
            
            # Instrucțiuni
            print("╔════════════════════════════════════════════════╗")
            print("║  Executabil Gata de Distribuire               ║")
            print("╚════════════════════════════════════════════════╝")
            print()
            print(f"Locație: {dist_dir}/")
            print(f"Fișier: {exe_name}")
            print()
            
            if platform.system() == 'Windows':
                print("Utilizare Windows:")
                print(f"  - Dublu-click pe {exe_name}")
                print("  - Sau rulați din Command Prompt")
            else:
                print(f"Utilizare {platform.system()}:")
                print(f"  chmod +x {exe_name}")
                print(f"  ./{exe_name}")
            
            print()
            print("Caracteristici:")
            print("  ✓ Standalone (nu necesită Python)")
            print("  ✓ Include toate dependențele")
            print("  ✓ Gata de distribuire")
            print("  ✓ Fără instalare necesară")
            print()
            
            # Curăță fișierele temporare după build
            print("Curățare fișiere temporare build...")
            build_dir = project_dir / 'build'
            if build_dir.exists():
                shutil.rmtree(build_dir)
                print("  ✓ Șters folder build/")
            
            for spec_file in project_dir.glob('*.spec'):
                spec_file.unlink()
                print(f"  ✓ Șters {spec_file.name}")
            
            print()
            print("✅ Build finalizat și curățat!")
            
            return 0
        else:
            print("✗ Executabilul nu a fost găsit!")
            print(f"  Așteptat: {exe_path}")
            return 1
            
    except subprocess.CalledProcessError as e:
        print()
        print("✗ Eroare la construirea executabilului!")
        print(f"  Cod eroare: {e.returncode}")
        if e.output:
            print("  Output:")
            print(e.output)
        return 1
    except Exception as e:
        print()
        print(f"✗ Eroare neașteptată: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
