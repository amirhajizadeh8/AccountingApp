import sys
import sqlite3
from PySide2.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("برنامه حسابداری ساده")
        self.setGeometry(100, 100, 600, 400)

        self.conn = sqlite3.connect("accounting.db")

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

        self.load_data()

    def load_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, date, description, amount FROM transactions")
        rows = cursor.fetchall()

        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["شناسه", "تاریخ", "شرح", "مبلغ"])

        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row_idx, col_idx, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
