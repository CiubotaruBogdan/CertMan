"""
Tabel personalizat pentru afișarea certificatelor
"""
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
from models.certificate import Certificate, COLUMN_NAMES


class CertificateTableView(QTableWidget):
    """Tabel personalizat pentru afișarea certificatelor"""
    
    def __init__(self, parent=None):
        """Inițializează tabelul"""
        super().__init__(parent)
        self._init_ui()
        self.visible_columns = list(range(len(COLUMN_NAMES)))
    
    def _init_ui(self):
        """Inițializează interfața tabelului"""
        # Setează numărul de coloane
        self.setColumnCount(len(COLUMN_NAMES))
        self.setHorizontalHeaderLabels(COLUMN_NAMES)
        
        # Configurare header
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self._show_column_menu)
        
        # Permite sortare
        self.setSortingEnabled(True)
        
        # Configurare selecție
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Configurare aspect
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        
        # Editare dezactivată (doar prin dialog)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    
    def _show_column_menu(self, position):
        """Afișează meniul pentru ascundere/afișare coloane"""
        menu = QMenu()
        
        for col_idx, col_name in enumerate(COLUMN_NAMES):
            action = menu.addAction(col_name)
            action.setCheckable(True)
            action.setChecked(not self.isColumnHidden(col_idx))
            action.setData(col_idx)
        
        action = menu.exec(self.horizontalHeader().mapToGlobal(position))
        if action:
            col_idx = action.data()
            self.setColumnHidden(col_idx, not action.isChecked())
            
            if action.isChecked() and col_idx not in self.visible_columns:
                self.visible_columns.append(col_idx)
            elif not action.isChecked() and col_idx in self.visible_columns:
                self.visible_columns.remove(col_idx)
    
    def load_certificates(self, certificates: list[Certificate]):
        """
        Încarcă lista de certificate în tabel
        
        Args:
            certificates: Lista de certificate
        """
        self.setSortingEnabled(False)
        self.setRowCount(0)
        
        for cert in certificates:
            self._add_certificate_row(cert)
        
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
    
    def _add_certificate_row(self, certificate: Certificate):
        """
        Adaugă un rând nou cu un certificat
        
        Args:
            certificate: Certificatul de adăugat
        """
        row = self.rowCount()
        self.insertRow(row)
        
        cert_dict = certificate.to_dict()
        
        # Determină culoarea pentru celula Data expirare
        zile = certificate.zile_pana_la_expirare()
        if zile < 0:
            # Expirat - roșu
            expirare_color = QColor(255, 0, 0)  # Roșu
        elif zile <= 90:  # Mai puțin de 3 luni
            # Sub 3 luni - galben
            expirare_color = QColor(255, 255, 0)  # Galben
        else:
            # Normal - alb
            expirare_color = QColor(255, 255, 255)  # Alb
        
        for col_idx, col_name in enumerate(COLUMN_NAMES):
            value = cert_dict.get(col_name, '')
            item = QTableWidgetItem(str(value))
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            
            # Aplică culoare DOAR pe celula Data expirare
            if col_name == 'Data expirare':
                item.setBackground(QBrush(expirare_color))
                # Text negru pentru vizibilitate
                item.setForeground(QBrush(QColor(0, 0, 0)))
            else:
                # Toate celelalte celule rămân albe
                item.setBackground(QBrush(QColor(255, 255, 255)))
            
            self.setItem(row, col_idx, item)
    
    def get_selected_certificate_index(self) -> int:
        """
        Returnează indexul certificatului selectat
        
        Returns:
            Index-ul rândului selectat sau -1 dacă nu e nimic selectat
        """
        selected = self.selectedItems()
        if selected:
            return selected[0].row()
        return -1
    
    def get_selected_row(self) -> int:
        """
        Returnează indexul rândului selectat
        
        Returns:
            Index-ul rândului selectat sau -1 dacă nu e nimic selectat
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
            
            # Determină culoarea pentru celula Data expirare
            zile = certificate.zile_pana_la_expirare()
            if zile < 0:
                expirare_color = QColor(255, 0, 0)  # Roșu
            elif zile <= 90:  # Mai puțin de 3 luni
                expirare_color = QColor(255, 255, 0)  # Galben
            else:
                expirare_color = QColor(255, 255, 255)  # Alb
            
            for col_idx, col_name in enumerate(COLUMN_NAMES):
                value = cert_dict.get(col_name, '')
                item = self.item(row, col_idx)
                if item:
                    item.setText(str(value))
                    
                    # Aplică culoare DOAR pe celula Data expirare
                    if col_name == 'Data expirare':
                        item.setBackground(QBrush(expirare_color))
                        item.setForeground(QBrush(QColor(0, 0, 0)))
                    else:
                        item.setBackground(QBrush(QColor(255, 255, 255)))
    
    def apply_filter(self, filter_text: str):
        """
        Aplică un filtru pe toate coloanele
        
        Args:
            filter_text: Textul de căutat
        """
        filter_text = filter_text.lower()
        
        for row in range(self.rowCount()):
            match = False
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            
            self.setRowHidden(row, not match)
    
    def apply_expiration_filter(self, months: int):
        """
        Aplică filtru bazat pe numărul de luni până la expirare
        
        Args:
            months: Numărul de luni (0 = toate, -1 = expirate, altfel = expiră în X luni)
        """
        if months == 0:
            # Afișează toate
            for row in range(self.rowCount()):
                self.setRowHidden(row, False)
            return
        
        # Găsește indexul coloanei Data expirare
        expirare_col = COLUMN_NAMES.index('Data expirare')
        
        for row in range(self.rowCount()):
            item = self.item(row, expirare_col)
            if not item:
                continue
            
            # Parsează data
            from datetime import datetime
            try:
                data_expirare = datetime.strptime(item.text(), '%d.%m.%Y')
                zile = (data_expirare - datetime.now()).days
                
                if months == -1:
                    # Doar expirate
                    show = zile < 0
                else:
                    # Expiră în X luni
                    zile_max = months * 30
                    show = 0 <= zile <= zile_max
                
                self.setRowHidden(row, not show)
            except:
                # Dacă nu putem parsa data, ascundem rândul
                self.setRowHidden(row, True)
