# Credit Approval System (Django + DRF + Celery)

## Run
1. Copy `.env.example` to `.env`
2. Ensure `data/customer_data.xlsx` and `data/loan_data.xlsx` exist (this archive includes copies).
3. `docker compose up --build`

### Endpoints
- POST /register
- POST /check-eligibility
- POST /create-loan
- GET /view-loan/<loan_id>
- GET /view-loans/<customer_id>

Business rules and ingestion match the assignment.
