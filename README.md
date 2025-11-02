🏦 Credit Approval System

A Django + Docker-based Credit Approval System that evaluates customers’ eligibility, registers users, and manages loan creation and tracking — all through REST APIs tested via Postman.

🧩 Table of Contents

Overview

Tech Stack

System Architecture

Setup & Installation

Running the Project

API Endpoints

Testing with Postman

Screenshots

Common Issues & Fixes

License

⚙️ Overview

This project automates the process of credit approval and loan management using machine learning logic (credit rules) integrated with Django REST APIs.

It enables:

Registering new customers

Checking loan eligibility

Creating and viewing loans

Managing loans in PostgreSQL via Docker containers

The APIs are tested using Postman and can easily be extended for production deployments.

🧠 Tech Stack
Component	Technology Used
Backend Framework	Django 5.2
API Layer	Django REST Framework
Database	PostgreSQL
Caching / Task Queue	Redis + Celery
Containerization	Docker + Docker Compose
API Testing	Postman
Language	Python 3.11
🏗️ System Architecture
+-------------------+
|   Postman Client  |
+---------+---------+
          |
          v
+---------+---------+
|   Django (Web)    |  <-- Runs Gunicorn in Docker
|-------------------|
|   REST APIs       |
|   Business Logic  |
|   Celery Worker   |
+---------+---------+
          |
          v
+---------+---------+
| PostgreSQL (DB)   |
+-------------------+
| Redis (Broker)    |
+-------------------+

⚙️ Setup & Installation
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/credit-approval-system.git
cd credit-approval-system

2️⃣ Build Docker Containers
docker compose build

3️⃣ Run Containers
docker compose up


Once running:

Django Web App → http://localhost:8000

PostgreSQL → port 5432

Redis → port 6379

▶️ Running the Project (Inside Docker)

To access the Django shell:

docker compose exec web bash


To apply migrations (if needed):

python manage.py migrate


To create a superuser:

python manage.py createsuperuser

🔗 API Endpoints
Endpoint	Method	Description
/register/	POST	Register a new customer
/check-eligibility/	POST	Check loan eligibility
/create-loan/	POST	Create a loan (approved/rejected based on credit rules)
/view-loan/<loan_id>/	GET	View details of a specific loan
/view-loans/<customer_id>/	GET	View all loans for a customer
📬 Example API Requests
🧾 Register a Customer

POST /register/

{
  "first_name": "Shubham",
  "last_name": "Agarwal",
  "phone_number": "9998887770",
  "age": 28,
  "monthly_income": 80000
}


Response:

{
  "customer_id": 34,
  "name": "Shubham Agarwal",
  "age": 28,
  "monthly_income": 80000,
  "approved_limit": 2000000,
  "phone_number": "9998887770"
}

💰 Create a Loan

POST /create-loan/

{
  "customer_id": 34,
  "loan_amount": 100000,
  "interest_rate": 10,
  "tenure": 12
}


Response:

{
  "loan_id": 7,
  "loan_approved": true,
  "message": "Loan approved successfully.",
  "monthly_installment": 8791.59
}

🧾 View Loan Details

GET /view-loan/7/

Response:

{
  "loan_id": 7,
  "customer_id": 34,
  "loan_amount": 100000,
  "tenure": 12,
  "monthly_installment": 8791.59,
  "status": "Approved"
}

🧪 Testing with Postman

All API endpoints were tested using Postman.

Steps:

Open Postman.

Create a new collection called Credit Approval System.

Add the following requests:

POST /register

POST /check-eligibility

POST /create-loan

GET /view-loan/<loan_id>

GET /view-loans/<customer_id>

Set Body → raw → JSON

Click Send to test each API.

🖼️ Screenshots
Description	Screenshot
✅ Register API Success	

❌ Invalid Loan Request	

✅ Approved Loan	

🧾 View Loan	

⚙️ Docker Containers	

📸 Replace the image paths above with your actual screenshot filenames from Postman and Docker.

🧰 Common Issues & Fixes
Issue	Cause	Fix
404 Not Found	Using /view-loan/<loan_id>/ literally	Replace <loan_id> with actual numeric ID (e.g. /view-loan/7/)
loan_id: null	Loan not approved	Try smaller loan_amount or higher income
Postman “Invalid protocol”	Wrong URL or missing http://	Use http://localhost:8000/... exactly
curl not found	Curl not installed inside Docker	Run apt-get install curl
📜 License

This project is licensed under the MIT License — feel free to use and modify it for your learning or production use.

👨‍💻 Author

Shubham Agarwal
💼 Developer | Data Enthusiast | API Automation Learner
📧 shubhag0411@gmail.com
