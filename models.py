from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Customer:
    id: str
    name: str
    age: int
    has_auto_policy: bool = False
    has_home_policy: bool = False
    years_as_customer: int = 0
    safe_driver: bool = False


@dataclass
class Vehicle:
    make: str
    model: str
    year: int
    vin: Optional[str] = None


@dataclass
class QuoteRequest:
    customer: Customer
    vehicle: Vehicle
    coverage_types: list[str]
    effective_date: date


@dataclass
class QuoteResponse:
    request_id: str
    customer_name: str
    base_premium: float
    discounts_applied: list[str]
    discount_amount: float
    final_premium: float
    coverage_breakdown: dict[str, float]
