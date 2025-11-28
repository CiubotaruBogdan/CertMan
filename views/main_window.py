"""
Fereastra principală a aplicației
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLineEdit, QLabel, QMessageBox,
                              QFileDialog, QStatusBar, QToolBar, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from views.table_view import CertificateTableView
from views.dialogs import CertificateDialog
from models.data_manager import DataManager
from models.certificate import Certificate


class MainWindow(QMainWindow):
    """Fereastra principală a aplicației"""
    
    def __init__(self, data_manager: DataManager):
        """
        Inițializează fereastra principală
        
        Args:
            data_manager: Manager pentru date
        """
        super().__init__()
        
        self.data_manager = data_manager
        
        self.setWindowTitle("Manager Certificate Securitate")
        self.setMinimumSize(1200, 700)
        
        self._init_ui()
        self._load_data()
    
    def _init_ui(self):
        """Inițializează interfața utilizator"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Toolbar
        self._create_toolbar()
        
        # Zona de filtrare
        filter_layout = QHBoxLayout()
        
        filter_label = QLabel("Căutare:")
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Introduceți text pentru căutare...")
        self.filter_edit.textChanged.connect(self._on_filter_changed)
        
        # Dropdown filtru expirare
        expiration_label = QLabel("Expiră în:")
        self.expiration_combo = QComboBox()
        self.expiration_combo.addItems([
            "Toate",
            "Expirate",
            "1 lună",
            "3 luni",
            "6 luni",
            "12 luni"
        ])
        self.expiration_combo.currentIndexChanged.connect(self._on_expiration_filter_changed)
        
        clear_filter_btn = QPushButton("Șterge filtre")
        clear_filter_btn.clicked.connect(self._clear_filter)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_edit)
        filter_layout.addWidget(expiration_label)
        filter_layout.addWidget(self.expiration_combo)
        filter_layout.addWidget(clear_filter_btn)
        
        main_layout.addLayout(filter_layout)
        
        # Tabel
        self.table = CertificateTableView()
        self.table.doubleClicked.connect(self._on_edit_certificate)
        main_layout.addWidget(self.table)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self._update_status_bar()
    
    def _create_toolbar(self):
        """Creează toolbar-ul cu butoane"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Buton Adăugare
        add_action = QAction("➕ Adăugare", self)
        add_action.setStatusTip("Adaugă un certificat nou")
        add_action.triggered.connect(self._on_add_certificate)
        toolbar.addAction(add_action)
        
        toolbar.addSeparator()
        
        # Buton Editare
        edit_action = QAction("✏️ Editare", self)
        edit_action.setStatusTip("Editează certificatul selectat")
        edit_action.triggered.connect(self._on_edit_selected)
        toolbar.addAction(edit_action)
        
        # Buton Ștergere
        delete_action = QAction("🗑️ Ștergere", self)
        delete_action.setStatusTip("Șterge certificatul selectat")
        delete_action.triggered.connect(self._on_delete_certificate)
        toolbar.addAction(delete_action)
        
        toolbar.addSeparator()
        
        # Buton Import
        import_action = QAction("📥 Import", self)
        import_action.setStatusTip("Importă certificate din Excel")
        import_action.triggered.connect(self._on_import)
        toolbar.addAction(import_action)
        
        # Buton Export
        export_action = QAction("📤 Export", self)
        export_action.setStatusTip("Exportă certificate în Excel")
        export_action.triggered.connect(self._on_export)
        toolbar.addAction(export_action)
        
        toolbar.addSeparator()
        
        # Buton Schimbare Sursă
        change_source_action = QAction("📁 Schimbare Sursă", self)
        change_source_action.setStatusTip("Schimbă fișierul sursă de date")
        change_source_action.triggered.connect(self._on_change_source)
        toolbar.addAction(change_source_action)
        
        # Buton Reîmprospătare
        refresh_action = QAction("🔄 Reîmprospătare", self)
        refresh_action.setStatusTip("Reîmprospătează datele")
        refresh_action.triggered.connect(self._load_data)
        toolbar.addAction(refresh_action)
    
    def _load_data(self):
        """Încarcă datele în tabel"""
        try:
            certificates = self.data_manager.get_all_certificates()
            self.table.load_certificates(certificates)
            self._update_status_bar()
        except Exception as e:
            QMessageBox.critical(self, "Eroare", f"Eroare la încărcarea datelor: {str(e)}")
    
    def _update_status_bar(self):
        """Actualizează bara de status"""
        total = self.table.rowCount()
        visible = sum(1 for row in range(total) if not self.table.isRowHidden(row))
        
        file_path = str(self.data_manager.file_path)
        
        self.status_bar.showMessage(
            f"Total înregistrări: {total} | Afișate: {visible} | Fișier: {file_path}"
        )
    
    def _on_filter_changed(self, text: str):
        """Handler pentru schimbarea filtrului de căutare"""
        self.table.apply_filter(text)
        self._update_status_bar()
    
    def _on_expiration_filter_changed(self, index: int):
        """Handler pentru schimbarea filtrului de expirare"""
        # Mapare index la luni
        months_map = {
            0: 0,    # Toate
            1: -1,   # Expirate
            2: 1,    # 1 lună
            3: 3,    # 3 luni
            4: 6,    # 6 luni
            5: 12    # 12 luni
        }
        
        months = months_map.get(index, 0)
        self.table.apply_expiration_filter(months)
        self._update_status_bar()
    
    def _clear_filter(self):
        """Șterge toate filtrele"""
        self.filter_edit.clear()
        self.expiration_combo.setCurrentIndex(0)
        self.table.apply_filter("")
        self.table.apply_expiration_filter(0)
        self._update_status_bar()
    
    def _on_add_certificate(self):
        """Handler pentru adăugarea unui certificat"""
        dialog = CertificateDialog(self)
        
        if dialog.exec():
            certificate = dialog.get_certificate()
            try:
                self.data_manager.add_certificate(certificate)
                self._load_data()
                QMessageBox.information(self, "Succes", "Certificat adăugat cu succes!")
            except Exception as e:
                QMessageBox.critical(self, "Eroare", f"Eroare la adăugare: {str(e)}")
    
    def _on_edit_selected(self):
        """Handler pentru editarea certificatului selectat"""
        selected_row = self.table.get_selected_row()
        
        if selected_row == -1:
            QMessageBox.warning(self, "Atenție", "Selectați un certificat pentru editare!")
            return
        
        self._on_edit_certificate(selected_row)
    
    def _on_edit_certificate(self, row: int):
        """
        Handler pentru editarea unui certificat
        
        Args:
            row: Indexul rândului de editat
        """
        try:
            # Obține certificatul curent
            certificates = self.data_manager.get_all_certificates()
            if row >= len(certificates):
                return
            
            current_cert = certificates[row]
            
            # Afișează dialogul de editare
            dialog = CertificateDialog(self, current_cert)
            
            if dialog.exec():
                updated_cert = dialog.get_certificate()
                self.data_manager.update_certificate(row, updated_cert)
                self._load_data()
                QMessageBox.information(self, "Succes", "Certificat actualizat cu succes!")
                
        except Exception as e:
            QMessageBox.critical(self, "Eroare", f"Eroare la editare: {str(e)}")
    
    def _on_delete_certificate(self):
        """Handler pentru ștergerea unui certificat"""
        selected_row = self.table.get_selected_row()
        
        if selected_row == -1:
            QMessageBox.warning(self, "Atenție", "Selectați un certificat pentru ștergere!")
            return
        
        # Confirmă ștergerea
        reply = QMessageBox.question(
            self,
            "Confirmare Ștergere",
            "Sigur doriți să ștergeți acest certificat?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.data_manager.delete_certificate(selected_row)
                self._load_data()
                QMessageBox.information(self, "Succes", "Certificat șters cu succes!")
            except Exception as e:
                QMessageBox.critical(self, "Eroare", f"Eroare la ștergere: {str(e)}")
    
    def _on_import(self):
        """Handler pentru import Excel"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selectați fișierul pentru import",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            success, message = self.data_manager.import_from_excel(file_path)
            
            if success:
                self._load_data()
                QMessageBox.information(self, "Succes", message)
            else:
                QMessageBox.critical(self, "Eroare", message)
    
    def _on_export(self):
        """Handler pentru export Excel"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Selectați locația pentru export",
            "certificate_export.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            success, message = self.data_manager.export_to_excel(file_path)
            
            if success:
                QMessageBox.information(self, "Succes", message)
            else:
                QMessageBox.critical(self, "Eroare", message)
    
    def _on_change_source(self):
        """Handler pentru schimbarea sursei de date"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selectați noul fișier sursă",
            "",
            "Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                self.data_manager.change_data_source(file_path)
                self._load_data()
                QMessageBox.information(
                    self,
                    "Succes",
                    f"Sursa de date schimbată cu succes!\nNoul fișier: {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Eroare", f"Eroare la schimbarea sursei: {str(e)}")
