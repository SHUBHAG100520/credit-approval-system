from django.utils import timezone

def round_to_nearest_lakh(value: float) -> int:
    return int(round(value / 100000.0) * 100000)

def monthly_emi(principal: float, annual_rate_percent: float, months: int) -> float:
    r = (annual_rate_percent / 100.0) / 12.0
    if r == 0:
        return round(principal / months, 2) if months else 0.0
    num = principal * r * (1 + r) ** months
    den = (1 + r) ** months - 1
    return round(num / den, 2)

def credit_score_components(customer, loans_qs):
    current_active = loans_qs.filter(active=True)
    active_principal = sum(l.loan_amount for l in current_active)
    if active_principal > customer.approved_limit:
        return 0

    total_emis = sum(l.tenure for l in loans_qs)
    ontime_emis = sum(l.emis_paid_on_time for l in loans_qs)
    ontime_ratio = (ontime_emis / total_emis) if total_emis else 1.0

    A = int(ontime_ratio * 40)
    n = loans_qs.count()
    B = max(0, 20 - 2 * max(0, n - 5))
    this_year = timezone.now().year
    recent = loans_qs.filter(start_date__year=this_year).count()
    C = max(0, 15 - 5 * max(0, recent - 1))
    total_volume = sum(l.loan_amount for l in loans_qs)
    util = total_volume / customer.approved_limit if customer.approved_limit else 0
    if util <= 0.5:
        D = 25
    elif util <= 1.0:
        D = 18
    elif util <= 1.5:
        D = 10
    else:
        D = 5
    score = A + B + C + D
    return min(100, max(0, int(score)))

def interest_slab_min_rate(score: int) -> float:
    if score > 50:
        return 0.0
    if 30 < score <= 50:
        return 12.0
    if 10 < score <= 30:
        return 16.0
    return float("inf")
