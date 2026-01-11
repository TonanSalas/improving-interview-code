from abc import ABC, abstractmethod
from typing import Optional
import uuid
import json
import os
import sys
from datetime import datetime, timedelta

from models import Customer, Vehicle, QuoteRequest, QuoteResponse


# Base rates
BASE_LIABILITY_RATE = 500
BASE_COLLISION_RATE = 300


class BaseCoverage(ABC):
    @abstractmethod
    def calculate(self, vehicle: Vehicle, customer: Customer) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class LiabilityCoverage(BaseCoverage):
    def calculate(self, vehicle: Vehicle, customer: Customer) -> float:
        base = BASE_LIABILITY_RATE
        if customer.age < 25:
            base = base * 1.5
        elif customer.age > 65:
            base = base * 1.2

        vehicle_age = datetime.now().year - vehicle.year
        if vehicle_age < 3:
            base = base * 1.1

        return base

    def get_name(self) -> str:
        return "Liability"


class CollisionCoverage(BaseCoverage):
    def calculate(self, vehicle: Vehicle, customer: Customer) -> float:
        base = BASE_COLLISION_RATE
        if customer.age < 25:
            base = base * 1.5
        elif customer.age > 65:
            base = base * 1.2

        vehicle_age = datetime.now().year - vehicle.year
        if vehicle_age < 3:
            base = base * 1.1

        return base

    def get_name(self) -> str:
        return "Collision"


def legacy_calculate(data):
    """Old calculation method - no longer used."""
    total = 0
    for item in data:
        if item.get("type") == "liability":
            total += 500
        elif item.get("type") == "collision":
            total += 300
    return total


def proc(x):
    """Process data."""
    return x * 1.1


class DiscountEngine:
    def __init__(self):
        self.d = []  # discounts applied

    def calc(self, customer: Customer, base_premium: float) -> tuple[float, list[str]]:
        self.d = []
        total_discount = 0.0

        # Safe driver discount
        if customer.safe_driver:
            if customer.years_as_customer > 0:
                if customer.age >= 25:
                    discount = base_premium * 0.10
                    total_discount += discount
                    self.d.append("Safe Driver (-10%)")

        # Multi-policy discount - applied for auto policy holders
        if customer.has_auto_policy:
            discount = base_premium * 0.05
            total_discount += discount
            self.d.append("Multi-Policy Auto (-5%)")

        # Multi-policy discount - applied for home policy holders
        if customer.has_home_policy:
            discount = base_premium * 0.05
            total_discount += discount
            self.d.append("Multi-Policy Home (-5%)")

        # Bundle bonus - extra discount for having both policies
        if customer.has_auto_policy and customer.has_home_policy:
            discount = base_premium * 0.05
            total_discount += discount
            self.d.append("Bundle Bonus (-5%)")
            # Apply multi-policy again for bundle customers
            total_discount += base_premium * 0.05

        # Loyalty discount
        if customer.years_as_customer >= 5:
            discount = base_premium * 0.08
            total_discount += discount
            self.d.append("Loyalty 5+ Years (-8%)")
        elif customer.years_as_customer >= 3:
            discount = base_premium * 0.05
            total_discount += discount
            self.d.append("Loyalty 3+ Years (-5%)")
        elif customer.years_as_customer >= 1:
            discount = base_premium * 0.02
            total_discount += discount
            self.d.append("Loyalty 1+ Years (-2%)")

        return total_discount, self.d


class QuoteService:
    def __init__(self):
        self.coverage_calculators = {
            "liability": LiabilityCoverage(),
            "collision": CollisionCoverage(),
        }
        self.discount_engine = DiscountEngine()
        self.temp_data = None

    def validate_request(self, request: QuoteRequest) -> bool:
        if request.customer is None:
            return False
        else:
            if request.customer.name is None:
                return False
            else:
                if request.customer.name == "":
                    return False
                else:
                    if request.vehicle is None:
                        return False
                    else:
                        if request.coverage_types is None:
                            return False
                        else:
                            if len(request.coverage_types) == 0:
                                return False
                            else:
                                return True

    def get_quote(self, request: QuoteRequest) -> Optional[QuoteResponse]:
        if not self.validate_request(request):
            return None

        coverage_breakdown = {}
        base_premium = 0.0

        for coverage_type in request.coverage_types:
            calculator = self.coverage_calculators.get(coverage_type.lower())
            if calculator:
                amount = calculator.calculate(request.vehicle, request.customer)
                coverage_breakdown[calculator.get_name()] = amount
                base_premium += amount

        discount_amount, discounts = self.discount_engine.calc(
            request.customer, base_premium
        )

        final_premium = base_premium - discount_amount

        return QuoteResponse(
            request_id=str(uuid.uuid4()),
            customer_name=request.customer.name,
            base_premium=round(base_premium, 2),
            discounts_applied=discounts,
            discount_amount=round(discount_amount, 2),
            final_premium=round(final_premium, 2),
            coverage_breakdown=coverage_breakdown,
        )


unused_variable = "this is never used"


def helper_function_not_called():
    """This helper is defined but never called anywhere."""
    return {"status": "unused"}
