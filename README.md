# 🏦 Credit Approval System

A **Django + Docker-based Credit Approval System** that automates customer registration, eligibility checks, loan creation, and viewing loan details — all via REST APIs.  
Tested using **Postman**, this project demonstrates a complete API workflow integrated with **PostgreSQL**, **Redis**, and **Celery** using **Docker Compose**.

---

## 📚 Table of Contents
1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [System Architecture](#system-architecture)
4. [Setup & Installation](#setup--installation)
5. [Running the Project](#running-the-project)
6. [API Endpoints](#api-endpoints)
7. [Example API Requests](#example-api-requests)
8. [Testing with Postman](#testing-with-postman)
9. [Screenshots](#screenshots)
10. [Common Issues & Fixes](#common-issues--fixes)
11. [License](#license)
12. [Author](#author)

---

## 🧠 Overview

The **Credit Approval System** is designed to streamline the loan approval process using a rules-based engine.  
It lets users:
- Register new customers  
- Check their loan eligibility  
- Create and approve loans automatically based on credit policy  
- View loan details and history  

The project runs seamlessly inside Docker containers and exposes a simple REST API for all actions.

---

## ⚙️ Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Backend** | Django 5.2 |
| **API Framework** | Django REST Framework |
| **Database** | PostgreSQL |
| **Cache / Broker** | Redis |
| **Task Queue** | Celery |
| **Containerization** | Docker & Docker Compose |
| **Testing** | Postman |
| **Language** | Python 3.11 |

---

## 🏗️ System Architecture

+-------------------+
| Postman |
+---------+---------+
|
v
+---------+---------+
| Django Backend |
| REST API + Celery |
+---------+---------+
|
v
+-------------------+
| PostgreSQL (DB) |
| Redis (Broker) |
+-------------------+

yaml
Copy code

---

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/credit-approval-system.git
cd credit-approval-system
2️⃣ Build Docker Containers
bash
Copy code
docker compose build
3️⃣ Run the Containers
bash
Copy code
docker compose up
After successful setup:

Web App → http://localhost:8000

Database (Postgres) → port 5432

Redis → port 6379

▶️ Running the Project (Inside Docker)
Open a shell inside the web container:

bash
Copy code
docker compose exec web bash
Apply database migrations:

bash
Copy code
python manage.py migrate
Create a Django superuser:

bash
Copy code
python manage.py createsuperuser
🔗 API Endpoints
Endpoint	Method	Description
/register/	POST	Register a new customer
/check-eligibility/	POST	Check if a customer is eligible for a loan
/create-loan/	POST	Create a loan based on eligibility
/view-loan/<loan_id>/	GET	View details of a specific loan
/view-loans/<customer_id>/	GET	View all loans for a specific customer

🧾 Example API Requests
✅ Register a Customer
POST /register/

json
Copy code
{
  "first_name": "Shubham",
  "last_name": "Agarwal",
  "phone_number": "9998887770",
  "age": 28,
  "monthly_income": 80000
}
Response

json
Copy code
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

json
Copy code
{
  "customer_id": 34,
  "loan_amount": 100000,
  "interest_rate": 10,
  "tenure": 12
}
Response (Approved)

json
Copy code
{
  "loan_id": 7,
  "loan_approved": true,
  "message": "Loan approved successfully.",
  "monthly_installment": 8791.59
}
Response (Rejected)

json
Copy code
{
  "loan_id": null,
  "loan_approved": false,
  "message": "Loan not approved based on credit policy.",
  "monthly_installment": 43957.94
}
🧾 View Loan Details
GET /view-loan/7/

json
Copy code
{
  "loan_id": 7,
  "customer_id": 34,
  "loan_amount": 100000,
  "tenure": 12,
  "monthly_installment": 8791.59,
  "status": "Approved"
}
🧪 Testing with Postman
Steps:

Open Postman

Create a collection named Credit Approval System

Add requests:

POST /register

POST /check-eligibility

POST /create-loan

GET /view-loan/<loan_id>

GET /view-loans/<customer_id>

For POST requests, choose Body → raw → JSON

Click Send to execute

🖼️ Screenshots
Description	Screenshot
✅ Register API Success	
💰 Loan Approved	
❌ Loan Rejected	
🧾 View Loan Details	
🐳 Docker Containers Running	
⚙️ Common Issues Fix Examples	
✅ Final Working Output	

⚙️ Common Issues & Fixes
Issue	Cause	Fix
404 Not Found	Using /view-loan/<loan_id>/ literally	Replace <loan_id> with an actual number, e.g. /view-loan/7/
loan_id = null	Loan not approved	Try lowering loan_amount or increasing income
“Invalid protocol” in Postman	Incorrect URL	Ensure http://localhost:8000/...
curl not found	Curl not installed	Run apt-get install curl in web container
Database not connecting	Containers not started	Run docker compose up before API tests

🧰 Useful Docker Commands
bash
Copy code
# List running containers
docker ps

# Enter Django container shell
docker compose exec web bash

# Restart the web container
docker compose restart web

# Stop all containers
docker compose down

![1](https://github.com/SHUBHAG100520/credit-approval-system/blob/main/ss/1.jpg)

### 🗣️ Voice / TTS Feature
![Voice Feature](https://raw.githubusercontent.com/SHUBHAG100520/credit-approval-system/main/ss/4.jpg)

### 🖼️ Image Generation
![Image Generation](https://raw.githubusercontent.com/SHUBHAG100520/credit-approval-system/main/ss/5.jpg)

### 🌗 Dark Mode
![Dark Mode](https://raw.githubusercontent.com/SHUBHAG100520/credit-approval-system/main/ss/6.jpg)

### 📄 Export as PDF
![PDF Export](https://raw.githubusercontent.com/SHUBHAG100520/credit-approval-system/main/ss/7.jpg)

### 💾 Saved Plan Example
![Saved Plan](https://raw.githubusercontent.com/SHUBHAG100520/credit-approval-system/main/ss/8.jpg)

### 💬 Motivation Quotes
![Motivation Quotes](https://raw.githubusercontent.com/SHUBHAG100520/credit-approval-system/main/ss/9.jpg)



📜 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute this code for personal or educational purposes.

👨‍💻 Author
Shubham Agarwal
💼 Backend Developer | Data & API Enthusiast
📧 shubhag0411@gmail.com
🌐 GitHub Profile
