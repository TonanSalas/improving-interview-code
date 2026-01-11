import pytest
from datetime import date

from models import Customer, Vehicle, QuoteRequest
from quote_engine import QuoteService, LiabilityCoverage, CollisionCoverage


@pytest.fixture
def basic_customer():
    return Customer(
        id="TEST-001",
        name="Test User",
        age=30,
        has_auto_policy=False,
        has_home_policy=False,
        years_as_customer=0,
        safe_driver=False,
    )


@pytest.fixture
def basic_vehicle():
    return Vehicle(make="Honda", model="Civic", year=2020)


@pytest.fixture
def quote_service():
    return QuoteService()


class TestLiabilityCoverage:
    def test_base_rate_for_standard_customer(self, basic_customer, basic_vehicle):
        coverage = LiabilityCoverage()
        result = coverage.calculate(basic_vehicle, basic_customer)
        assert result > 0

    def test_young_driver_surcharge(self, basic_vehicle):
        young_customer = Customer(
            id="YOUNG-001", name="Young Driver", age=22, safe_driver=False
        )
        coverage = LiabilityCoverage()
        result = coverage.calculate(basic_vehicle, young_customer)
        # Young drivers should pay more
        assert result > 500


class TestCollisionCoverage:
    def test_base_rate_for_standard_customer(self, basic_customer, basic_vehicle):
        coverage = CollisionCoverage()
        result = coverage.calculate(basic_vehicle, basic_customer)
        assert result > 0


class TestQuoteService:
    def test_valid_quote_generation(
        self, quote_service, basic_customer, basic_vehicle
    ):
        request = QuoteRequest(
            customer=basic_customer,
            vehicle=basic_vehicle,
            coverage_types=["liability"],
            effective_date=date.today(),
        )
        quote = quote_service.get_quote(request)
        assert quote is not None
        assert quote.customer_name == "Test User"
        assert quote.base_premium > 0

    def test_invalid_request_returns_none(self, quote_service, basic_vehicle):
        request = QuoteRequest(
            customer=Customer(id="", name="", age=0),
            vehicle=basic_vehicle,
            coverage_types=["liability"],
            effective_date=date.today(),
        )
        quote = quote_service.get_quote(request)
        assert quote is None

    def test_multiple_coverages(self, quote_service, basic_customer, basic_vehicle):
        request = QuoteRequest(
            customer=basic_customer,
            vehicle=basic_vehicle,
            coverage_types=["liability", "collision"],
            effective_date=date.today(),
        )
        quote = quote_service.get_quote(request)
        assert quote is not None
        assert len(quote.coverage_breakdown) == 2


class TestDiscounts:
    def test_safe_driver_discount_applied(self, quote_service, basic_vehicle):
        safe_customer = Customer(
            id="SAFE-001",
            name="Safe Driver",
            age=35,
            safe_driver=True,
            years_as_customer=2,
        )
        request = QuoteRequest(
            customer=safe_customer,
            vehicle=basic_vehicle,
            coverage_types=["liability"],
            effective_date=date.today(),
        )
        quote = quote_service.get_quote(request)
        assert "Safe Driver (-10%)" in quote.discounts_applied

    def test_loyalty_discount_applied(self, quote_service, basic_vehicle):
        loyal_customer = Customer(
            id="LOYAL-001",
            name="Loyal Customer",
            age=40,
            years_as_customer=5,
        )
        request = QuoteRequest(
            customer=loyal_customer,
            vehicle=basic_vehicle,
            coverage_types=["liability"],
            effective_date=date.today(),
        )
        quote = quote_service.get_quote(request)
        assert "Loyalty 5+ Years (-8%)" in quote.discounts_applied

    # NOTE: There seems to be an issue with discount calculations
    # for customers with both auto and home policies.
    # The total discount appears higher than expected.
