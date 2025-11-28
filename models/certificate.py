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
        """Creează un certificat dintr-un dicționar"""
        from datetime import datetime
        
        def parse_date(date_str):
            """Parse date în format DD.MM.YYYY sau YYYY-MM-DD"""
            if isinstance(date_str, date):
                return date_str
            if isinstance(date_str, str):
                # Încearcă format DD.MM.YYYY
                try:
                    return datetime.strptime(date_str, '%d.%m.%Y').date()
                except ValueError:
                    pass
                # Încearcă format YYYY-MM-DD
                try:
                    return datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
            raise ValueError(f"Format dată invalid: {date_str}")
        
        return cls(
            grad=data.get('Grad', ''),
            nume=data.get('Nume', ''),
            prenume=data.get('Prenume', ''),
            data_nasterii=parse_date(data.get('Data nașterii') or data.get('Data Nașterii')),
            serie_certificat=data.get('Serie certificat') or data.get('Serie Certificat', ''),
            numar_certificat=data.get('Număr certificat') or data.get('Număr Certificat', ''),
            nivel_certificat=data.get('Nivel certificat') or data.get('Nivel Certificat', ''),
            data_eliberare=parse_date(data.get('Data eliberare') or data.get('Data Eliberare')),
            data_expirare=parse_date(data.get('Data expirare') or data.get('Data Expirare')),
            observatii=data.get('Observații', '')
        )
    
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
