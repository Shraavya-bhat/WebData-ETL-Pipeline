
# 🌐 Web Data ETL Pipeline

An extensible, containerized ETL pipeline that extracts structured data from web APIs, transforms and validates the records, and loads them into PostgreSQL.

The project currently uses the **Open Library Search API** as its data source, with a reusable scraper architecture designed to support additional web/API sources.

## 🚀 Overview

This project demonstrates an end-to-end **Extract, Transform, Load (ETL)** workflow using Python, Docker, and PostgreSQL.

```text
Web / API Source
       │
       ▼
   Base Scraper
       │
       ▼
Source-Specific Scraper
   (Open Library)
       │
       ▼
Extract → Transform → Validate
       │
       ▼
   PostgreSQL
````

The pipeline accepts a search query and record limit, retrieves matching records from Open Library, transforms the required fields, validates the data, prevents duplicate records, and stores the results in PostgreSQL.

## 🛠️ Tech Stack

* **Python 3.10** — ETL pipeline and scraper implementation
* **Requests** — API requests
* **Psycopg 3** — PostgreSQL connectivity
* **PostgreSQL 14** — data storage
* **Docker & Docker Compose** — containerization
* **Git & GitHub** — version control

## 📁 Project Structure

```text
Web-Data-ETL-Pipeline/
│
├── src/
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── openlibrary.py
│   │
│   ├── __init__.py
│   └── openlibrary_postgres.py
│
├── sql/
│   └── schema.sql
│
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## ⚙️ Pipeline Workflow

1. Accept a book search query and record limit.
2. Extract book data from the Open Library Search API.
3. Transform the API response into a structured format.
4. Validate required `openlibrary_key` values.
5. Load valid records into PostgreSQL.
6. Prevent duplicate records using the Open Library work key.
7. Report newly stored records and skipped duplicates.

### Data Fields

* `openlibrary_key`
* `title`
* `author`
* `year`

## 🐳 Running the Pipeline

### 1. Start PostgreSQL

```bash
docker compose up -d psql-db
```

### 2. Run the ETL pipeline

```bash
docker compose run --rm -it python_service
```

Enter a search query and the number of records to retrieve:

```text
🔎 Search for a book: python
📚 How many books do you want? 5
```

The pipeline extracts the requested records, validates them, and stores unique records in PostgreSQL.

## 🗄️ Database

The pipeline stores the processed data in a PostgreSQL `books` table.

| Column            | Type         |
| ----------------- | ------------ |
| `id`              | SERIAL       |
| `openlibrary_key` | VARCHAR(255) |
| `title`           | VARCHAR(255) |
| `author`          | VARCHAR(255) |
| `year`            | INTEGER      |

`openlibrary_key` is configured as `NOT NULL` and `UNIQUE` to prevent duplicate records.

The database schema is initialized from:

```text
sql/schema.sql
```

## 🔍 Verify Stored Data

### Check the number of records

```bash
docker compose exec psql-db \
psql -U postgres -d demo \
-c "SELECT COUNT(*) AS total_records FROM books;"
```

### View all stored records

```bash
docker compose exec psql-db \
psql -U postgres -d demo \
-c "SELECT * FROM books ORDER BY id;"
```

### Check storage used by the `books` table

```bash
docker compose exec psql-db \
psql -U postgres -d demo \
-c "SELECT pg_size_pretty(pg_total_relation_size('books')) AS books_storage;"
```

### Check total database size

```bash
docker compose exec psql-db \
psql -U postgres -d demo \
-c "SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;"
```

### Check for duplicate records

```bash
docker compose exec psql-db \
psql -U postgres -d demo \
-c "SELECT openlibrary_key, COUNT(*) FROM books GROUP BY openlibrary_key HAVING COUNT(*) > 1;"
```

If no rows are returned, there are no duplicate Open Library records.

## 🧩 Extensible Architecture

The scraper design separates source-specific extraction logic from the rest of the pipeline.

```text
BaseScraper
      │
      └── OpenLibraryScraper
```

Additional web/API sources can be added by implementing new scraper classes based on the `BaseScraper` interface, without redesigning the PostgreSQL loading layer.

## 🔮 Future Improvements

* Add automated unit and integration tests
* Add structured logging and improved error handling
* Support additional web/API data sources
* Add GitHub Actions CI
* Add scheduled pipeline execution
* Add analytical SQL queries and visualizations

## 📌 Project Status

**Functional end-to-end ETL pipeline**

The current implementation successfully extracts data from Open Library, transforms and validates the records, prevents duplicates, and loads the processed data into PostgreSQL through Dockerized services.

