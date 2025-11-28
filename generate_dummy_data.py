#!/usr/bin/env python3
"""
Script pentru generarea datelor dummy de testare
Generează 30 de înregistrări cu diverse statusuri de expirare
"""
import sys
from pathlib import Path
from datetime import date, timedelta
import random

# Adaugă directorul curent la path
sys.path.insert(0, str(Path(__file__).parent))

from models.certificate import Certificate, GRADE_MILITARE, NIVELURI_CERTIFICATE
from models.data_manager import DataManager


# Date pentru generare
NUME_LIST = [
    "Popescu", "Ionescu", "Georgescu", "Vasilescu", "Marinescu",
    "Constantinescu", "Stanescu", "Dumitru", "Mihai", "Popa",
    "Radu", "Stoica", "Munteanu", "Diaconu", "Barbu",
    "Cristea", "Moldovan", "Nistor", "Florea", "Tudor",
    "Luca", "Stanciu", "Ilie", "Apostol", "Matei",
    "Andrei", "Nicolae", "Stefan", "Pavel", "Gheorghe"
]

PRENUME_LIST = [
    "Ion", "Maria", "Andrei", "Elena", "Cristian",
    "Alexandra", "Mihai", "Ana", "George", "Ioana",
    "Alexandru", "Daniela", "Florin", "Simona", "Adrian",
    "Monica", "Bogdan", "Gabriela", "Marius", "Raluca",
    "Catalin", "Laura", "Ionut", "Carmen", "Vlad",
    "Diana", "Razvan", "Alina", "Stefan", "Andreea"
]


def generate_dummy_certificates(count: int = 30) -> list[Certificate]:
    """
    Generează certificate dummy pentru testare
    
    Args:
        count: Numărul de certificate de generat
        
    Returns:
        Lista de certificate
    """
    certificates = []
    today = date.today()
    
    # Distribuție statusuri:
    # - 40% normale (> 3 luni)
    # - 25% atenție (1-3 luni)
    # - 20% urgente (< 1 lună)
    # - 15% expirate
    
    status_distribution = (
        ['normal'] * 12 +
        ['atentie'] * 8 +
        ['urgent'] * 6 +
        ['expirat'] * 4
    )
    
    random.shuffle(status_distribution)
    
    for i in range(count):
        # Date personale
        nume = NUME_LIST[i % len(NUME_LIST)]
        prenume = PRENUME_LIST[i % len(PRENUME_LIST)]
        
        # Vârstă între 25-55 ani
        varsta = random.randint(25, 55)
        data_nasterii = today - timedelta(days=varsta * 365 + random.randint(0, 365))
        
        # Grad aleator
        grad = random.choice(GRADE_MILITARE)
        
        # Serie și număr certificat
        serie = random.choice(['AB', 'CD', 'EF', 'GH', 'IJ', 'KL', 'MN', 'OP', 'QR', 'ST'])
        numar = f"{random.randint(100000, 999999)}"
        
        # Nivel certificat
        nivel = random.choice(NIVELURI_CERTIFICATE)
        
        # Date eliberare (între 1-5 ani în urmă)
        zile_eliberare = random.randint(365, 1825)
        data_eliberare = today - timedelta(days=zile_eliberare)
        
        # Data expirare bazată pe status
        status = status_distribution[i]
        
        if status == 'normal':
            # Între 91 și 730 zile (3 luni - 2 ani)
            zile_expirare = random.randint(91, 730)
        elif status == 'atentie':
            # Între 31 și 90 zile (1-3 luni)
            zile_expirare = random.randint(31, 90)
        elif status == 'urgent':
            # Între 1 și 30 zile
            zile_expirare = random.randint(1, 30)
        else:  # expirat
            # Între -180 și -1 zile (expirat în ultimele 6 luni)
            zile_expirare = random.randint(-180, -1)
        
        data_expirare = today + timedelta(days=zile_expirare)
        
        # Observații
        observatii_options = [
            "",
            "Reînnoire în curs",
            "Verificat",
            "Contact: 0721234567",
            "Nivel actualizat",
            "Documentație completă",
            ""
        ]
        observatii = random.choice(observatii_options)
        
        # Creează certificatul
        cert = Certificate(
            grad=grad,
            nume=nume,
            prenume=prenume,
            data_nasterii=data_nasterii,
            serie_certificat=serie,
            numar_certificat=numar,
            nivel_certificat=nivel,
            data_eliberare=data_eliberare,
            data_expirare=data_expirare,
            observatii=observatii
        )
        
        certificates.append(cert)
    
    return certificates


def main():
    """Funcția principală"""
    print("╔════════════════════════════════════════════════╗")
    print("║  Generare Date Dummy - Certificate            ║")
    print("╚════════════════════════════════════════════════╝")
    print()
    
    # Calea către fișierul de output
    output_file = Path(__file__).parent / "date_dummy_30_certificate.xlsx"
    
    print(f"Generare 30 certificate dummy...")
    certificates = generate_dummy_certificates(30)
    
    print(f"Certificate generate: {len(certificates)}")
    print()
    
    # Statistici
    today = date.today()
    normale = sum(1 for c in certificates if c.zile_pana_la_expirare() > 90)
    atentie = sum(1 for c in certificates if 30 < c.zile_pana_la_expirare() <= 90)
    urgente = sum(1 for c in certificates if 0 < c.zile_pana_la_expirare() <= 30)
    expirate = sum(1 for c in certificates if c.zile_pana_la_expirare() < 0)
    
    print("Distribuție statusuri:")
    print(f"  ⬜ Normale (> 3 luni):     {normale:2d} certificate")
    print(f"  🟨 Atenție (1-3 luni):     {atentie:2d} certificate")
    print(f"  🟥 Urgente (< 1 lună):     {urgente:2d} certificate")
    print(f"  🟥 Expirate:               {expirate:2d} certificate")
    print()
    
    # Creează fișierul
    print(f"Creare fișier: {output_file}")
    
    try:
        # Șterge fișierul dacă există
        if output_file.exists():
            output_file.unlink()
        
        # Creează DataManager și adaugă certificatele
        dm = DataManager(str(output_file))
        
        for cert in certificates:
            dm.add_certificate(cert)
        
        print(f"✓ Fișier creat cu succes!")
        print(f"✓ Locație: {output_file}")
        print()
        
        # Afișează câteva exemple
        print("Exemple certificate generate:")
        print("-" * 80)
        for i, cert in enumerate(certificates[:5], 1):
            zile = cert.zile_pana_la_expirare()
            status = "EXPIRAT" if zile < 0 else f"{zile} zile"
            print(f"{i}. {cert.grad} {cert.nume} {cert.prenume}")
            print(f"   Certificat: {cert.serie_certificat}-{cert.numar_certificat} ({cert.nivel_certificat})")
            print(f"   Expirare: {cert.data_expirare.strftime('%d.%m.%Y')} - {status}")
            print()
        
        print("..." + " (și încă 25 certificate)" if len(certificates) > 5 else "")
        print()
        print("╔════════════════════════════════════════════════╗")
        print("║  Generare Completă!                            ║")
        print("╚════════════════════════════════════════════════╝")
        print()
        print("Puteți importa acest fișier în aplicație sau")
        print("îl puteți folosi ca sursă de date la pornire.")
        
    except Exception as e:
        print(f"✗ Eroare la crearea fișierului: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
