import sqlite3

def create_connection(db_file):
    """ اتصال به دیتابیس SQLite یا ساختن آن """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("اتصال به دیتابیس موفق بود:", db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """ ساخت جدول تراکنش‌ها """
    try:
        sql_create_transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql_create_transactions_table)
        print("جدول transactions ساخته شد یا قبلا وجود داشت")
    except sqlite3.Error as e:
        print(e)

if __name__ == "__main__":
    conn = create_connection("accounting.db")
    if conn:
        create_table(conn)
        conn.close()
