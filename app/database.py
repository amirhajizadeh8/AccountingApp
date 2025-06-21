import sqlite3
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide2.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db  # دیتابیس را ذخیره می‌کنیم
        self.init_ui()


class Database:
    def __init__(self, db_name="app_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount INTEGER NOT NULL,
            type TEXT CHECK(type IN ('درآمد', 'هزینه')) NOT NULL,
            date TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_transaction(self, title, amount, t_type, date):
        query = "INSERT INTO transactions (title, amount, type, date) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (title, amount, t_type, date))
        self.conn.commit()

            # ────────────────────────────────────────────────
    # داشبورد – خلاصه مبالغ
    # ────────────────────────────────────────────────
    def _sum_by_type(self, t_type: str) -> int:
        """جمعِ مبلغ‌ها برای نوع مشخص (درآمد یا هزینه). اگر هیچ رکوردی نبود، صفر برمی‌گرداند."""
        cur = self.conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = ?", (t_type,)
        )
        return cur.fetchone()[0]

    def get_summary(self):
        """برمی‌گرداند: (موجودی کل، جمع درآمدها، جمع هزینه‌ها)"""
        income  = self._sum_by_type("درآمد")
        expense = self._sum_by_type("هزینه")
        balance = income - expense
        return balance, income, expense

    # ────────────────────────────────────────────────
    # داشبورد – تراکنش‌های اخیر
    # ────────────────────────────────────────────────
    def get_recent_transactions(self, limit: int = 5):
        """آخرین `limit` تراکنش به‌صورت لیست تاپل برمی‌گرداند."""
        cur = self.conn.execute(
            "SELECT * FROM transactions ORDER BY date DESC LIMIT ?", (limit,)
        )
        return cur.fetchall()


    def get_all_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        return cursor.fetchall()

    def delete_transaction(self, transaction_id):
        query = "DELETE FROM transactions WHERE id = ?"
        self.conn.execute(query, (transaction_id,))
        self.conn.commit()

    def update_transaction(self, transaction_id, title, amount, t_type, date):
        query = """
        UPDATE transactions
        SET title = ?, amount = ?, type = ?, date = ?
        WHERE id = ?
        """
        self.conn.execute(query, (title, amount, t_type, date, transaction_id))
        self.conn.commit()


def get_recent_transactions(self, limit=5):
    query = "SELECT * FROM transactions ORDER BY date DESC LIMIT ?"
    return self.conn.execute(query, (limit,)).fetchall()

def _sum_by_type(self, t_type):
    query = "SELECT SUM(amount) FROM transactions WHERE type = ?"
    result = self.conn.execute(query, (t_type,)).fetchone()[0]
    return result if result else 0

def _sum_by_type(self, t_type):
    query = "SELECT SUM(amount) FROM transactions WHERE type = ?"
    result = self.conn.execute(query, (t_type,)).fetchone()[0]
    return result if result else 0



    def close(self):
        self.conn.close()
