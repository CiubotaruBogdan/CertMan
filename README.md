# Certificate Manager

Aplicație desktop pentru gestionarea certificatelor de securitate militare.

## Instalare

```bash
pip install -r requirements.txt
```

## Utilizare

```bash
python main.py
```

## Funcționalități

- Adăugare, editare, ștergere certificate
- Filtrare și sortare
- Import/Export Excel
- Alertă automată pentru certificate care expiră
- Colorare automată: galben (< 3 luni), roșu (expirat)

## Structură

```
certificate_manager/
├── main.py              # Aplicație principală
├── requirements.txt     # Dependențe
├── models/              # Modele de date
├── views/               # Interfață grafică
├── utils/               # Utilitare
└── controllers/         # Logică (rezervat)
```

## Cerințe

- Python 3.11+
- PyQt6
- pandas
- openpyxl
