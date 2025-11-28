# Certificate Manager

Aplicație desktop pentru gestionarea certificatelor de securitate militare.

![Certificate Manager](assets/icon.png)

## Descriere

Certificate Manager este o aplicație desktop dezvoltată în Python cu interfață grafică PyQt6, destinată gestionării eficiente a certificatelor de securitate pentru personalul militar. Aplicația oferă funcționalități complete de vizualizare, editare, filtrare și export al datelor certificatelor.

## Funcționalități

### Gestionare Date
- ✅ **CRUD complet**: Adăugare, editare (dublu-click), ștergere certificate
- ✅ **Import/Export Excel**: Importare și exportare date în format .xlsx
- ✅ **Validare structură**: Verificare automată a structurii fișierelor importate
- ✅ **Compatibilitate retroactivă**: Suport pentru fișiere cu format vechi

### Vizualizare și Filtrare
- ✅ **Tabel interactiv**: 11 coloane cu numerotare automată
- ✅ **Sortare inteligentă**: Sortare corectă pentru date (AAAA-LL-ZZ)
- ✅ **Filtrare text**: Căutare în toate coloanele
- ✅ **Filtru expirare**: Filtrare după perioada de expirare (1, 3, 6, 12 luni)
- ✅ **Selectare coloane**: Afișare/ascundere coloane personalizabilă
- ✅ **Resize manual**: Redimensionare coloane la dimensiune dorită

### Alertare și Monitorizare
- ✅ **Alertă la pornire**: Pop-up automat pentru certificate care expiră
- ✅ **Colorare automată**: Highlight pe celula "Data expirare"
  - **Galben**: < 3 luni până la expirare
  - **Roșu**: Certificat expirat

### Interfață
- ✅ **Temă light forțată**: Interfață albă indiferent de tema sistemului
- ✅ **Selectoare de dată**: Calendar pop-up pentru câmpuri dată
- ✅ **Dialog "Despre"**: Informații despre aplicație și dezvoltator
- ✅ **Icon personalizat**: Icon certificat în fereastră și executabil

## Coloane Tabel

1. **Nr.** - Numerotare automată
2. **Grad** - Grad militar (36 grade oficiale cu abrevieri)
3. **Nume** - Nume de familie
4. **Prenume** - Prenume
5. **Data nașterii** - Data nașterii (DD.MM.YYYY)
6. **Serie certificat** - Serie certificat securitate
7. **Număr certificat** - Număr certificat securitate
8. **Nivel certificat** - Nivel (SSv, S, SS, SSID)
9. **Data eliberare** - Data eliberare certificat (DD.MM.YYYY)
10. **Data expirare** - Data expirare certificat (DD.MM.YYYY)
11. **Observații** - Note și observații

## Grade Militare

Aplicația folosește **36 grade militare oficiale** conform nomenclatorului Ministerului Apărării Naționale:

### Subofițeri (11 grade)
Sold., Frt., Cap. III, Cap. II, Cap. I, Sg., Sg. maj., Plt., Plt. maj., Plt. adj., Plt. adj. pr.

### Maiștri militari (6 grade)
M. m. V, M. m. IV, M. m. III, M. m. II, M. m. I, M. m. p.

### Ofițeri (11 grade)
Slt., Asp., Lt., Cpt., Mr., Lt. col., Col., Gl. bg., Gl. mr., Gl. lt., Gl.

### Ofițeri Forțe Navale (7 grade)
Lt. cdor., Cpt. cdor., Cdor., Cam. fl., Cam., Vam., Am.

### Ofițeri Forțe Aeriene (1 grad)
Gl. fl. aer.

## Instalare

### Cerințe
- Python 3.8 sau mai nou (recomandat Python 3.12)
- pip (package installer pentru Python)

### Instalare dependențe

```bash
pip install -r requirements.txt
```

### Dependențe
- PyQt6 >= 6.6.0
- pandas >= 2.0.0
- openpyxl >= 3.1.0

## Utilizare

### Rulare aplicație

```bash
python main.py
```

### Prima deschidere
La prima deschidere, aplicația va solicita selectarea unui fișier Excel pentru stocarea datelor:
- **Fișier Nou**: Creează un fișier nou gol
- **Fișier Existent**: Deschide un fișier existent cu date

### Operații de bază

**Adăugare certificat:**
- Click pe butonul "➕ Adăugare"
- Completați formularul
- Click "OK" pentru salvare

**Editare certificat:**
- Dublu-click pe rândul dorit
- Modificați datele în formular
- Click "OK" pentru salvare

**Ștergere certificat:**
- Selectați rândul dorit
- Click pe butonul "🗑️ Ștergere"
- Confirmați ștergerea

**Filtrare:**
- Introduceți text în bara de căutare pentru filtrare text
- Selectați perioada din dropdown "Expiră în" pentru filtrare după expirare

**Selectare coloane:**
- Click pe butonul "☰ Selectare Coloane"
- Bifați/debifați coloanele dorite
- Click "OK"

**Export:**
- Click pe butonul "📤 Export"
- Fișierul va fi salvat automat cu numele: `AAAALLZZ_N_xx-CertificateSecuritate.xlsx`

## Build Executabil

Pentru a crea un executabil standalone (fără Python):

```bash
python build_executable.py
```

Executabilul va fi creat în directorul `dist/`:
- **Windows**: `dist/CertificateManager.exe`
- **Linux/macOS**: `dist/CertificateManager`

## Generare Date Dummy

Pentru testare, puteți genera 30 înregistrări dummy:

```bash
python generate_dummy_data.py
```

Fișierul `date_dummy_30_certificate.xlsx` va fi creat cu 30 înregistrări realiste.

## Structură Proiect

```
certificate_manager/
├── assets/                    # Resurse (iconuri)
│   ├── icon.png              # Icon PNG (256x256)
│   └── icon.ico              # Icon Windows
│
├── models/                    # Modele de date
│   ├── certificate.py        # Model certificat
│   └── data_manager.py       # Manager date Excel
│
├── views/                     # Interfață grafică
│   ├── main_window.py        # Fereastră principală
│   ├── table_view.py         # Tabel certificate
│   ├── dialogs.py            # Dialog adăugare/editare
│   └── alert_dialog.py       # Dialog alertă
│
├── utils/                     # Utilitare
│   └── config_manager.py     # Gestionare configurație
│
├── controllers/               # Logică (rezervat)
│
├── main.py                    # Aplicație principală
├── build_executable.py        # Script build executabil
├── generate_dummy_data.py     # Generator date test
├── requirements.txt           # Dependențe Python
├── .gitignore                # Git ignore
└── README.md                  # Documentație (acest fișier)
```

## Tehnologii

- **Python 3.11** - Limbaj de programare
- **PyQt6** - Framework interfață grafică
- **pandas** - Procesare date tabulare
- **openpyxl** - Citire/scriere fișiere Excel
- **PyInstaller** - Creare executabil standalone

## Dezvoltator

**Bogdan Ciubotaru**  
Pentru: Ministerul Apărării Naționale

## Repository

GitHub: [CiubotaruBogdan/CertMan](https://github.com/CiubotaruBogdan/CertMan)

## Licență

Aplicație dezvoltată pentru uz intern Ministerul Apărării Naționale.

## Versiune

**v1.0** - Noiembrie 2025

---

© 2025 Ministerul Apărării Naționale. Toate drepturile rezervate.
