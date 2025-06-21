from pathlib import Path
from PySide2.QtCore import Qt
from PySide2.QtGui import QFontDatabase, QFont
from PySide2.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QApplication,
)

from app.database import Database
from app.ui.transaction_form import TransactionForm
from .dashboard import Dashboard
from .right_tab_bar import RightTabBar


class TransactionsTab(QWidget):
    """Tab that combines the TransactionForm + table of all transactions."""

    def __init__(self, db: Database, dashboard: Dashboard):
        super().__init__()
        self.db = db
        self.dashboard = dashboard  # to refresh balance after insert

        root = QVBoxLayout(self)
        self.form = TransactionForm(self.db)
        root.addWidget(self.form)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["عنوان", "مبلغ", "نوع", "تاریخ"])
        self.table.setAlternatingRowColors(True)
        root.addWidget(self.table)

        self.form.transaction_saved.connect(self._on_new_transaction)
        self.reload_table()

    def _on_new_transaction(self):
        self.reload_table()
        self.dashboard.refresh()

    def reload_table(self):
        self.table.setRowCount(0)
        rows = self.db.get_all_transactions()
        for row_idx, (tid, title, amount, t_type, date) in enumerate(rows):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(title))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{amount:,}"))
            self.table.setItem(row_idx, 2, QTableWidgetItem(t_type))
            self.table.setItem(row_idx, 3, QTableWidgetItem(date))
            self.table.item(row_idx, 0).setData(Qt.UserRole, tid)


class MainWindow(QMainWindow):
    """The application's main window with Dashboard and Transactions tabs."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("برنامه حسابداری")
        self.resize(900, 600)

        # shared database instance
        self.db = Database()

        # central widget with tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tabs.setTabPosition(QTabWidget.East)
        self.tabs.setTabBar(RightTabBar())

        # create tabs
        self.dashboard_tab = Dashboard(self.db)
        self.transactions_tab = TransactionsTab(self.db, self.dashboard_tab)

        # add tabs
        self.tabs.addTab(self.dashboard_tab, "داشبورد")
        self.tabs.addTab(self.transactions_tab, "تراکنش‌ها")

        # load and apply font + set راست‌چین
        self._apply_global_font()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

    @staticmethod
    def _apply_global_font():
        app = QApplication.instance()
        if not app:
            return
        font_path = (
            Path(__file__).resolve().parent.parent.parent
            / "resources"
            / "fonts"
            / "Vazir.ttf"
        )
        if font_path.exists():
            fid = QFontDatabase.addApplicationFont(str(font_path))
            if fid != -1:
                fam = QFontDatabase.applicationFontFamilies(fid)[0]
                app.setFont(QFont(fam, 11))
        app.setLayoutDirection(Qt.RightToLeft)
