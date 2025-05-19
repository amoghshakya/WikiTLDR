import sqlite3


def init_database(db_name: str = "simple_articles.db") -> sqlite3.Connection:
    """
    Initialize the SQLite database and create the articles table if it doesn't exist.
    """
    conn = sqlite3.connect(f"raw_data/{db_name}")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   input_text TEXT,
                   target_text TEXT
                )
                   """)
    conn.commit()

    return conn


def insert_articles(conn: sqlite3.Connection, articles: list[dict[str, str]]) -> None:
    """
    Insert multiple articles into the database in bulk.
    """
    try:
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT OR IGNORE INTO articles (title, input_text, target_text)
            VALUES (?, ?, ?)
        """, [(a['title'], a['input_text'], a['target_text']) for a in articles])
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting articles: {e}")
