import pandas as pd
from celery import shared_task
from django.db import transaction
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Customer, Loan
from .utils import monthly_emi


@shared_task
def ingest_from_excel(customer_path: str = "data/customer_data.xlsx", loan_path: str = "data/loan_data.xlsx"):
    try:
        with transaction.atomic():
            # ----------- CUSTOMER DATA -----------
            cdf = pd.read_excel(customer_path)
            for _, row in cdf.iterrows():
                phone = str(row.get("phone_number", "")).strip()
                # Skip rows with missing or empty phone numbers
                if not phone:
                    continue

                # Safely extract customer_id if it exists
                cid = None
                if "customer_id" in row and not pd.isna(row["customer_id"]):
                    try:
                        cid = int(row["customer_id"])
                    except Exception:
                        cid = None

                defaults = {
                    "first_name": str(row.get("first_name", "")).strip(),
                    "last_name": str(row.get("last_name", "")).strip(),
                    "phone_number": phone,
                    "monthly_salary": int(row.get("monthly_salary", 0)),
                    "approved_limit": int(row.get("approved_limit", 0)),
                    "current_debt": int(row.get("current_debt", 0)),
                }

                # Update or create customer safely, skipping duplicates
                if cid and Customer.objects.filter(id=cid).exists():
                    Customer.objects.filter(id=cid).update(**defaults)
                elif not Customer.objects.filter(phone_number=phone).exists():
                    Customer.objects.create(**defaults)

            # ----------- LOAN DATA -----------
            ldf = pd.read_excel(loan_path)
            for _, row in ldf.iterrows():
                # Handle multiple possible column names
                cid = row.get("customer id") or row.get("customer_id")
                if pd.isna(cid):
                    continue

                try:
                    customer = Customer.objects.get(id=int(cid))
                except Customer.DoesNotExist:
                    continue

                tenure = int(row.get("tenure", 0) or 0)
                rate = float(row.get("interest rate", 0) or 0)
                amount = float(row.get("loan amount", 0) or 0)

                emi = float(
                    row.get("monthly repayment (emi)", monthly_emi(amount, rate, tenure))
                )
                emis_on_time = int(row.get("EMIs paid on time", 0) or 0)

                # Handle start/end dates safely
                sd = pd.to_datetime(row.get("start date"), errors="coerce")
                ed = pd.to_datetime(row.get("end date"), errors="coerce")
                start_date = sd.date() if not pd.isna(sd) else timezone.now().date()
                end_date = (
                    ed.date()
                    if not pd.isna(ed)
                    else (start_date + relativedelta(months=tenure))
                )

                lid = None
                if "loan id" in row and not pd.isna(row["loan id"]):
                    lid = int(row["loan id"])

                defaults = {
                    "customer": customer,
                    "loan_amount": amount,
                    "tenure": tenure,
                    "interest_rate": rate,
                    "monthly_installment": emi,
                    "emis_paid_on_time": emis_on_time,
                    "start_date": start_date,
                    "end_date": end_date,
                    "active": end_date >= timezone.now().date(),
                }

                if lid and Loan.objects.filter(id=lid).exists():
                    Loan.objects.filter(id=lid).update(**defaults)
                else:
                    Loan.objects.create(**defaults)

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "error": str(e)}
