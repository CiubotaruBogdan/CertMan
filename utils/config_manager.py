"""
Manager pentru configurația aplicației
"""
import json
from pathlib import Path
from typing import Optional


class ConfigManager:
    """Gestionează configurația aplicației"""
    
    CONFIG_FILE = "config.json"
    
    def __init__(self):
        """Inițializează managerul de configurare"""
        self.config_path = Path.home() / ".certificate_manager" / self.CONFIG_FILE
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """
        Încarcă configurația din fișier
        
        Returns:
            Dicționar cu configurația
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Eroare la încărcarea configurației: {e}")
                return {}
        return {}
    
    def _save_config(self):
        """Salvează configurația în fișier"""
        # Asigură că directorul există
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Eroare la salvarea configurației: {e}")
    
    def get_data_file_path(self) -> Optional[str]:
        """
        Returnează calea către fișierul de date
        
        Returns:
            Calea către fișier sau None
        """
        return self.config.get('data_file_path')
    
    def set_data_file_path(self, path: str):
        """
        Setează calea către fișierul de date
        
        Args:
            path: Calea către fișier
        """
        self.config['data_file_path'] = path
        self._save_config()
    
    def get_visible_columns(self) -> Optional[list]:
        """
        Returnează lista coloanelor vizibile
        
        Returns:
            Lista cu numele coloanelor sau None
        """
        return self.config.get('visible_columns')
    
    def set_visible_columns(self, columns: list):
        """
        Setează coloanele vizibile
        
        Args:
            columns: Lista cu numele coloanelor
        """
        self.config['visible_columns'] = columns
        self._save_config()
    
    def get_window_geometry(self) -> Optional[dict]:
        """
        Returnează geometria ferestrei
        
        Returns:
            Dicționar cu x, y, width, height sau None
        """
        return self.config.get('window_geometry')
    
    def set_window_geometry(self, x: int, y: int, width: int, height: int):
        """
        Setează geometria ferestrei
        
        Args:
            x: Coordonata X
            y: Coordonata Y
            width: Lățimea
            height: Înălțimea
        """
        self.config['window_geometry'] = {
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }
        self._save_config()
