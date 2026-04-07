import re
import sqlite3
import json

INPUT_FILE = "task1_d.json"
DATABASE = "books.db"


def fix_json(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    # :key=> "key" to json format
    fixed = re.sub(r":(\w+)=>", r'"\1":', raw)
    return json.loads(fixed)


def create_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            publisher TEXT,
            year INTEGER,
            price TEXT,
            price_value REAL,
            currency TEXT
        )
        """
    )

    conn.commit()
    return conn


def parse_price(price_str):
    """
    Extract numeric value and currency from a price string (price and currency)
    """
    print("PARSE PRISE PART", price_str)

    if price_str.startswith("$"):
        currency = "USD"
        value = float(price_str.replace("$", "").strip())
    elif price_str.startswith("€") or "EUR" in price_str:
        currency = "EUR"
        value = float(price_str.replace("€", "").replace("EUR", "").strip())
    print("PARSE PRISE PART OUTPUT", value, currency)
    return value, currency


def insert_books(conn, books):
    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO books (id, title, author, genre, publisher, year, price, price_value, currency)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO NOTHING
    """

    records = []
    for book in books:
        price_value, currency = parse_price(book.get("price", ""))

        records.append(
            (
                str(book["id"]),
                book["title"],
                book["author"],
                book.get("genre", ""),
                book.get("publisher", ""),
                book.get("year"),
                book.get("price", ""),
                price_value,
                currency,
            )
        )
    print("SQL QUERY", insert_sql)
    print("RECORDS", records)
    cursor.executemany(insert_sql, records)
    conn.commit()
    return len(records)


def main():

    print("Parsing task1_d.json")
    books = fix_json(INPUT_FILE)
    print(books)
    print(f"parsed {len(books)} books")


    print("\nCreating SQLite database")
    conn = create_table(DATABASE)
    print(f"Database '{DATABASE}' created")

    print("\nInserting books into db")
    count = insert_books(conn, books)
    print(f"Inserted {count} records into books table")


    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    books_count = cursor.fetchone()[0]
    print(f"\ninserted books count {books_count}")
    conn.close()

if __name__ == "__main__":
    main()