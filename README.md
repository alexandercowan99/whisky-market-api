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

---

## Running with Docker

This project can also be run in a Docker container.

Build the image:

```bash
docker build -t whisky-market-api .

## Machine Learning: Price Prediction

The project includes a baseline machine learning layer for predicting whisky auction result prices.

The current model is a simple linear regression baseline trained on synthetic sample data. It uses the following numeric features:

- `estimate_low`
- `estimate_high`
- `size_ml`
- `quantity`

The target variable is:

- `result_price`

This model is intentionally simple. The aim of this stage is to demonstrate a production-style ML workflow:

```text
cleaned data
→ feature preparation
→ train/test evaluation
→ saved model artefact
→ API-based inference