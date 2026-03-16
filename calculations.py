"""
Financial calculation helpers: mortgage, STR income, cash flow, cap rate, etc.
"""

import numpy as np


def monthly_mortgage(price: float, down_pct: float, rate_annual: float, term_years: int) -> float:
    """Standard amortizing monthly mortgage payment."""
    loan = price * (1 - down_pct / 100)
    r = rate_annual / 100 / 12
    n = term_years * 12
    if r == 0:
        return loan / n
    return loan * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


def total_cash_to_close(price: float, down_pct: float, closing_cost_pct: float = 2.5) -> float:
    down = price * down_pct / 100
    closing = price * closing_cost_pct / 100
    return down + closing


def amortization_schedule(price: float, down_pct: float, rate_annual: float, term_years: int):
    """Returns list of dicts with year-end balances, cumulative interest/principal."""
    loan = price * (1 - down_pct / 100)
    r = rate_annual / 100 / 12
    n = term_years * 12
    pmt = monthly_mortgage(price, down_pct, rate_annual, term_years)

    balance = loan
    schedule = []
    cum_interest = 0
    cum_principal = 0

    for year in range(1, term_years + 1):
        yr_interest = 0
        yr_principal = 0
        for _ in range(12):
            interest = balance * r
            principal = pmt - interest
            balance -= principal
            yr_interest += interest
            yr_principal += principal
        cum_interest += yr_interest
        cum_principal += yr_principal
        schedule.append({
            "year": year,
            "balance": max(balance, 0),
            "yr_interest": yr_interest,
            "yr_principal": yr_principal,
            "cum_interest": cum_interest,
            "cum_principal": cum_principal,
        })

    return schedule


def str_monthly_revenue(
    nightly_rate: float,
    occupancy: float,
    platform_fee_pct: float = 0.03,
) -> float:
    """Gross revenue after platform fee."""
    days = 30 * occupancy
    gross = days * nightly_rate
    return gross * (1 - platform_fee_pct)


def str_monthly_expenses(
    home_value: float,
    market_key: str,
    monthly_revenue: float,
    self_manage: bool,
    avg_stays_per_mo: float,
    costs: dict,
) -> dict:
    """Returns breakdown of monthly STR operating expenses."""
    mgmt = 0 if self_manage else monthly_revenue * costs["mgmt_fee_pct"]
    cleaning = avg_stays_per_mo * costs["cleaning_per_stay"]
    supplies = costs["supplies_monthly"]
    utilities = costs["utilities_monthly"]
    insurance = costs["insurance_annual"] / 12
    maintenance = home_value * costs["maintenance_pct"] / 12
    platform = monthly_revenue * costs["platform_fee_pct"]  # already subtracted above

    return {
        "Management": mgmt,
        "Cleaning": cleaning,
        "Supplies": supplies,
        "Utilities": utilities,
        "Insurance": insurance,
        "Maintenance": maintenance,
    }


def property_tax_monthly(home_value: float, tax_rate: float) -> float:
    return home_value * tax_rate / 12


def cap_rate(annual_noi: float, purchase_price: float) -> float:
    return annual_noi / purchase_price


def gross_rent_multiplier(purchase_price: float, annual_gross_revenue: float) -> float:
    return purchase_price / annual_gross_revenue


def cash_on_cash_return(annual_cash_flow: float, total_cash_invested: float) -> float:
    return annual_cash_flow / total_cash_invested


def break_even_occupancy(
    monthly_mortgage: float,
    monthly_fixed_expenses: float,
    nightly_rate: float,
    platform_fee_pct: float = 0.03,
) -> float:
    """Occupancy rate needed to break even (cover mortgage + fixed costs)."""
    net_per_night = nightly_rate * (1 - platform_fee_pct)
    nights_needed = (monthly_mortgage + monthly_fixed_expenses) / net_per_night
    return nights_needed / 30


def price_appreciation(current_price: float, yoy_rate: float, years: int) -> list:
    """Project home value over N years."""
    return [current_price * (1 + yoy_rate) ** y for y in range(years + 1)]


def total_return(
    equity_gain: float,
    cum_cash_flow: float,
    initial_investment: float,
    years: int,
) -> float:
    """Annualized total return (simple)."""
    total = equity_gain + cum_cash_flow
    return (total / initial_investment) / years
