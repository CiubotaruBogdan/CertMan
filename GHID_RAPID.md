# Ghid Rapid - Manager Certificate Securitate

## Pornire Rapidă

### Windows
1. Dublu-click pe `run.bat`
2. SAU deschideți Command Prompt și rulați: `python main.py`

### Linux/macOS
1. Dublu-click pe `run.sh` (sau click dreapta → Run)
2. SAU deschideți Terminal și rulați: `./run.sh`
3. SAU: `python3 main.py`

## Prima Utilizare

### Pasul 1: Selectare Fișier Date
La prima pornire veți vedea un dialog:
- **Fișier Nou**: Recomandare pentru început
  - Alegeți o locație (ex: `Documente/certificate_securitate.xlsx`)
  - Aplicația creează fișierul automat
- **Fișier Existent**: Dacă aveți deja date în Excel
  - Verificați că are coloanele corecte (vezi mai jos)

### Pasul 2: Interfața Principală
După selectarea fișierului, veți vedea:
- **Toolbar** sus: Butoane pentru acțiuni
- **Căutare**: Câmp pentru filtrare rapidă
- **Tabel**: Afișare certificate cu culori
- **Status bar** jos: Informații despre date

## Operații de Bază

### ➕ Adăugare Certificat Nou
1. Click buton **➕ Adăugare**
2. Completați formularul:
   ```
   Grad: [Selectați din listă]
   Nume: Popescu
   Prenume: Ion
   Data Nașterii: 15.05.1985
   Serie Certificat: AB
   Număr Certificat: 123456
   Nivel Certificat: S
   Data Eliberare: 01.01.2020
   Data Expirare: 01.01.2025
   Observații: (opțional)
   ```
3. Click **Salvează**

### ✏️ Editare Certificat
**Metoda 1** (Rapidă):
- Dublu-click pe rândul din tabel

**Metoda 2**:
1. Click pe rând pentru selectare
2. Click buton **✏️ Editare**

### 🗑️ Ștergere Certificat
1. Click pe rând pentru selectare
2. Click buton **🗑️ Ștergere**
3. Confirmați cu **Yes**

### 🔍 Căutare
- Tastați în câmpul **Căutare** (ex: "Popescu")
- Tabelul se filtrează automat
- Click **Șterge Filtru** pentru a vedea tot

### 📊 Sortare
- Click pe header-ul coloanei (ex: "Nume")
- Click din nou pentru inversare

### 👁️ Ascundere Coloane
1. Click dreapta pe header-ul tabelului
2. Debifați coloanele pe care nu vreți să le vedeți
3. Bifați pentru a le afișa din nou

## Culori și Statusuri

| Culoare | Semnificație | Acțiune |
|---------|--------------|---------|
| ⬜ **Alb** | > 3 luni până la expirare | Nicio acțiune |
| 🟨 **Galben** | 1-3 luni până la expirare | Planificați reînnoirea |
| 🟥 **Roșu deschis** | < 1 lună până la expirare | **URGENT** - Reînnoiți imediat |
| 🟥 **Roșu închis** | Expirat | **CRITIC** - Certificat invalid |

## Import/Export

### 📥 Import Date din Excel
1. Pregătiți fișierul Excel cu coloanele:
   - Grad, Nume, Prenume, Data Nașterii
   - Serie Certificat, Număr Certificat, Nivel Certificat
   - Data Eliberare, Data Expirare, Observații
2. Click **📥 Import**
3. Selectați fișierul
4. Aplicația validează și importă datele

### 📤 Export Date în Excel
1. Click **📤 Export**
2. Alegeți locația și numele
3. Toate datele sunt exportate

### 📁 Schimbare Fișier Sursă
1. Click **📁 Schimbare Sursă**
2. Selectați alt fișier Excel
3. Datele noi se încarcă automat

## Grade Militare Disponibile

### Trupă
- Soldat, Caporal, Sergent, Sergent Major

### Maiștri Militari
- Plutonier Adjutant, Plutonier
- Plutonier Adjutant Principal, Plutonier Major

### Ofițeri
- Sublocotenent, Locotenent, Căpitan
- Major, Locotenent Colonel, Colonel

### Generali
- General de Brigadă, General de Divizie
- General, General de Armată

## Niveluri Certificate

- **SSv** - Strict Secret de Importanță Deosebită (nivel foarte înalt)
- **S** - Secret
- **SS** - Strict Secret  
- **SSID** - Strict Secret de Importanță Deosebită

## Scurtături Tastatură

| Acțiune | Scurtătură |
|---------|------------|
| Căutare | Click în câmpul Căutare |
| Editare rând selectat | Dublu-click |
| Salvare în dialog | Enter |
| Anulare în dialog | Esc |

## Probleme Frecvente

### ❌ "Python nu este instalat"
**Soluție**: Instalați Python 3.11+ de la [python.org](https://www.python.org/downloads/)

### ❌ "Eroare la încărcarea datelor"
**Cauze posibile**:
- Fișierul Excel este deschis în altă aplicație → Închideți-l
- Nu aveți permisiuni → Verificați drepturile de acces
- Fișierul este corupt → Selectați alt fișier

### ❌ "Importul eșuează"
**Verificați**:
- Fișierul are toate cele 10 coloane
- Datele sunt în format DD.MM.YYYY
- Gradele sunt din nomenclator
- Nivelurile sunt: SSv, S, SS, sau SSID

### ❌ "Interfața nu se vede bine"
**Soluții**:
- Redimensionați fereastra
- Verificați rezoluția ecranului (min. 1024x768)
- Resetați configurația: ștergeți `~/.certificate_manager/config.json`

## Backup și Siguranță

### ✅ Recomandări
1. **Backup regulat**: Copiați fișierul Excel săptămânal
2. **Locație sigură**: Folosiți un folder protejat
3. **Nu partajați**: Nu trimiteți fișierul prin email nesecurizat
4. **Verificare**: Testați backup-urile periodic

### ⚠️ Atenție
- Aplicația NU criptează datele
- Pentru date clasificate, folosiți sisteme autorizate
- Respectați regulamentele de securitate

## Contact Suport

Pentru probleme tehnice:
1. Verificați secțiunea "Depanare" din README.md
2. Contactați administratorul de sistem
3. Păstrați mesajele de eroare pentru diagnostic

## Actualizări

Pentru versiuni noi:
1. Descărcați noua versiune
2. Copiați fișierul de date (Excel) în siguranță
3. Instalați noua versiune
4. Testați cu datele existente

---

**Versiune Ghid**: 1.0.0  
**Data**: Noiembrie 2025  
**Aplicație**: Manager Certificate Securitate
