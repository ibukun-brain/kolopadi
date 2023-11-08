import random
from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker

from loans.models import Borrower, LoanListing

User = get_user_model()
fake = Faker()


def reasons_for_loan():
    reasons = [
        "Debt Consolidation",
        "Home Improvemnets",
        "Medical Expenses",
        "Wedding Expenses",
        "Travel",
        "Education",
        "Vehicle Financing",
        "Moving Expenses",
        "Emergency Expenses",
        "Business Startup Costs",
    ]
    return random.choice(reasons)


def generate_decimal_number():
    rand_decimal = [5000.00, 10000.00, 20000.00, 50000.00, 100000.00, 200000.00]
    return random.choice(rand_decimal)


def generate_random_interest_rate():
    interest_rate = [500.00, 1000.00, 2000.00, 5000.00, 10000.00, 20000.00]
    return random.choice(interest_rate)


def create_borrower_profile(number):
    # for i in range(number):
    user = random.choice(User.objects.order_by("-created_at"))
    # borrower = Borrower()
    # try:
    borrower, _ = Borrower.objects.get_or_create(
        user=user,
    )
    borrower.username = fake.profile()["username"]
    borrower.bio = fake.paragraph(nb_sentences=5)
    borrower.address = fake.address()
    borrower.employment_type = fake.job()
    borrower.verified = fake.date_between(
        datetime.strptime("2023-11-1", "%Y-%m-%d"),
        datetime.strptime("2023-11-8", "%Y-%m-%d"),
    )
    borrower.profession_type = fake.profile()["job"]
    borrower.save()
    return borrower


class Command(BaseCommand):
    help = "Creates dummy data for LoanListing model"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=10,
            type=int,
            help="How many for LoanListing(s) do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            LoanListing,
            number,
            {
                "uid": lambda x: seeder.faker.uuid4(cast_to=None),
                "loan_amount": lambda x: Decimal(generate_decimal_number()),
                "interest_rate": lambda x: Decimal(generate_random_interest_rate()),
                "borrower": lambda x: create_borrower_profile(number),
                "loan_tenure_in_months": lambda x: random.randint(1, 12),
                "reason_for_loan": lambda x: seeder.faker.paragraph(nb_sentences=3),
                "title": lambda x: reasons_for_loan(),
                "ability_to_repay": lambda x: seeder.faker.paragraph(nb_sentences=3),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} LoanListing(s) was created"))
