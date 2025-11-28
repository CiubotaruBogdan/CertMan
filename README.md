# Manager Certificate Securitate

Aplicație desktop pentru gestionarea certificatelor de securitate militare, dezvoltată în Python cu interfață grafică PyQt6.

## Caracteristici Principale

### 📊 Vizualizare Date
- Tabel interactiv cu 10 coloane de informații
- Sortare pe orice coloană (click pe header)
- Filtrare rapidă prin căutare text
- Coloane selectabile (click dreapta pe header)
- Colorare automată bazată pe status expirare

### ✏️ Gestionare Certificate
- **Adăugare**: Formular complet cu validare
- **Editare**: Dublu-click pe rând sau buton Editare
- **Ștergere**: Cu confirmare pentru siguranță
- **Validare**: Verificare automată date și nomenclatoare

### 📁 Import/Export
- Import din fișiere Excel (.xlsx)
- Export în format Excel
- Validare structură la import
- Verificare integritate date

### 🎨 Sistem Alertare Vizuală

| Status | Culoare | Condiție |
|--------|---------|----------|
| Normal | Alb | Mai mult de 3 luni până la expirare |
| Atenție | Galben | 1-3 luni până la expirare |
| Urgent | Roșu deschis | Mai puțin de 1 lună până la expirare |
| Expirat | Roșu închis | Data expirare depășită |

## Instalare

### Cerințe Sistem
- Python 3.11 sau mai nou
- Sistem de operare: Windows, Linux, sau macOS
- 100 MB spațiu liber pe disc

### Instalare Dependențe

```bash
cd certificate_manager
pip install -r requirements.txt
```

Sau cu sudo (Linux):
```bash
sudo pip3 install -r requirements.txt
```

### Dependențe Necesare
- PyQt6 >= 6.6.1
- pandas >= 2.1.4
- openpyxl >= 3.1.2

## Utilizare

### Pornire Aplicație

**Linux/macOS:**
```bash
python3 main.py
```

**Windows:**
```bash
python main.py
```

Sau dublu-click pe `main.py` (dacă Python este asociat cu extensia .py)

### Prima Deschidere

La prima pornire, aplicația va solicita:
1. Selectarea unui fișier Excel pentru stocarea datelor
2. Opțiuni:
   - **Fișier Nou**: Creează un fișier nou (recomandat)
   - **Fișier Existent**: Folosește un fișier existent

Aplicația va crea automat structura necesară în fișierul selectat.

### Operații Principale

#### Adăugare Certificat
1. Click pe butonul **➕ Adăugare** din toolbar
2. Completați formularul:
   - **Grad**: Selectați din lista de grade militare
   - **Nume, Prenume**: Text obligatoriu
   - **Data Nașterii**: Selectați din calendar
   - **Serie/Număr Certificat**: Identificare unică
   - **Nivel Certificat**: SSv, S, SS, sau SSID
   - **Date Eliberare/Expirare**: Din calendar
   - **Observații**: Text opțional
3. Click **Salvează**

#### Editare Certificat
- **Metoda 1**: Dublu-click pe rândul dorit
- **Metoda 2**: Selectați rândul → Click **✏️ Editare**

#### Ștergere Certificat
1. Selectați rândul dorit
2. Click **🗑️ Ștergere**
3. Confirmați acțiunea

#### Căutare și Filtrare
1. Introduceți text în câmpul **Căutare**
2. Tabelul se filtrează automat
3. Click **Șterge Filtru** pentru a afișa toate înregistrările

#### Sortare
- Click pe header-ul coloanei dorite
- Click repetat pentru inversare ordine

#### Selectare Coloane Vizibile
1. Click dreapta pe header-ul tabelului
2. Bifați/debifați coloanele dorite
3. Coloanele se ascund/afișează instant

#### Import Date
1. Click **📥 Import**
2. Selectați fișierul Excel (.xlsx)
3. Aplicația validează:
   - Structura coloanelor
   - Formatele datelor
   - Valorile nomenclatoarelor
4. Datele valide sunt adăugate

#### Export Date
1. Click **📤 Export**
2. Alegeți locația și numele fișierului
3. Toate înregistrările sunt exportate

#### Schimbare Sursă Date
1. Click **📁 Schimbare Sursă**
2. Selectați noul fișier Excel
3. Datele noi sunt încărcate automat

## Structura Date

### Coloane Tabel

