import psycopg

from src.sources.openlibrary import OpenLibraryScraper


query = input("🔎 Search for a book: ")

while True:
    try:
        limit = int(input("📚 How many books do you want? "))

        if limit > 0:
            break

        print("⚠️ Please enter a number greater than 0.")

    except ValueError:
        print("⚠️ Please enter a valid number.")


# Extract and transform data from Open Library
scraper = OpenLibraryScraper(query, limit)

raw_data = scraper.extract()
books = scraper.transform(raw_data)


# Connect to PostgreSQL
conn = psycopg.connect(
    host="psql-db",
    port=5432,
    dbname="demo",
    user="postgres",
    password="REMOVED_SECRET"
)

cursor = conn.cursor()


# Load data into PostgreSQL
for book in books:

    cursor.execute(
        """
        INSERT INTO books (title, author, year)
        VALUES (%s, %s, %s)
        """,
        (
            book["title"],
            book["author"],
            book["year"]
        )
    )

    print(
        f"📖 {book['title']} | "
        f"👤 {book['author']} | "
        f"📅 {book['year']}"
    )


conn.commit()

cursor.close()
conn.close()

print(f"\n✅ {len(books)} books stored in PostgreSQL!")
