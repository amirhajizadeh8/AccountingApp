from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont

class Dashboard(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # -------------------- کارت‌ها --------------------
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(16)

        self.balance_card = self._create_card("موجودی کل", "0 تومان")
        self.income_card = self._create_card("درآمد", "0 تومان")
        self.expense_card = self._create_card("هزینه", "0 تومان")

        self.cards_layout.addWidget(self.balance_card)
        self.cards_layout.addWidget(self.income_card)
        self.cards_layout.addWidget(self.expense_card)

        self.layout.addLayout(self.cards_layout)
        self.layout.addStretch()

        # بروزرسانی مقدارها
        self.refresh()

    def _create_card(self, title, amount_text):
        card = QFrame()
        card.setObjectName("dashboardCard")
        card.setFixedHeight(120)
        card.setStyleSheet("""
            QFrame#dashboardCard {
                background-color: #2f2f40;
                border-radius: 12px;
                padding: 12px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)


        title_label = QLabel(title)
        title_label.setStyleSheet("color: #aaa; background: transparent;")
        title_label.setFont(QFont("Vazir", 10))

        amount_label = QLabel(amount_text)
        amount_label.setObjectName("amountLabel")
        amount_label.setFont(QFont("Vazir", 16, QFont.Bold))
        amount_label.setStyleSheet("color: white; background: transparent;")

        layout.addWidget(title_label)
        layout.addWidget(amount_label)

        card.amount_label = amount_label  # برای دسترسی راحت‌تر در refresh

        return card

    def refresh(self):
        # گرفتن اطلاعات از دیتابیس
        balance, income, expense = self.db.get_summary()

        self.balance_card.amount_label.setText(f"{balance:,.0f} تومان")
        self.income_card.amount_label.setText(f"{income:,.0f} تومان")
        self.expense_card.amount_label.setText(f"{expense:,.0f} تومان")
