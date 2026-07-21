# Whisky Market Data API

A FastAPI data API for uploading, validating, cleaning, storing and analysing whisky auction market data.

This project is designed as a production-style portfolio project that demonstrates API development, messy data cleaning, SQL storage, automated testing and analytics endpoint design.

The repository uses synthetic sample data only. It is inspired by real-world scraping and analytics work, but does not include private or proprietary datasets.

---

## What the API Does

The API accepts a whisky auction CSV file, validates the expected schema, cleans messy scraped fields, stores the cleaned auction lots in SQLite, and exposes query and analytics endpoints.

Current data flow:

```text
CSV upload
→ required-column validation
→ data cleaning and parsing
→ upload summary
→ SQLite storage
→ query and analytics endpoints