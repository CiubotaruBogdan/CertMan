#!/usr/bin/env python3
"""
Generator de date dummy pentru testarea aplicației
Generează 30 înregistrări cu diverse statusuri de expirare
"""
import random
from datetime import datetime, timedelta
import pandas as pd
from models.certificate import GRADE_MILITARE, NIVELURI_CERTIFICATE


def generate_dummy_data(num_records=30, output_file="date_dummy_30_certificate.xlsx"):
    """
    Generează date dummy pentru testare
    
    Args:
        num_records: Număr de înregistrări de generat
        output_file: Fișier de output
    """
    
    # Liste pentru generare date
    nume_list = [
        "Popescu", "Ionescu", "Popa", "Dumitrescu", "Stan", "Gheorghe",
        "Marin", "Radu", "Stoica", "Barbu", "Dima", "Constantinescu",
        "Rusu", "Mocanu", "Dobre", "Vasile", "Preda", "Lungu",
        "Cristea", "Mihai", "Tudor", "Andrei", "Matei", "Florea",
        "Ilie", "Stanciu", "Ștefan", "Enache", "Georgescu", "Nistor"
    ]
    
    prenume_list = [
        "Ion", "Gheorghe", "Vasile", "Nicolae", "Constantin", "Mihai",
        "Alexandru", "Andrei", "Cristian", "Marius", "Adrian", "Florin",
        "Daniel", "Gabriel", "Ionuț", "Bogdan", "Răzvan", "Ștefan",
        "Vlad", "Cosmin", "Dragoș", "Ciprian", "Sorin", "Lucian",
        "Cătălin", "Valentin", "Emil", "Radu", "Octavian", "Liviu"
    ]
    
    # Generează date
    data = []
    today = datetime.now()
    
    # Distribuție statusuri:
    # 12 normale (> 3 luni)
    # 8 atenție (1-3 luni)
    # 6 urgente (< 1 lună)
    # 4 expirate
    
    status_distribution = (
        ['normal'] * 12 +
        ['atentie'] * 8 +
        ['urgent'] * 6 +
        ['expirat'] * 4
    )
    random.shuffle(status_distribution)
    
    for i in range(num_records):
        # Date personale
        nume = random.choice(nume_list)
        prenume = random.choice(prenume_list)
        
        # Data nașterii (între 30 și 55 ani)
        varsta = random.randint(30, 55)
        data_nasterii = today - timedelta(days=varsta * 365 + random.randint(0, 364))
        
        # Grad militar
        grad = random.choice(GRADE_MILITARE)
        
        # Serie și număr certificat
        serie = f"{random.choice(['AB', 'CD', 'EF', 'GH', 'IJ'])}-{random.randint(100000, 999999)}"
        numar = random.randint(100000, 999999)
        
        # Nivel certificat
        nivel = random.choice(NIVELURI_CERTIFICATE)
        
        # Data eliberare (între 1 și 10 ani în urmă)
        zile_eliberare = random.randint(365, 3650)
        data_eliberare = today - timedelta(days=zile_eliberare)
        
        # Data expirare bazată pe status
        status = status_distribution[i]
        
        if status == 'normal':
            # Mai mult de 3 luni (90-730 zile)
            zile_expirare = random.randint(91, 730)
            data_expirare = today + timedelta(days=zile_expirare)
        elif status == 'atentie':
            # 1-3 luni (30-89 zile)
            zile_expirare = random.randint(30, 89)
            data_expirare = today + timedelta(days=zile_expirare)
        elif status == 'urgent':
            # Mai puțin de 1 lună (1-29 zile)
            zile_expirare = random.randint(1, 29)
            data_expirare = today + timedelta(days=zile_expirare)
        else:  # expirat
            # Expirat (1-180 zile în urmă)
            zile_expirare = random.randint(1, 180)
            data_expirare = today - timedelta(days=zile_expirare)
        
        # Observații (opțional)
        observatii_options = [
            "",
            "",
            "",  # Majoritatea fără observații
            "Reînnoire în curs",
            "Verificat",
            "Contact: 0721234567",
            "Delegat în străinătate",
            "În concediu medical",
            "Transfer în curs"
        ]
        observatii = random.choice(observatii_options)
        
        # Adaugă înregistrarea
        data.append({
            'Grad': grad,
            'Nume': nume,
            'Prenume': prenume,
            'Data nașterii': data_nasterii.strftime('%d.%m.%Y'),
            'Serie certificat': serie,
            'Număr certificat': str(numar),
            'Nivel certificat': nivel,
            'Data eliberare': data_eliberare.strftime('%d.%m.%Y'),
            'Data expirare': data_expirare.strftime('%d.%m.%Y'),
            'Observații': observatii
        })
    
    # Creează DataFrame și salvează
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"✓ Generat {num_records} înregistrări în {output_file}")
    print(f"\nDistribuție statusuri:")
    print(f"  - Normale (> 3 luni): 12")
    print(f"  - Atenție (1-3 luni): 8")
    print(f"  - Urgente (< 1 lună): 6")
    print(f"  - Expirate: 4")
    print(f"\nTotal: {num_records} înregistrări")


if __name__ == "__main__":
    generate_dummy_data()
