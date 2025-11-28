#!/usr/bin/env python3
"""
Manager Certificate Securitate
Aplicație pentru gestionarea certificatelor de securitate militare
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt

from models.data_manager import DataManager
from views.main_window import MainWindow
from views.alert_dialog import AlertDialog
from utils.config_manager import ConfigManager


def select_data_file(parent=None) -> str:
    """
    Permite utilizatorului să selecteze sau creeze un fișier de date
    
    Args:
        parent: Widget părinte pentru dialog
        
    Returns:
        Calea către fișierul selectat
    """
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
        return None
    elif clicked == new_btn:
        # Creează fișier nou
        file_path, _ = QFileDialog.getSaveFileName(
            parent,
            "Creați fișierul de date",
            str(Path.home() / "certificate_securitate.xlsx"),
            "Excel Files (*.xlsx)"
        )
        return file_path
    else:
        # Selectează fișier existent
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Selectați fișierul de date",
            str(Path.home()),
            "Excel Files (*.xlsx)"
        )
        return file_path


def main():
    """Funcția principală a aplicației"""
    # Creează aplicația Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Manager Certificate Securitate")
    app.setOrganizationName("MApN")
    
    # Forțează tema light (white background)
    from PyQt6.QtGui import QPalette, QColor
    
    # Creează paletă light
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
    app.setStyle("Fusion")
    
    # Încarcă configurația
    config_manager = ConfigManager()
    
    # Verifică dacă există un fișier de date configurat
    data_file_path = config_manager.get_data_file_path()
    
    if not data_file_path or not Path(data_file_path).parent.exists():
        # Prima deschidere sau cale invalidă - solicită utilizatorului să selecteze
        data_file_path = select_data_file()
        
        if not data_file_path:
            # Utilizatorul a anulat
            QMessageBox.critical(
                None,
                "Eroare",
                "Este necesar un fișier de date pentru a continua."
            )
            sys.exit(1)
        
        # Salvează calea în configurație
        config_manager.set_data_file_path(data_file_path)
    
    try:
        # Inițializează managerul de date
        data_manager = DataManager(data_file_path)
        
        # Creează și afișează fereastra principală
        window = MainWindow(data_manager)
        
        # Restaurează geometria ferestrei dacă există
        geometry = config_manager.get_window_geometry()
        if geometry:
            window.setGeometry(
                geometry['x'],
                geometry['y'],
                geometry['width'],
                geometry['height']
            )
        
        window.show()
        
        # Verifică și afișează alerte pentru certificate care expiră
        try:
            certificates = data_manager.get_all_certificates()
            AlertDialog.check_and_show_alerts(certificates, window)
        except Exception as e:
            print(f"Eroare la verificarea alertelor: {e}")
        
        # Salvează geometria la închidere
        def save_geometry():
            geom = window.geometry()
            config_manager.set_window_geometry(
                geom.x(),
                geom.y(),
                geom.width(),
                geom.height()
            )
        
        app.aboutToQuit.connect(save_geometry)
        
        # Rulează aplicația
        sys.exit(app.exec())
        
    except Exception as e:
        QMessageBox.critical(
            None,
            "Eroare Critică",
            f"Eroare la inițializarea aplicației:\n{str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
