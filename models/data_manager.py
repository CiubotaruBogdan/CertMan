"""
Manager pentru gestionarea datelor certificate
"""
import pandas as pd
from pathlib import Path
from typing import List, Optional
from models.certificate import Certificate, COLUMN_NAMES


class DataManager:
    """Gestionează operațiile CRUD pentru certificate"""
    
    def __init__(self, file_path: str):
        """
        Inițializează managerul de date
        
        Args:
            file_path: Calea către fișierul Excel
        """
        self.file_path = Path(file_path)
        self.df: Optional[pd.DataFrame] = None
        self._load_or_create()
    
    def _load_or_create(self):
        """Încarcă fișierul Excel sau creează unul nou"""
        if self.file_path.exists():
            try:
                self.df = pd.read_excel(self.file_path)
                # Verifică structura
                if not self._validate_structure():
                    raise ValueError("Structura fișierului este invalidă")
            except Exception as e:
                raise Exception(f"Eroare la încărcarea fișierului: {str(e)}")
        else:
            # Creează fișier nou cu structură goală
            self.df = pd.DataFrame(columns=COLUMN_NAMES)
            self._save()
    
    def _validate_structure(self) -> bool:
        """
        Validează că fișierul are toate coloanele necesare
        Suportă atât formatul nou (lowercase) cât și cel vechi (capitalized)
        
        Returns:
            True dacă structura este validă
        """
        # Coloane vechi (pentru compatibilitate)
        old_column_names = [
            'Grad', 'Nume', 'Prenume', 'Data Nașterii',
            'Serie Certificat', 'Număr Certificat', 'Nivel Certificat',
            'Data Eliberare', 'Data Expirare', 'Observații'
        ]
        
        # Verifică dacă are coloanele noi
        has_new_columns = all(col in self.df.columns for col in COLUMN_NAMES)
        
        # Verifică dacă are coloanele vechi
        has_old_columns = all(col in self.df.columns for col in old_column_names)
        
        # Dacă are coloanele vechi, le redenumește la cele noi
        if has_old_columns and not has_new_columns:
            rename_map = {
                'Data Nașterii': 'Data nașterii',
                'Serie Certificat': 'Serie certificat',
                'Număr Certificat': 'Număr certificat',
                'Nivel Certificat': 'Nivel certificat',
                'Data Eliberare': 'Data eliberare',
                'Data Expirare': 'Data expirare'
            }
            self.df.rename(columns=rename_map, inplace=True)
            # Salvează cu noile nume
            self._save()
            return True
        
        return has_new_columns or has_old_columns
    
    def _save(self):
        """Salvează datele în fișierul Excel"""
        # Asigură că directorul există
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Salvează cu formatare
        with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
            self.df.to_excel(writer, index=False, sheet_name='Certificate')
            
            # Ajustează lățimea coloanelor
            worksheet = writer.sheets['Certificate']
            for idx, col in enumerate(self.df.columns):
                max_length = max(
                    self.df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
    
    def get_all_certificates(self) -> List[Certificate]:
        """
        Returnează toate certificatele
        
        Returns:
            Lista de obiecte Certificate
        """
        certificates = []
        
        # Dacă DataFrame-ul este gol, returnează listă goală
        if self.df.empty:
            return certificates
        
        for _, row in self.df.iterrows():
            try:
                row_dict = row.to_dict()
                
                # Ignoră rânduri goale sau cu valori NaN
                if pd.isna(row_dict.get('Nume')) or row_dict.get('Nume') == '':
                    continue
                
                cert = Certificate.from_dict(row_dict)
                certificates.append(cert)
            except Exception as e:
                print(f"Eroare la parsarea certificatului: {e}")
                continue
        return certificates
    
    def add_certificate(self, certificate: Certificate):
        """
        Adaugă un certificat nou
        
        Args:
            certificate: Obiect Certificate de adăugat
        """
        new_row = pd.DataFrame([certificate.to_dict()])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self._save()
    
    def update_certificate(self, index: int, certificate: Certificate):
        """
        Actualizează un certificat existent
        
        Args:
            index: Indexul rândului de actualizat
            certificate: Noul obiect Certificate
        """
        if 0 <= index < len(self.df):
            for col, value in certificate.to_dict().items():
                self.df.at[index, col] = value
            self._save()
        else:
            raise IndexError(f"Index invalid: {index}")
    
    def delete_certificate(self, index: int):
        """
        Șterge un certificat
        
        Args:
            index: Indexul rândului de șters
        """
        if 0 <= index < len(self.df):
            self.df = self.df.drop(index).reset_index(drop=True)
            self._save()
        else:
            raise IndexError(f"Index invalid: {index}")
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Returnează DataFrame-ul curent
        
        Returns:
            DataFrame cu toate datele
        """
        return self.df.copy()
    
    def import_from_excel(self, file_path: str) -> tuple[bool, str]:
        """
        Importă date dintr-un fișier Excel extern
        
        Args:
            file_path: Calea către fișierul de importat
            
        Returns:
            Tuple (succes, mesaj)
        """
        try:
            df_import = pd.read_excel(file_path)
            
            # Validează structura
            if not all(col in df_import.columns for col in COLUMN_NAMES):
                missing = [col for col in COLUMN_NAMES if col not in df_import.columns]
                return False, f"Lipsesc coloanele: {', '.join(missing)}"
            
            # Validează fiecare rând
            errors = []
            for idx, row in df_import.iterrows():
                try:
                    Certificate.from_dict(row.to_dict())
                except Exception as e:
                    errors.append(f"Rând {idx + 2}: {str(e)}")
            
            if errors:
                return False, "Erori de validare:\n" + "\n".join(errors[:5])
            
            # Dacă totul e OK, adaugă datele
            self.df = pd.concat([self.df, df_import[COLUMN_NAMES]], ignore_index=True)
            self._save()
            
            return True, f"Importate cu succes {len(df_import)} înregistrări"
            
        except Exception as e:
            return False, f"Eroare la import: {str(e)}"
    
    def export_to_excel(self, file_path: str) -> tuple[bool, str]:
        """
        Exportă datele într-un fișier Excel
        
        Args:
            file_path: Calea către fișierul de export
            
        Returns:
            Tuple (succes, mesaj)
        """
        try:
            export_path = Path(file_path)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
                self.df.to_excel(writer, index=False, sheet_name='Certificate')
                
                # Ajustează lățimea coloanelor
                worksheet = writer.sheets['Certificate']
                for idx, col in enumerate(self.df.columns):
                    max_length = max(
                        self.df[col].astype(str).apply(len).max(),
                        len(col)
                    ) if len(self.df) > 0 else len(col)
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
            
            return True, f"Exportate cu succes {len(self.df)} înregistrări"
            
        except Exception as e:
            return False, f"Eroare la export: {str(e)}"
    
    def change_data_source(self, new_file_path: str):
        """
        Schimbă sursa de date
        
        Args:
            new_file_path: Calea către noul fișier
        """
        self.file_path = Path(new_file_path)
        self._load_or_create()
