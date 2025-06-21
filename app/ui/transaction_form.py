from PySide2.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QDateEdit, QMessageBox
)
from PySide2.QtCore import QDate, Signal
from datetime import datetime


class TransactionForm(QWidget):
    transaction_saved = Signal()  # سیگنال برای اعلام ذخیره تراکنش

    def __init__(self, db):
        super().__init__()
        self.db = db
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(["درآمد", "هزینه"])
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        form.addRow("عنوان:", self.title_input)
        form.addRow("مبلغ:", self.amount_input)
        form.addRow("نوع:", self.type_input)
        form.addRow("تاریخ:", self.date_input)

        self.submit_btn = QPushButton("ذخیره تراکنش")
        self.submit_btn.clicked.connect(self.save_transaction)

        layout.addLayout(form)
        layout.addWidget(self.submit_btn)

    def save_transaction(self):
        title = self.title_input.text().strip()
        amount_text = self.amount_input.text().strip()
        t_type = self.type_input.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")

        if not title or not amount_text:
            QMessageBox.warning(self, "خطا", "لطفاً عنوان و مبلغ را وارد کنید.")
            return

        try:
            amount = int(amount_text.replace(",", ""))
        except ValueError:
            QMessageBox.warning(self, "خطا", "مبلغ باید عدد باشد.")
            return

        try:
            self.db.insert_transaction(title, amount, t_type, date)
            QMessageBox.information(self, "موفقیت", "تراکنش با موفقیت ذخیره شد.")
            self.clear_form()
            self.transaction_saved.emit()  # اعلام به بقیه ویجت‌ها برای بروزرسانی
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره تراکنش:\n{e}")

    def clear_form(self):
        self.title_input.clear()
        self.amount_input.clear()
        self.type_input.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())
