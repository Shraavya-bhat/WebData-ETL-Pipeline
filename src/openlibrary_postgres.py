import os
import psycopg

from src.sources.openlibrary import OpenLibraryScraper


# -----------------------------
# Get user input
# -----------------------------
query = input("🔎 Search for a book: ")
limit = int(input("📚 How many books do you want? "))


# -----------------------------
# Extract and transform data
# -----------------------------
scraper = OpenLibraryScraper(query, limit)

data = scraper.extract()
books = scraper.transform(data)


# -----------------------------
# Connect to PostgreSQL
# -----------------------------
conn = psycopg.connect(
    host=os.getenv("POSTGRES_HOST", "psql-db"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    dbname=os.getenv("POSTGRES_DB", "demo"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()


# -----------------------------
# Insert books
# -----------------------------
stored_count = 0
duplicate_count = 0

for book in books:

    cursor.execute(
        """
        INSERT INTO books (
            openlibrary_key,
            title,
            author,
            year
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (openlibrary_key) DO NOTHING
        """,
        (
            book["openlibrary_key"],
            book["title"],
            book["author"],
            book["year"]
        )
    )

    if cursor.rowcount == 1:
        stored_count += 1
        print(
            f"📚 {book['title']} | "
            f"👤 {book['author']} | "
            f"📅 {book['year']}"
        )
    else:
        duplicate_count += 1
        print(f"⚠️ Already exists: {book['title']}")


# -----------------------------
# Commit changes
# -----------------------------
conn.commit()


# -----------------------------
# Close connection
# -----------------------------
cursor.close()
conn.close()


# -----------------------------
# Summary
# -----------------------------
print()
print(f"✅ {stored_count} new books stored in PostgreSQL!")
print(f"⚠️ {duplicate_count} duplicate books skipped")
