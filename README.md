````markdown
# 🌐 Web Data ETL Pipeline

An extensible, containerized ETL pipeline that extracts structured data from web APIs, transforms and validates the records, and loads them into PostgreSQL.

The project currently uses the **Open Library API** as its data source and follows a reusable scraper architecture that can be extended to support additional web/API sources.

## 🚀 Overview

```text
Web/API Source
      │
      ▼
  Base Scraper
      │
      ▼
Source-specific Scraper
   (Open Library)
      │
      ▼
Extract → Transform → Validate
      │
      ▼
  PostgreSQL
````

The pipeline accepts a search query and record limit, retrieves matching records from Open Library, transforms the required fields, validates the data, and stores unique records in PostgreSQL.

## 🛠️ Tech Stack

* **Python 3.10**
* **Requests** — API requests
* **PostgreSQL 14** — data storage
* **psycopg2** — PostgreSQL connectivity
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
5. Load unique records into PostgreSQL.
6. Skip duplicate records using the Open Library work key.

### Data Fields

* `openlibrary_key`
* `title`
* `author`
* `year`

## 🐳 Running the Pipeline

### Start PostgreSQL

```bash
docker compose up -d psql-db
```

### Run the pipeline

```bash
docker compose run --rm -it python_service
```

Example:

```text
🔎 Search for a book: python
📚 How many books do you want? 5
```

The pipeline reports newly stored records and skipped duplicates.

## 🗄️ Database

The pipeline stores data in a PostgreSQL `books` table:

| Column            | Type         |
| ----------------- | ------------ |
| `id`              | SERIAL       |
| `openlibrary_key` | VARCHAR(255) |
| `title`           | VARCHAR(255) |
| `author`          | VARCHAR(255) |
| `year`            | INTEGER      |

`openlibrary_key` is configured as `NOT NULL` and `UNIQUE` to prevent duplicate records.

The schema is initialized from:

```text
sql/schema.sql
```

## 🔍 Verify Stored Data

```bash
docker compose exec psql-db \
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
-c "SELECT * FROM books;"
```

## 🧩 Extensible Architecture

The scraper design separates source-specific logic from the rest of the pipeline:

```text
BaseScraper
    │
    ├── OpenLibraryScraper
    │
    ├── FutureScraper
    │
    └── FutureScraper
```

Additional web/API sources can be implemented using the same scraper structure without redesigning the database loading layer.

## 🔮 Future Improvements

* Add automated unit and integration tests
* Add structured logging and improved error handling
* Support additional web/API data sources
* Add GitHub Actions CI
* Add scheduled pipeline execution
* Add analytical SQL queries and visualizations

## 📌 Project Status

**Functional end-to-end ETL pipeline**

The current implementation successfully extracts data from Open Library, transforms and validates the records, prevents duplicates, and loads the data into PostgreSQL through Dockerized services.

```
```
