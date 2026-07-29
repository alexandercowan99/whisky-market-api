# Whisky Market Data API

A FastAPI project for ingesting, cleaning, storing and analysing synthetic whisky auction data.

The API accepts CSV uploads, validates the expected columns, cleans scraped auction fields, stores the results through SQLAlchemy, exposes query and analytics endpoints, and serves a simple baseline price prediction model.

I built this as a portfolio project to practise production-style Python data work: API design, data validation, SQL storage, testing, Docker, model serving and cloud deployment.

The repository contains synthetic sample data only. It does not include private, client-owned or proprietary datasets.

---

## Project Status

Portfolio v2 complete.

The project includes:

- CSV upload and required-column validation
- cleaning and parsing for auction result fields
- duplicate handling based on `Lot_Link`
- SQLite and PostgreSQL support through SQLAlchemy
- query and analytics endpoints
- automated tests with pytest
- Docker and Docker Compose support
- a baseline price prediction workflow
- model inference through FastAPI
- an AWS deployment using ECR, ECS Fargate and RDS PostgreSQL
- GitHub Actions for tests and automated ARM64 image publishing

The ML model is deliberately simple. The main focus is the workflow around the model: feature preparation, train/test evaluation, saving and loading the model, input validation, and serving predictions through an API.

---

## What the API Does

```text
CSV upload
→ required-column validation
→ data cleaning and parsing
→ duplicate checking
→ SQL storage
→ query, analytics and prediction endpoints
```

Main endpoints:

```text
GET  /health
POST /sales/upload
GET  /sales/lots
GET  /sales/summary
GET  /sales/top-lots
GET  /sales/auction-houses
GET  /sales/monthly-summary
POST /sales/predict-price
```

Interactive API documentation is available locally at:

```text
http://localhost:8000/docs
```

---

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- PostgreSQL
- pandas
- scikit-learn
- joblib
- pytest
- Docker and Docker Compose
- GitHub Actions
- AWS ECR
- AWS ECS Fargate
- AWS RDS for PostgreSQL
- AWS Secrets Manager
- Amazon CloudWatch

---

## Run Modes

### Local development

```text
FastAPI
→ local SQLite database file
```

### Docker Compose

```text
FastAPI container
→ PostgreSQL container
```

### Automated tests

```text
pytest
→ temporary SQLite test database
```

### AWS deployment demonstration

```text
GitHub Actions
→ OIDC authentication
→ Amazon ECR
→ ECS Fargate
→ FastAPI container
→ RDS PostgreSQL

Secrets Manager
→ DATABASE_URL

FastAPI logs
→ CloudWatch
```

The application reads its database connection from the `DATABASE_URL` environment variable. When the variable is not set, it falls back to:

```text
sqlite:///./whisky_market.db
```

This keeps local development lightweight while allowing PostgreSQL to be used in Docker Compose and AWS.

---

## Local Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest
```

Train the baseline model:

```bash
python -m scripts.train_price_model
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

---

## Docker Compose with PostgreSQL

An example environment file is provided:

```text
.env.example
```

Docker Compose also includes local default values. To customise them:

```bash
cp .env.example .env
```

The `.env` file is ignored by Git so private local values are not committed.

Start the API and PostgreSQL services:

```bash
docker compose up --build -d
```

Check their status:

```bash
docker compose ps
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

Stop the services:

```bash
docker compose down
```

Stop the services and delete the local PostgreSQL volume:

```bash
docker compose down -v
```

### Check PostgreSQL data

After uploading the sample CSV, count the stored rows:

```bash
docker compose exec postgres \
  psql -U whisky_user -d whisky_market \
  -c "SELECT COUNT(*) FROM auction_lots;"
```

Expected result after one sample upload:

```text
 count
-------
    10
(1 row)
```

List the database tables:

```bash
docker compose exec postgres \
  psql -U whisky_user -d whisky_market \
  -c "\\dt"
