"""
Model de date pentru certificatele de securitate
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional


# Nomenclator grade militare România
GRADE_MILITARE = [
    "Soldat",
    "Caporal",
    "Sergent",
    "Sergent Major",
    "Plutonier Adjutant",
    "Plutonier",
    "Plutonier Adjutant Principal",
    "Plutonier Major",
    "Sublocotenent",
    "Locotenent",
    "Căpitan",
    "Major",
    "Locotenent Colonel",
    "Colonel",
    "General de Brigadă",
    "General de Divizie",
    "General",
    "General de Armată"
]

# Niveluri certificate
NIVELURI_CERTIFICATE = ["SSv", "S", "SS", "SSID"]


@dataclass
class Certificate:
    """Clasa pentru reprezentarea unui certificat de securitate"""
    grad: str
    nume: str
    prenume: str
    data_nasterii: date
    serie_certificat: str
    numar_certificat: str
    nivel_certificat: str
    data_eliberare: date
    data_expirare: date
    observatii: Optional[str] = ""
    
    def __post_init__(self):
        """Validare date după inițializare"""
        if self.grad not in GRADE_MILITARE:
            raise ValueError(f"Grad invalid: {self.grad}")
        
        if self.nivel_certificat not in NIVELURI_CERTIFICATE:
            raise ValueError(f"Nivel certificat invalid: {self.nivel_certificat}")
        
        if not isinstance(self.data_nasterii, date):
            raise ValueError("Data nașterii trebuie să fie de tip date")
        
        if not isinstance(self.data_eliberare, date):
            raise ValueError("Data eliberare trebuie să fie de tip date")
        
        if not isinstance(self.data_expirare, date):
            raise ValueError("Data expirare trebuie să fie de tip date")
        
        if self.data_expirare <= self.data_eliberare:
            raise ValueError("Data expirare trebuie să fie după data eliberare")
    
    def to_dict(self):
        """Convertește certificatul într-un dicționar"""
        return {
            'Grad': self.grad,
            'Nume': self.nume,
            'Prenume': self.prenume,
            'Data nașterii': self.data_nasterii.strftime('%d.%m.%Y'),
            'Serie certificat': self.serie_certificat,
            'Număr certificat': self.numar_certificat,
            'Nivel certificat': self.nivel_certificat,
            'Data eliberare': self.data_eliberare.strftime('%d.%m.%Y'),
            'Data expirare': self.data_expirare.strftime('%d.%m.%Y'),
            'Observații': self.observatii or ''
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Crează un certificat dintr-un dicționar"""
        from datetime import datetime
        import pandas as pd
        
        # Verifică dacă data este un dicționar valid
        if not isinstance(data, dict):
            raise TypeError(f"Expected dict, got {type(data).__name__}")
        
        def parse_date(date_value):
            """Parse date în format DD.MM.YYYY sau YYYY-MM-DD"""
            # Verifică None sau NaN
            if date_value is None or (isinstance(date_value, float) and pd.isna(date_value)):
                raise ValueError("Data lipsă sau invalidă")
            
            if isinstance(date_value, date):
                return date_value
            
            if isinstance(date_value, str):
                date_value = date_value.strip()
                if not date_value:
                    raise ValueError("Data goală")
                
                # Încearca format DD.MM.YYYY
                try:
                    return datetime.strptime(date_value, '%d.%m.%Y').date()
                except ValueError:
                    pass
                # Încearca format YYYY-MM-DD
                try:
                    return datetime.strptime(date_value, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            raise ValueError(f"Format dată invalid: {date_value} (tip: {type(date_value).__name__})")
        
        def get_value(key1, key2='', default=''):
            """Obține valoare cu fallback pentru chei multiple"""
            value = data.get(key1)
            if value is None or (isinstance(value, float) and pd.isna(value)):
                if key2:
                    value = data.get(key2)
                    if value is None or (isinstance(value, float) and pd.isna(value)):
                        return default
                else:
                    return default
            return str(value) if value != default else default
        
        try:
            return cls(
                grad=get_value('Grad'),
                nume=get_value('Nume'),
                prenume=get_value('Prenume'),
                data_nasterii=parse_date(data.get('Data nașterii') or data.get('Data Nașterii')),
                serie_certificat=get_value('Serie certificat', 'Serie Certificat'),
                numar_certificat=get_value('Număr certificat', 'Număr Certificat'),
                nivel_certificat=get_value('Nivel certificat', 'Nivel Certificat'),
                data_eliberare=parse_date(data.get('Data eliberare') or data.get('Data Eliberare')),
                data_expirare=parse_date(data.get('Data expirare') or data.get('Data Expirare')),
                observatii=get_value('Observații')
            )
        except Exception as e:
            raise ValueError(f"Eroare la parsarea certificatului: {e}. Date: {data}")
    
    def zile_pana_la_expirare(self) -> int:
        """Calculează numărul de zile până la expirare"""
        from datetime import datetime
        today = datetime.now().date()
        return (self.data_expirare - today).days
    
    def get_status_color(self) -> str:
        """Returnează codul de culoare bazat pe statusul expirării"""
        zile = self.zile_pana_la_expirare()
        
        if zile < 0:
            return "#8B0000"  # Roșu închis - expirat
        elif zile <= 30:
            return "#FFB6C1"  # Roșu deschis - 1 lună
        elif zile <= 90:
            return "#FFFF99"  # Galben - 3 luni
        else:
            return "#FFFFFF"  # Alb - normal


# Coloanele tabelului în ordinea dorită
COLUMN_NAMES = [
    'Grad',
    'Nume',
    'Prenume',
    'Data nașterii',
    'Serie certificat',
    'Număr certificat',
    'Nivel certificat',
    'Data eliberare',
    'Data expirare',
    'Observații'
]
