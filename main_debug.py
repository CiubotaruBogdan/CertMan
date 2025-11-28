"""
Manager Certificate Securitate - VERSIUNE DEBUG
Aplicație pentru gestionarea certificatelor de securitate militare
"""
import sys
import traceback
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

def debug_print(message):
    """Print pentru debugging"""
    print(f"[DEBUG] {message}")
    sys.stdout.flush()

try:
    debug_print("Importare module...")
    from models.data_manager import DataManager
    from views.main_window import MainWindow
    from views.alert_dialog import AlertDialog
    from utils.config_manager import ConfigManager
    debug_print("✓ Module importate cu succes")
except Exception as e:
    print(f"[EROARE] La importare module: {e}")
    traceback.print_exc()
    sys.exit(1)


def select_data_file(parent=None) -> str:
    """
    Permite utilizatorului să selecteze sau creeze un fișier de date
    
    Args:
        parent: Widget părinte pentru dialog
        
    Returns:
        Calea către fișierul selectat
    """
    debug_print("Afișare dialog selectare fișier...")
    msg = QMessageBox(parent)
    msg.setWindowTitle("Selectare Fișier Date")
    msg.setText("Selectați fișierul Excel pentru stocarea datelor.")
    msg.setInformativeText("Puteți selecta un fișier existent sau crea unul nou.")
    msg.setIcon(QMessageBox.Icon.Information)
    
    # Butoane personalizate
    new_btn = msg.addButton("Fișier Nou", QMessageBox.ButtonRole.AcceptRole)
    existing_btn = msg.addButton("Fișier Existent", QMessageBox.ButtonRole.AcceptRole)
    cancel_btn = msg.addButton("Anulare", QMessageBox.ButtonRole.RejectRole)
    
    msg.exec()
    clicked = msg.clickedButton()
    
    if clicked == cancel_btn:
        debug_print("Utilizator a anulat")
        return None
    elif clicked == new_btn:
        debug_print("Utilizator selectează fișier nou...")
        # Creează fișier nou
        file_path, _ = QFileDialog.getSaveFileName(
            parent,
            "Creați fișierul de date",
            str(Path.home() / "certificate_securitate.xlsx"),
            "Excel Files (*.xlsx)"
        )
        debug_print(f"Fișier nou selectat: {file_path}")
        return file_path
    else:
        debug_print("Utilizator selectează fișier existent...")
        # Selectează fișier existent
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Selectați fișierul de date",
            str(Path.home()),
            "Excel Files (*.xlsx)"
        )
        debug_print(f"Fișier existent selectat: {file_path}")
        return file_path


def main():
    """Funcția principală"""
    debug_print("=== PORNIRE APLICAȚIE ===")
    
    try:
        debug_print("Creare QApplication...")
        app = QApplication(sys.argv)
        debug_print("✓ QApplication creat")
        
        # Forțează tema light (white background)
        debug_print("Setare temă light...")
        light_palette = QPalette()
        light_palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))
        light_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
        light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        app.setPalette(light_palette)
        debug_print("✓ Temă light setată")
        
        # Încarcă configurația
        debug_print("Încărcare configurație...")
        config_manager = ConfigManager()
        debug_print("✓ ConfigManager creat")
        
        # Verifică dacă există un fișier de date configurat
        debug_print("Verificare fișier de date configurat...")
        data_file_path = config_manager.get_data_file_path()
        debug_print(f"Fișier configurat: {data_file_path}")
        
        if not data_file_path or not Path(data_file_path).parent.exists():
            debug_print("Fișier lipsă sau cale invalidă - solicită utilizatorului")
            # Prima deschidere sau cale invalidă - solicită utilizatorului să selecteze
            data_file_path = select_data_file()
            
            if not data_file_path:
                debug_print("Utilizator a anulat - închidere aplicație")
                # Utilizatorul a anulat
                QMessageBox.critical(
                    None,
                    "Eroare",
                    "Este necesar un fișier de date pentru a continua."
                )
                sys.exit(1)
            
            # Salvează calea în configurație
            debug_print(f"Salvare cale în configurație: {data_file_path}")
            config_manager.set_data_file_path(data_file_path)
        
        try:
            # Inițializează managerul de date
            debug_print(f"Inițializare DataManager cu: {data_file_path}")
            data_manager = DataManager(data_file_path)
            debug_print("✓ DataManager creat")
            
            # Încarcă certificate pentru verificare
            debug_print("Încărcare certificate pentru verificare...")
            certificates = data_manager.get_all_certificates()
            debug_print(f"✓ Certificate încărcate: {len(certificates)}")
            
            # Creează și afișează fereastra principală
            debug_print("Creare MainWindow...")
            window = MainWindow(data_manager)
            debug_print("✓ MainWindow creat")
            
            # Restaurează geometria ferestrei dacă există
            debug_print("Restaurare geometrie fereastră...")
            geometry = config_manager.get_window_geometry()
            if geometry:
                window.setGeometry(
                    geometry['x'],
                    geometry['y'],
                    geometry['width'],
                    geometry['height']
                )
                debug_print("✓ Geometrie restaurată")
            
            debug_print("Afișare fereastră...")
            window.show()
            debug_print("✓ Fereastră afișată")
            
            # Verifică și afișează alerte pentru certificate care expiră
            try:
                debug_print("Verificare alerte certificate...")
                AlertDialog.check_and_show_alerts(certificates, window)
                debug_print("✓ Alerte verificate")
            except Exception as e:
                debug_print(f"⚠ Eroare la verificarea alertelor: {e}")
                traceback.print_exc()
            
            # Salvează geometria la închidere
            def save_geometry():
                debug_print("Salvare geometrie la închidere...")
                geom = window.geometry()
                config_manager.set_window_geometry(
                    geom.x(),
                    geom.y(),
                    geom.width(),
                    geom.height()
                )
                debug_print("✓ Geometrie salvată")
            
            app.aboutToQuit.connect(save_geometry)
            
            debug_print("=== APLICAȚIE PORNITĂ CU SUCCES ===")
            debug_print("Intrare în event loop...")
            sys.exit(app.exec())
            
        except Exception as e:
            debug_print(f"✗ EROARE CRITICĂ la inițializare aplicație: {e}")
            traceback.print_exc()
            QMessageBox.critical(
                None,
                "Eroare Critică",
                f"Eroare la inițializarea aplicației:\n{str(e)}\n\nVerificați fișierul de date."
            )
            sys.exit(1)
            
    except Exception as e:
        debug_print(f"✗ EROARE FATALĂ: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
