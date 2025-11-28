"""
Dialoguri pentru adăugare și editare certificate
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QLineEdit, QComboBox, QDateEdit, QTextEdit,
                              QPushButton, QMessageBox, QLabel)
from PyQt6.QtCore import QDate, Qt
from datetime import datetime
from models.certificate import Certificate, GRADE_MILITARE, NIVELURI_CERTIFICATE


class CertificateDialog(QDialog):
    """Dialog pentru adăugare/editare certificate"""
    
    def __init__(self, parent=None, certificate: Certificate = None):
        """
        Inițializează dialogul
        
        Args:
            parent: Widget părinte
            certificate: Certificat de editat (None pentru adăugare)
        """
        super().__init__(parent)
        self.certificate = certificate
        self.is_edit_mode = certificate is not None
        
        self.setWindowTitle("Editare Certificat" if self.is_edit_mode else "Adăugare Certificat")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self._init_ui()
        
        if self.is_edit_mode:
            self._populate_fields()
    
    def _init_ui(self):
        """Inițializează interfața utilizator"""
        layout = QVBoxLayout()
        
        # Formular
        form_layout = QFormLayout()
        
        # Grad
        self.grad_combo = QComboBox()
        self.grad_combo.addItems(GRADE_MILITARE)
        form_layout.addRow("Grad:", self.grad_combo)
        
        # Nume
        self.nume_edit = QLineEdit()
        self.nume_edit.setPlaceholderText("Introduceți numele")
        form_layout.addRow("Nume:", self.nume_edit)
        
        # Prenume
        self.prenume_edit = QLineEdit()
        self.prenume_edit.setPlaceholderText("Introduceți prenumele")
        form_layout.addRow("Prenume:", self.prenume_edit)
        
        # Data nașterii
        self.data_nasterii_edit = QDateEdit()
        self.data_nasterii_edit.setCalendarPopup(True)
        self.data_nasterii_edit.setDisplayFormat("dd.MM.yyyy")
        self.data_nasterii_edit.setDate(QDate.currentDate().addYears(-30))
        form_layout.addRow("Data Nașterii:", self.data_nasterii_edit)
        
        # Serie certificat
        self.serie_edit = QLineEdit()
        self.serie_edit.setPlaceholderText("Ex: AB")
        form_layout.addRow("Serie Certificat:", self.serie_edit)
        
        # Număr certificat
        self.numar_edit = QLineEdit()
        self.numar_edit.setPlaceholderText("Ex: 123456")
        form_layout.addRow("Număr Certificat:", self.numar_edit)
        
        # Nivel certificat
        self.nivel_combo = QComboBox()
        self.nivel_combo.addItems(NIVELURI_CERTIFICATE)
        form_layout.addRow("Nivel Certificat:", self.nivel_combo)
        
        # Data eliberare
        self.data_eliberare_edit = QDateEdit()
        self.data_eliberare_edit.setCalendarPopup(True)
        self.data_eliberare_edit.setDisplayFormat("dd.MM.yyyy")
        self.data_eliberare_edit.setDate(QDate.currentDate())
        form_layout.addRow("Data Eliberare:", self.data_eliberare_edit)
        
        # Data expirare
        self.data_expirare_edit = QDateEdit()
        self.data_expirare_edit.setCalendarPopup(True)
        self.data_expirare_edit.setDisplayFormat("dd.MM.yyyy")
        self.data_expirare_edit.setDate(QDate.currentDate().addYears(5))
        form_layout.addRow("Data Expirare:", self.data_expirare_edit)
        
        # Observații
        self.observatii_edit = QTextEdit()
        self.observatii_edit.setPlaceholderText("Observații opționale")
        self.observatii_edit.setMaximumHeight(80)
        form_layout.addRow("Observații:", self.observatii_edit)
        
        layout.addLayout(form_layout)
        
        # Butoane
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Salvează")
        self.save_button.clicked.connect(self._on_save)
        self.save_button.setDefault(True)
        
        self.cancel_button = QPushButton("Anulează")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _populate_fields(self):
        """Populează câmpurile cu datele certificatului existent"""
        if not self.certificate:
            return
        
        # Setează valorile
        self.grad_combo.setCurrentText(self.certificate.grad)
        self.nume_edit.setText(self.certificate.nume)
        self.prenume_edit.setText(self.certificate.prenume)
        
        # Date
        self.data_nasterii_edit.setDate(QDate(
            self.certificate.data_nasterii.year,
            self.certificate.data_nasterii.month,
            self.certificate.data_nasterii.day
        ))
        
        self.serie_edit.setText(str(self.certificate.serie_certificat))
        self.numar_edit.setText(str(self.certificate.numar_certificat))
        self.nivel_combo.setCurrentText(self.certificate.nivel_certificat)
        
        self.data_eliberare_edit.setDate(QDate(
            self.certificate.data_eliberare.year,
            self.certificate.data_eliberare.month,
            self.certificate.data_eliberare.day
        ))
        
        self.data_expirare_edit.setDate(QDate(
            self.certificate.data_expirare.year,
            self.certificate.data_expirare.month,
            self.certificate.data_expirare.day
        ))
        
        self.observatii_edit.setPlainText(self.certificate.observatii or "")
    
    def _validate_fields(self) -> tuple[bool, str]:
        """
        Validează câmpurile formularului
        
        Returns:
            Tuple (valid, mesaj_eroare)
        """
        # Verifică câmpuri obligatorii
        if not self.nume_edit.text().strip():
            return False, "Numele este obligatoriu"
        
        if not self.prenume_edit.text().strip():
            return False, "Prenumele este obligatoriu"
        
        if not self.serie_edit.text().strip():
            return False, "Seria certificatului este obligatorie"
        
        if not self.numar_edit.text().strip():
            return False, "Numărul certificatului este obligatoriu"
        
        # Verifică date
        data_nasterii = self.data_nasterii_edit.date().toPyDate()
        data_eliberare = self.data_eliberare_edit.date().toPyDate()
        data_expirare = self.data_expirare_edit.date().toPyDate()
        
        if data_eliberare >= data_expirare:
            return False, "Data de expirare trebuie să fie după data de eliberare"
        
        if data_nasterii >= data_eliberare:
            return False, "Data de eliberare trebuie să fie după data nașterii"
        
        return True, ""
    
    def _on_save(self):
        """Handler pentru butonul Salvează"""
        # Validare
        valid, error_msg = self._validate_fields()
        if not valid:
            QMessageBox.warning(self, "Validare", error_msg)
            return
        
        # Creează certificatul
        try:
            self.certificate = Certificate(
                grad=self.grad_combo.currentText(),
                nume=self.nume_edit.text().strip(),
                prenume=self.prenume_edit.text().strip(),
                data_nasterii=self.data_nasterii_edit.date().toPyDate(),
                serie_certificat=self.serie_edit.text().strip(),
                numar_certificat=self.numar_edit.text().strip(),
                nivel_certificat=self.nivel_combo.currentText(),
                data_eliberare=self.data_eliberare_edit.date().toPyDate(),
                data_expirare=self.data_expirare_edit.date().toPyDate(),
                observatii=self.observatii_edit.toPlainText().strip()
            )
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Eroare", f"Eroare la salvare: {str(e)}")
    
    def get_certificate(self) -> Certificate:
        """
        Returnează certificatul creat/editat
        
        Returns:
            Obiect Certificate
        """
        return self.certificate
