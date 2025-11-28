"""
Script de testare pentru aplicația Manager Certificate Securitate
"""
import sys
from datetime import date, timedelta
from pathlib import Path

# Adaugă directorul curent la path
sys.path.insert(0, str(Path(__file__).parent))

from models.certificate import Certificate, GRADE_MILITARE, NIVELURI_CERTIFICATE
from models.data_manager import DataManager


def test_certificate_model():
    """Testează modelul Certificate"""
    print("=== Test Model Certificate ===")
    
    try:
        # Creează un certificat valid
        cert = Certificate(
            grad="Căpitan",
            nume="Popescu",
            prenume="Ion",
            data_nasterii=date(1985, 5, 15),
            serie_certificat="AB",
            numar_certificat="123456",
            nivel_certificat="S",
            data_eliberare=date(2020, 1, 1),
            data_expirare=date(2025, 1, 1),
            observatii="Test"
        )
        
        print(f"✓ Certificat creat: {cert.nume} {cert.prenume}")
        print(f"  Zile până la expirare: {cert.zile_pana_la_expirare()}")
        print(f"  Culoare status: {cert.get_status_color()}")
        
        # Test conversie to_dict
        cert_dict = cert.to_dict()
        print(f"✓ Conversie to_dict: {len(cert_dict)} câmpuri")
        
        # Test conversie from_dict
        cert2 = Certificate.from_dict(cert_dict)
        print(f"✓ Conversie from_dict: {cert2.nume} {cert2.prenume}")
        
    except Exception as e:
        print(f"✗ Eroare la testarea modelului: {e}")
        return False
    
    print()
    return True


def test_data_manager():
    """Testează DataManager"""
    print("=== Test Data Manager ===")
    
    test_file = "/tmp/test_certificates.xlsx"
    
    try:
        # Șterge fișierul de test dacă există
        if Path(test_file).exists():
            Path(test_file).unlink()
        
        # Creează manager
        dm = DataManager(test_file)
        print(f"✓ DataManager creat cu fișier: {test_file}")
        
        # Verifică că fișierul a fost creat
        if Path(test_file).exists():
            print("✓ Fișier Excel creat automat")
        
        # Adaugă certificate de test
        today = date.today()
        
        # Certificat normal (valid mult timp)
        cert1 = Certificate(
            grad="Major",
            nume="Ionescu",
            prenume="Maria",
            data_nasterii=date(1980, 3, 10),
            serie_certificat="CD",
            numar_certificat="789012",
            nivel_certificat="SS",
            data_eliberare=today - timedelta(days=365),
            data_expirare=today + timedelta(days=365),
            observatii="Certificat normal"
        )
        dm.add_certificate(cert1)
        print("✓ Certificat normal adăugat")
        
        # Certificat cu avertizare (3 luni)
        cert2 = Certificate(
            grad="Locotenent",
            nume="Georgescu",
            prenume="Andrei",
            data_nasterii=date(1990, 7, 20),
            serie_certificat="EF",
            numar_certificat="345678",
            nivel_certificat="S",
            data_eliberare=today - timedelta(days=730),
            data_expirare=today + timedelta(days=60),  # 2 luni
            observatii="Expirare în 2 luni - GALBEN"
        )
        dm.add_certificate(cert2)
        print("✓ Certificat cu avertizare (galben) adăugat")
        
        # Certificat urgent (1 lună)
        cert3 = Certificate(
            grad="Sergent",
            nume="Vasilescu",
            prenume="Cristian",
            data_nasterii=date(1995, 11, 5),
            serie_certificat="GH",
            numar_certificat="901234",
            nivel_certificat="SSv",
            data_eliberare=today - timedelta(days=1095),
            data_expirare=today + timedelta(days=20),  # 20 zile
            observatii="Expirare în 20 zile - ROȘU DESCHIS"
        )
        dm.add_certificate(cert3)
        print("✓ Certificat urgent (roșu deschis) adăugat")
        
        # Certificat expirat
        cert4 = Certificate(
            grad="Plutonier",
            nume="Marinescu",
            prenume="Elena",
            data_nasterii=date(1988, 2, 14),
            serie_certificat="IJ",
            numar_certificat="567890",
            nivel_certificat="SSID",
            data_eliberare=today - timedelta(days=1460),
            data_expirare=today - timedelta(days=10),  # Expirat
            observatii="EXPIRAT - ROȘU ÎNCHIS"
        )
        dm.add_certificate(cert4)
        print("✓ Certificat expirat (roșu închis) adăugat")
        
        # Verifică încărcarea
        certificates = dm.get_all_certificates()
        print(f"✓ Total certificate încărcate: {len(certificates)}")
        
        # Afișează statusul fiecărui certificat
        print("\nStatus certificate:")
        for i, cert in enumerate(certificates, 1):
            zile = cert.zile_pana_la_expirare()
            culoare = cert.get_status_color()
            status = "EXPIRAT" if zile < 0 else f"{zile} zile"
            print(f"  {i}. {cert.nume} {cert.prenume} - {status} - {culoare}")
        
        # Test export
        export_file = "/tmp/test_export.xlsx"
        success, msg = dm.export_to_excel(export_file)
        if success:
            print(f"✓ Export reușit: {export_file}")
        else:
            print(f"✗ Export eșuat: {msg}")
        
    except Exception as e:
        print(f"✗ Eroare la testarea DataManager: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    return True


def test_color_coding():
    """Testează sistemul de colorare"""
    print("=== Test Sistem Colorare ===")
    
    today = date.today()
    
    test_cases = [
        ("Expirat", today - timedelta(days=10), "#8B0000"),
        ("20 zile", today + timedelta(days=20), "#FFB6C1"),
        ("60 zile", today + timedelta(days=60), "#FFFF99"),
        ("365 zile", today + timedelta(days=365), "#FFFFFF"),
    ]
    
    for name, expiry_date, expected_color in test_cases:
        cert = Certificate(
            grad="Soldat",
            nume="Test",
            prenume=name,
            data_nasterii=date(1990, 1, 1),
            serie_certificat="XX",
            numar_certificat="000000",
            nivel_certificat="S",
            data_eliberare=today - timedelta(days=365),
            data_expirare=expiry_date,
            observatii=""
        )
        
        color = cert.get_status_color()
        status = "✓" if color == expected_color else "✗"
        print(f"{status} {name}: {color} (așteptat: {expected_color})")
    
    print()
    return True


def main():
    """Rulează toate testele"""
    print("╔════════════════════════════════════════════════╗")
    print("║  Test Manager Certificate Securitate          ║")
    print("╚════════════════════════════════════════════════╝")
    print()
    
    results = []
    
    results.append(("Model Certificate", test_certificate_model()))
    results.append(("Data Manager", test_data_manager()))
    results.append(("Sistem Colorare", test_color_coding()))
    
    print("╔════════════════════════════════════════════════╗")
    print("║  Rezultate Teste                               ║")
    print("╚════════════════════════════════════════════════╝")
    
    for name, result in results:
        status = "✓ SUCCES" if result else "✗ EȘUAT"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    
    print()
    if all_passed:
        print("✓ Toate testele au trecut cu succes!")
    else:
        print("✗ Unele teste au eșuat!")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
