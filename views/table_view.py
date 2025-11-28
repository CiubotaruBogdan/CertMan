"""
Tabel personalizat pentru afișarea certificatelor
"""
from PyQt6.QtWidgets import (QTableWidget, QTableWidgetItem, QHeaderView,
                              QMenu, QAbstractItemView)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QAction
from models.certificate import Certificate, COLUMN_NAMES


class CertificateTableWidget(QTableWidget):
    """Widget tabel personalizat pentru certificate"""
    
    # Signal emis când se face dublu-click pe un rând
    row_double_clicked = pyqtSignal(int)
    
    def __init__(self, parent=None):
        """Inițializează tabelul"""
        super().__init__(parent)
        
        self.visible_columns = COLUMN_NAMES.copy()
        self._init_ui()
    
    def _init_ui(self):
        """Inițializează interfața tabelului"""
        # Setări generale
        self.setColumnCount(len(COLUMN_NAMES))
        self.setHorizontalHeaderLabels(COLUMN_NAMES)
        
        # Comportament
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        
        # Header
        header = self.horizontalHeader()
        header.setSectionsMovable(False)
        header.setStretchLastSection(True)
        
        # Ajustează lățimea coloanelor
        for i in range(len(COLUMN_NAMES)):
            if i < 3:  # Grad, Nume, Prenume
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
        
        # Context menu pentru coloane
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self._show_column_menu)
        
        # Dublu-click
        self.doubleClicked.connect(self._on_double_click)
    
    def _on_double_click(self, index):
        """Handler pentru dublu-click"""
        if index.isValid():
            self.row_double_clicked.emit(index.row())
    
    def _show_column_menu(self, position):
        """Afișează meniul contextual pentru selectarea coloanelor"""
        menu = QMenu()
        
        for col_name in COLUMN_NAMES:
            action = QAction(col_name, self)
            action.setCheckable(True)
            action.setChecked(col_name in self.visible_columns)
            action.triggered.connect(lambda checked, name=col_name: self._toggle_column(name, checked))
            menu.addAction(action)
        
        menu.exec(self.horizontalHeader().mapToGlobal(position))
    
    def _toggle_column(self, column_name: str, visible: bool):
        """
        Ascunde/afișează o coloană
        
        Args:
            column_name: Numele coloanei
            visible: True pentru afișare, False pentru ascundere
        """
        col_index = COLUMN_NAMES.index(column_name)
        
        if visible:
            if column_name not in self.visible_columns:
                self.visible_columns.append(column_name)
            self.showColumn(col_index)
        else:
            if column_name in self.visible_columns:
                self.visible_columns.remove(column_name)
            self.hideColumn(col_index)
    
    def load_certificates(self, certificates: list[Certificate]):
        """
        Încarcă certificatele în tabel
        
        Args:
            certificates: Lista de certificate
        """
        # Dezactivează sortarea temporar pentru performanță
        self.setSortingEnabled(False)
        
        # Șterge conținutul existent
        self.setRowCount(0)
        
        # Adaugă rânduri
        for cert in certificates:
            self._add_certificate_row(cert)
        
        # Reactivează sortarea
        self.setSortingEnabled(True)
    
    def _add_certificate_row(self, certificate: Certificate):
        """
        Adaugă un rând pentru un certificat
        
        Args:
            certificate: Certificat de adăugat
        """
        row = self.rowCount()
        self.insertRow(row)
        
        cert_dict = certificate.to_dict()
        color = QColor(certificate.get_status_color())
        
        for col_idx, col_name in enumerate(COLUMN_NAMES):
            value = cert_dict.get(col_name, '')
            item = QTableWidgetItem(str(value))
            
            # Setează culoarea de fundal
            item.setBackground(color)
            
            # Face celulele read-only
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            self.setItem(row, col_idx, item)
    
    def get_selected_row(self) -> int:
        """
        Returnează indexul rândului selectat
        
        Returns:
            Index rând sau -1 dacă nu e selectat nimic
        """
        selected = self.selectedItems()
        if selected:
            return selected[0].row()
        return -1
    
    def refresh_row(self, row: int, certificate: Certificate):
        """
        Reîmprospătează un rând cu date noi
        
        Args:
            row: Indexul rândului
            certificate: Noul certificat
        """
        if 0 <= row < self.rowCount():
            cert_dict = certificate.to_dict()
            color = QColor(certificate.get_status_color())
            
            for col_idx, col_name in enumerate(COLUMN_NAMES):
                value = cert_dict.get(col_name, '')
                item = self.item(row, col_idx)
                if item:
                    item.setText(str(value))
                    item.setBackground(color)
    
    def apply_filter(self, filter_text: str):
        """
        Aplică un filtru pe toate coloanele
        
        Args:
            filter_text: Text de căutat
        """
        filter_text = filter_text.lower()
        
        for row in range(self.rowCount()):
            show_row = False
            
            if not filter_text:
                show_row = True
            else:
                # Caută în toate coloanele vizibile
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    if item and filter_text in item.text().lower():
                        show_row = True
                        break
            
            self.setRowHidden(row, not show_row)
    
    def clear_filter(self):
        """Șterge filtrul și afișează toate rândurile"""
        for row in range(self.rowCount()):
            self.setRowHidden(row, False)