```

You should see the `auction_lots` table.

---

## Duplicate Upload Handling

The upload endpoint identifies duplicate auction lots using `Lot_Link`.

Uploading the same sample CSV for a second time returns a response similar to:

```json
{
  "rows_received": 10,
  "rows_inserted": 0,
  "duplicates_skipped": 10
}
```

---

## Sample Data

The public repository includes synthetic sample data at:

```text
data/sample/sample_auction_lots.csv
```

Real and private data is excluded.

---

## Machine Learning: Price Prediction

The project includes a linear regression baseline for predicting whisky auction result prices.

Features:

- `estimate_low`
- `estimate_high`
- `size_ml`
- `quantity`

Target:

- `result_price`

Workflow:

```text
cleaned data
→ feature preparation
→ train/test evaluation
→ saved model artefact
→ API prediction
```

The sample dataset is small and synthetic, so the model metrics are a smoke test of the end-to-end ML pipeline rather than evidence of commercial predictive accuracy.

Train the model with:

```bash
python -m scripts.train_price_model
```

This creates:

```text
models/price_model.joblib
```

Generated model files are ignored by Git and can be recreated from the training script.

Example training output:

```json
{
  "training_rows": 7,
  "test_rows": 3,
  "train_mae": 2.62,
  "test_mae": 4.26,
  "test_r2": 0.9787,
  "model_path": "models/price_model.joblib"
}
```

### Prediction endpoint

Use:

```text
POST /sales/predict-price
```

Example request:

```json
{
  "estimate_low": 400,
  "estimate_high": 550,
  "size_ml": 700,
  "quantity": 1
}
```

Example response:

```json
{
  "predicted_price": 451.8,
  "model_version": "baseline-linear-regression-v1"
}
```

When the model file is unavailable, the endpoint returns `503 Service Unavailable` with instructions to train the model.

---

## AWS Deployment Demonstration

The Docker image was deployed temporarily to ECS Fargate and connected to a private RDS PostgreSQL instance.

The deployment used:

- ECR to store the Docker image
- ECS Fargate to run the FastAPI container
- RDS PostgreSQL for persistent storage
- Secrets Manager to supply `DATABASE_URL`
- security groups to restrict database access to the API task
- CloudWatch for container logs
- an ARM64 task and Docker image

A persistence test was completed by:

1. uploading 10 sample records through the live API;
2. stopping and replacing the Fargate task;
3. querying the replacement task without uploading the CSV again; and
4. confirming that all 10 records remained in RDS.

This demonstrated that application containers could be replaced without losing database data.

The AWS setup was a temporary portfolio deployment rather than a continuously hosted production service. A production version would normally add a stable ECS service, HTTPS, a load balancer or another stable endpoint, a custom domain, database migrations, health-based recovery and fuller monitoring.

---

## GitHub Actions and ECR Publishing

The workflow in `.github/workflows/tests.yml` runs the automated tests for pushes and pull requests.

For successful pushes to `main`, it also:

1. requests a temporary GitHub OIDC identity token;
2. assumes a repository-restricted AWS IAM role;
3. logs in to ECR;
4. builds a Linux ARM64 Docker image; and
5. pushes two tags:
   - `latest`
   - the full Git commit SHA

The commit tag links an ECR image back to the exact source-code version that produced it. Permanent AWS access keys are not stored in the GitHub repository.

The workflow publishes the image to ECR but does not automatically launch or update an ECS service.

---

## Testing

Run the full test suite with:

```bash
pytest
```

The suite covers:

- cleaning and parsing logic
- API routes
- SQL repository functions
- serializers
- Pydantic schemas
- ML feature preparation
- model training and evaluation
- model saving and loading
- prediction utilities
- the prediction API endpoint

---

## Security and Deployment Choices

- The container runs as a non-root Linux user.
- The RDS database is not publicly accessible.
- PostgreSQL traffic is restricted to the API task security group.
- The database connection is held in Secrets Manager.
- GitHub uses temporary OIDC credentials rather than permanent AWS keys.
- Pull requests run tests but do not receive AWS deployment credentials.
- The public API security-group rule was restricted for the deployment test.

---

## Notes and Limitations

- The dataset is small and synthetic.
- The model is a baseline demonstration rather than a commercial pricing model.
- Table creation currently occurs through SQLAlchemy at application start; a production system would normally use explicit database migrations.
- The AWS deployment was temporary and did not include an always-running ECS service, load balancer, HTTPS endpoint or custom domain.
- Secrets injected as environment variables are available to the running process, so production systems should also apply strict task access controls and regular secret rotation.
