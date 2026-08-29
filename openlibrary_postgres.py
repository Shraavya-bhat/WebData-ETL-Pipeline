import requests
import psycopg

query = input("🔎 Search for a book: ")

# Get data from Open Library
response = requests.get(
    "https://openlibrary.org/search.json",
    params={"q": query, "limit": 10}
)

response.raise_for_status()

data = response.json()

# Connect to PostgreSQL container
conn = psycopg.connect(
    host="psql-db",
    port=5432,
    dbname="demo",
    user="postgres",
    password="REMOVED_SECRET"
)

cursor = conn.cursor()

for book in data["docs"]:
    title = book.get("title", "Unknown")
    authors = book.get("author_name", ["Unknown"])
    author = ", ".join(authors[:2])
    year = book.get("first_publish_year")

    cursor.execute(
        "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)",
        (title, author, year)
    )

    print(f"📖 {title} | 👤 {author} | 📅 {year}")

conn.commit()

cursor.close()
conn.close()

print("\n✅ Data stored in PostgreSQL!")
