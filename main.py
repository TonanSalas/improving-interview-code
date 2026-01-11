from datetime import date

from models import Customer, Vehicle, QuoteRequest
from quote_engine import QuoteService


def main():
    # Create a sample customer with both auto and home policies
    customer = Customer(
        id="CUST-001",
        name="Jane Smith",
        age=35,
        has_auto_policy=True,
        has_home_policy=True,
        years_as_customer=6,
        safe_driver=True,
    )

    vehicle = Vehicle(
        make="Toyota",
        model="Camry",
        year=2022,
    )

    request = QuoteRequest(
        customer=customer,
        vehicle=vehicle,
        coverage_types=["liability", "collision"],
        effective_date=date.today(),
    )

    service = QuoteService()
    quote = service.get_quote(request)

    if quote:
        print("=" * 50)
        print("INSURANCE QUOTE")
        print("=" * 50)
        print(f"Customer: {quote.customer_name}")
        print(f"Quote ID: {quote.request_id}")
        print()
        print("Coverage Breakdown:")
        for coverage, amount in quote.coverage_breakdown.items():
            print(f"  {coverage}: ${amount:.2f}")
        print()
        print(f"Base Premium: ${quote.base_premium:.2f}")
        print()
        print("Discounts Applied:")
        for discount in quote.discounts_applied:
            print(f"  {discount}")
        print(f"Total Discounts: -${quote.discount_amount:.2f}")
        print()
        print(f"Final Premium: ${quote.final_premium:.2f}")
        print("=" * 50)
    else:
        print("Failed to generate quote.")


if __name__ == "__main__":
    main()
