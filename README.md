# 📚 OpenLibrary Data Pipeline

A containerized data engineering pipeline that extracts book data from the Open Library API, transforms the response into a structured format, and loads the results into PostgreSQL.

## 🚀 Overview

This project demonstrates a simple **ETL (Extract, Transform, Load)** workflow using Python, Docker, and PostgreSQL.

```text
Open Library API
       │
       ▼
   Python ETL
       │
       ├── Extract
       ├── Transform
       └── Load
       │
       ▼
   PostgreSQL

The pipeline accepts a book-related search query, retrieves matching records from Open Library, processes the relevant fields, and stores the results in a PostgreSQL database.

##  🛠️ Tech Stack
Python 3.10
Requests – API requests
BeautifulSoup / html5lib – web/data parsing dependencies
Psycopg 3 – PostgreSQL connectivity
PostgreSQL 14 – data storage
Docker & Docker Compose – containerization
##  📁 Project Structure
```
OpenLibrary-Data-Pipeline/
│
├── src/
│   └── openlibrary_postgres.py
│
├── sql/
│   └── schema.sql
│
├── tests/
│
├── docs/
│
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

##  ⚙️ How It Works
The user provides a book search query.
Python sends the query to the Open Library Search API.
The API returns book metadata.
The pipeline extracts:
Book title
Author
First publication year
The transformed records are inserted into PostgreSQL.
The stored data can then be queried using SQL.

## 🐳 Running the Pipeline

Start PostgreSQL:
```
docker compose up -d psql-db
```
Run the Python pipeline:
```
docker compose run --rm -it python_service
```
Enter a search query when prompted:

🔎 Search for a book: python

## 🗄️ Database

The PostgreSQL database contains a books table with the following fields:
```
Column	Type
id	SERIAL
title	VARCHAR(255)
author	VARCHAR(255)
year	INT
```

The database schema is automatically initialized using:
```
sql/schema.sql
```

## 🔍 Verify the Data

Check the number of records:
```
docker compose exec psql-db \
psql -U postgres -d demo \
-c "SELECT COUNT(*) FROM books;"
```

View the stored records:
```
docker compose exec psql-db \
psql -U postgres -d demo \
-c "SELECT * FROM books;"
```

## 📊 Example

A search for python retrieves book records such as:

Learning Python
Python For Data Analysis
Fluent Python
Black Hat Python
Python Cookbook

The records are then persisted in PostgreSQL for further querying and analysis.

### 🔮 Future Improvements
Separate extraction, transformation, and loading into independent modules
Add data validation and duplicate handling
Add automated tests
Improve database schema and constraints
Add logging and error handling
Support configurable API query limits
Add analytical SQL queries
Add a data visualization/dashboard layer
Introduce scheduled pipeline execution

### Then create it

From:

```bash
cd ~/OpenLibrary-Data-Pipeline
```
