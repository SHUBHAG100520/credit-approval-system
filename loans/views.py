from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Customer, Loan
from .serializers import (
    RegisterRequestSerializer, RegisterResponseSerializer,
    CheckEligibilityRequestSerializer, CheckEligibilityResponseSerializer,
    CreateLoanRequestSerializer, CreateLoanResponseSerializer,
)
from .utils import round_to_nearest_lakh, monthly_emi, credit_score_components, interest_slab_min_rate

@api_view(["POST"])
def register_customer(request):
    ser = RegisterRequestSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    data = ser.validated_data
    approved_limit = round_to_nearest_lakh(36 * data["monthly_income"])
    customer = Customer.objects.create(
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        monthly_salary=data["monthly_income"],
        phone_number=data["phone_number"],
        approved_limit=approved_limit,
        current_debt=0,
    )
    out = RegisterResponseSerializer({
        "customer_id": customer.id,
        "name": f"{customer.first_name} {customer.last_name}",
        "age": customer.age,
        "monthly_income": customer.monthly_salary,
        "approved_limit": customer.approved_limit,
        "phone_number": customer.phone_number,
    })
    return Response(out.data, status=status.HTTP_201_CREATED)

def _eligibility_core(customer: Customer, loan_amount: float, interest_rate: float, tenure: int):
    loans_qs = Loan.objects.filter(customer=customer)
    score = credit_score_components(customer, loans_qs)

    current_emis = sum(l.monthly_installment for l in loans_qs if l.active)
    requested_emi = monthly_emi(loan_amount, interest_rate, tenure)
    if current_emis + requested_emi > 0.5 * customer.monthly_salary:
        approve = False
        corrected_rate = interest_rate
    else:
        floor_rate = interest_slab_min_rate(score)
        if floor_rate == float("inf"):
            approve = False
            corrected_rate = interest_rate
        else:
            corrected_rate = max(interest_rate, floor_rate)
            approve = score > 50 or corrected_rate == interest_rate
    emi = monthly_emi(loan_amount, corrected_rate, tenure)
    return approve, corrected_rate, emi, score

@api_view(["POST"])
def check_eligibility(request):
    ser = CheckEligibilityRequestSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    d = ser.validated_data
    customer = get_object_or_404(Customer, id=d["customer_id"])
    approve, corrected_rate, emi, score = _eligibility_core(customer, d["loan_amount"], d["interest_rate"], d["tenure"])
    out = CheckEligibilityResponseSerializer({
        "customer_id": customer.id,
        "approval": approve,
        "interest_rate": d["interest_rate"],
        "corrected_interest_rate": corrected_rate,
        "tenure": d["tenure"],
        "monthly_installment": emi,
    })
    return Response(out.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_loan(request):
    ser = CreateLoanRequestSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    d = ser.validated_data
    customer = get_object_or_404(Customer, id=d["customer_id"])
    approve, corrected_rate, emi, score = _eligibility_core(customer, d["loan_amount"], d["interest_rate"], d["tenure"])
    if not approve and corrected_rate != d["interest_rate"]:
        approve2, corrected_rate2, emi2, score2 = _eligibility_core(customer, d["loan_amount"], corrected_rate, d["tenure"])
        if approve2:
            approve = True
            corrected_rate = corrected_rate2
            emi = emi2
    if not approve:
        out = CreateLoanResponseSerializer({
            "loan_id": None,
            "customer_id": customer.id,
            "loan_approved": False,
            "message": "Loan not approved based on credit policy.",
            "monthly_installment": emi,
        })
        return Response(out.data, status=status.HTTP_200_OK)
    loan = Loan.objects.create(
        customer=customer,
        loan_amount=d["loan_amount"],
        tenure=d["tenure"],
        interest_rate=corrected_rate,
        monthly_installment=emi,
        emis_paid_on_time=0,
        start_date=timezone.now().date(),
    )
    out = CreateLoanResponseSerializer({
        "loan_id": loan.id,
        "customer_id": customer.id,
        "loan_approved": True,
        "message": "Loan approved.",
        "monthly_installment": loan.monthly_installment,
    })
    return Response(out.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def view_loan(request, loan_id: int):
    loan = get_object_or_404(Loan, id=loan_id)
    customer = loan.customer
    payload = {
        "loan_id": loan.id,
        "customer": {
            "id": customer.id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age,
        },
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "monthly_installment": loan.monthly_installment,
        "tenure": loan.tenure,
    }
    return Response(payload, status=status.HTTP_200_OK)

@api_view(["GET"])
def view_loans_for_customer(request, customer_id: int):
    loans = Loan.objects.filter(customer_id=customer_id).order_by("-start_date")
    items = [{
        "loan_id": l.id,
        "loan_amount": l.loan_amount,
        "interest_rate": l.interest_rate,
        "monthly_installment": l.monthly_installment,
        "repayments_left": l.repayments_left,
    } for l in loans]
    return Response(items, status=status.HTTP_200_OK)
