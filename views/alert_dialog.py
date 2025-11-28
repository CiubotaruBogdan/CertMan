"""
Dialog de alertă pentru certificate care expiră
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QPushButton, QTableWidget, QTableWidgetItem,
                              QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from models.certificate import Certificate


class AlertDialog(QDialog):
    """Dialog pentru afișarea alertelor de expirare certificate"""
    
    def __init__(self, expirate: list[Certificate], urgente: list[Certificate], 
                 atentie: list[Certificate], parent=None):
        """
        Inițializează dialogul de alertă
        
        Args:
            expirate: Lista certificate expirate
            urgente: Lista certificate urgente (< 1 lună)
            atentie: Lista certificate cu atenție (1-3 luni)
            parent: Widget părinte
        """
        super().__init__(parent)
        
        self.expirate = expirate
        self.urgente = urgente
        self.atentie = atentie
        
        self.setWindowTitle("⚠️ ALERTĂ - Certificate care Expiră")
        self.setModal(True)
        self.setMinimumSize(900, 600)
        
        self._init_ui()
    
    def _init_ui(self):
        """Inițializează interfața utilizator"""
        layout = QVBoxLayout()
        
        # Header cu icon și mesaj
        header_layout = QHBoxLayout()
        
        # Icon mare de alertă
        icon_label = QLabel("⚠️")
        icon_font = QFont()
        icon_font.setPointSize(48)
        icon_label.setFont(icon_font)
        header_layout.addWidget(icon_label)
        
        # Mesaj principal
        message_layout = QVBoxLayout()
        
        title_label = QLabel("ATENȚIE - Certificate care Necesită Acțiune")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        message_layout.addWidget(title_label)
        
        # Statistici
        total_probleme = len(self.expirate) + len(self.urgente) + len(self.atentie)
        
        stats_text = f"""
        <b style='color: #8B0000;'>🔴 Certificate EXPIRATE: {len(self.expirate)}</b><br>
        <b style='color: #FF6B6B;'>🔴 Certificate URGENTE (&lt; 1 lună): {len(self.urgente)}</b><br>
        <b style='color: #FFD700;'>🟡 Certificate ATENȚIE (1-3 luni): {len(self.atentie)}</b><br>
        <br>
        <b>Total certificate care necesită atenție: {total_probleme}</b>
        """
        
        stats_label = QLabel(stats_text)
        stats_label.setWordWrap(True)
        message_layout.addWidget(stats_label)
        
        header_layout.addLayout(message_layout)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Separator
        separator = QLabel("─" * 100)
        layout.addWidget(separator)
        
        # Tabel cu certificate
        self.table = QTableWidget()
        self._init_table()
        self._populate_table()
        layout.addWidget(self.table)
        
        # Mesaj informativ
        info_label = QLabel(
            "💡 <b>Acțiuni recomandate:</b><br>"
            "• Certificate EXPIRATE: Reînnoiți IMEDIAT - certificate invalide<br>"
            "• Certificate URGENTE: Planificați reînnoirea în următoarele zile<br>"
            "• Certificate ATENȚIE: Începeți procedura de reînnoire"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background-color: #FFF9E6; padding: 10px; border: 1px solid #FFD700; border-radius: 5px;")
        layout.addWidget(info_label)
        
        # Buton OK
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_button = QPushButton("Am Înțeles")
        ok_button.setMinimumWidth(150)
        ok_button.setMinimumHeight(40)
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _init_table(self):
        """Inițializează tabelul"""
        columns = ["Status", "Grad", "Nume", "Prenume", "Serie", "Număr", 
                   "Nivel", "Data Expirare", "Zile Rămase"]
        
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        
        # Setări tabel
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Ajustează lățimea coloanelor
        header = self.table.horizontalHeader()
        for i in range(len(columns)):
            if i == 0:  # Status
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            elif i < 4:  # Grad, Nume, Prenume
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
    
    def _populate_table(self):
        """Populează tabelul cu datele"""
        self.table.setSortingEnabled(False)
        
        # Adaugă certificate în ordinea priorității
        all_certs = []
        
        # Expirate (prioritate maximă)
        for cert in self.expirate:
            all_certs.append(("🔴 EXPIRAT", cert, "#8B0000"))
        
        # Urgente
        for cert in self.urgente:
            all_certs.append(("🔴 URGENT", cert, "#FFB6C1"))
        
        # Atenție
        for cert in self.atentie:
            all_certs.append(("🟡 ATENȚIE", cert, "#FFFF99"))
        
        # Adaugă rânduri
        for status_text, cert, color in all_certs:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            zile = cert.zile_pana_la_expirare()
            zile_text = "EXPIRAT" if zile < 0 else f"{zile}"
            
            data = [
                status_text,
                cert.grad,
                cert.nume,
                cert.prenume,
                cert.serie_certificat,
                cert.numar_certificat,
                cert.nivel_certificat,
                cert.data_expirare.strftime('%d.%m.%Y'),
                zile_text
            ]
            
            bg_color = QColor(color)
            
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                item.setBackground(bg_color)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # Bold pentru status
                if col == 0:
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                
                self.table.setItem(row, col, item)
        
        self.table.setSortingEnabled(True)
    
    @staticmethod
    def check_and_show_alerts(certificates: list[Certificate], parent=None) -> bool:
        """
        Verifică certificate și afișează dialog de alertă dacă e necesar
        
        Args:
            certificates: Lista de certificate de verificat
            parent: Widget părinte
            
        Returns:
            True dacă au fost găsite alerte și dialogul a fost afișat
        """
        expirate = []
        urgente = []
        atentie = []
        
        for cert in certificates:
            zile = cert.zile_pana_la_expirare()
            
            if zile < 0:
                expirate.append(cert)
            elif zile <= 30:
                urgente.append(cert)
            elif zile <= 90:
                atentie.append(cert)
        
        # Afișează dialog doar dacă există probleme
        if expirate or urgente or atentie:
            dialog = AlertDialog(expirate, urgente, atentie, parent)
            dialog.exec()
            return True
        
        return False