| Coloană | Tip | Obligatoriu | Descriere |
|---------|-----|-------------|-----------|
| Grad | Text | Da | Grad militar din nomenclator |
| Nume | Text | Da | Numele persoanei |
| Prenume | Text | Da | Prenumele persoanei |
| Data Nașterii | Dată | Da | Format: DD.MM.YYYY |
| Serie Certificat | Text | Da | Seria certificatului |
| Număr Certificat | Text | Da | Numărul certificatului |
| Nivel Certificat | Text | Da | SSv, S, SS, sau SSID |
| Data Eliberare | Dată | Da | Format: DD.MM.YYYY |
| Data Expirare | Dată | Da | Format: DD.MM.YYYY |
| Observații | Text | Nu | Note suplimentare |

### Nomenclator Grade Militare

**Trupă:**
- Soldat
- Caporal
- Sergent
- Sergent Major

**Maiștri Militari:**
- Plutonier Adjutant
- Plutonier
- Plutonier Adjutant Principal
- Plutonier Major

**Ofițeri:**
- Sublocotenent
- Locotenent
- Căpitan
- Major
- Locotenent Colonel
- Colonel

**Generali:**
- General de Brigadă
- General de Divizie
- General
- General de Armată

### Niveluri Certificate
- **SSv** - Strict Secret de Importanță Deosebită (nivel foarte înalt)
- **S** - Secret
- **SS** - Strict Secret
- **SSID** - Strict Secret de Importanță Deosebită

## Configurare

### Fișier Configurare
Aplicația salvează setările în: `~/.certificate_manager/config.json`

**Setări salvate:**
- Calea către fișierul de date
- Coloanele vizibile
- Geometria ferestrei (poziție, dimensiune)

### Locație Date
Datele sunt stocate în fișierul Excel selectat de utilizator. Recomandări:
- Păstrați backup-uri regulate
- Folosiți o locație sigură (folder protejat)
- Nu partajați fișierul pe rețele nesecurizate

## Depanare

### Probleme Comune

**Aplicația nu pornește:**
- Verificați instalarea Python: `python3 --version`
- Reinstalați dependențele: `pip3 install -r requirements.txt`
- Verificați mesajele de eroare în terminal

**Eroare la încărcarea datelor:**
- Verificați că fișierul Excel nu este deschis în altă aplicație
- Verificați permisiunile de acces la fișier
- Încercați să selectați un fișier nou

**Importul eșuează:**
- Verificați că fișierul are toate coloanele necesare
- Verificați formatele datelor (DD.MM.YYYY)
- Verificați că gradele și nivelurile sunt din nomenclator

**Interfața nu se afișează corect:**
- Verificați instalarea PyQt6: `pip3 show PyQt6`
- Încercați să redimensionați fereastra
- Resetați configurația (ștergeți `~/.certificate_manager/config.json`)

## Structura Proiect

```
certificate_manager/
├── main.py                    # Punct de intrare aplicație
├── requirements.txt           # Dependențe Python
├── README.md                  # Documentație (acest fișier)
├── test_app.py               # Script testare
├── models/                    # Modele de date
│   ├── __init__.py
│   ├── certificate.py        # Model certificat + nomenclatoare
│   └── data_manager.py       # Gestionare CRUD și Excel
├── views/                     # Interfață grafică
│   ├── __init__.py
│   ├── main_window.py        # Fereastra principală
│   ├── table_view.py         # Tabel personalizat
│   └── dialogs.py            # Dialoguri adăugare/editare
├── controllers/               # Logică aplicație (rezervat)
│   └── __init__.py
└── utils/                     # Utilitare
    ├── __init__.py
    └── config_manager.py     # Gestionare configurație
```

## Securitate

### Recomandări
- ⚠️ **Nu stocați date clasificate pe sisteme neautorizate**
- 🔒 Folosiți criptare la nivel de disc pentru fișierele de date
- 📋 Păstrați backup-uri în locații sigure
- 🔐 Restricționați accesul la fișierul de date
- 🚫 Nu transmiteți fișierul prin email nesecurizat

### Limitări
- Aplicația **NU** criptează datele în fișierul Excel
- Aplicația **NU** implementează control acces utilizatori
- Pentru medii clasificate, consultați regulamentele de securitate

## Licență

Aplicație dezvoltată pentru uz intern - Ministerul Apărării Naționale.

## Suport

Pentru probleme tehnice sau sugestii de îmbunătățire, contactați administratorul de sistem.

## Versiune

**Versiunea**: 1.0.0  
**Data**: Noiembrie 2025  
**Python**: 3.11+  
**PyQt6**: 6.6.1+
