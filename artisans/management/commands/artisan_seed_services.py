from django.core.management.base import BaseCommand
from django.db import transaction
from artisans.models import Service


class Command(BaseCommand):
    help = "Seed data into the Artisan Service model"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear", action="store_true", help="Clear existing data before seeding"
        )
        parser.add_argument(
            "--refresh", action="store_true", help="Refresh table with seed"
        )

    def handle(self, *args, **kwargs):
        clear_data = kwargs["clear"]
        refresh_data = kwargs["refresh"]

        if clear_data and refresh_data:
            self.stderr.write(
                self.style.ERROR("Specify either '--clear' or '--refresh', not both.")
            )
            return

        if clear_data:
            self.clear_data()
        elif refresh_data:
            self.stdout.write(self.style.SUCCESS("Refreshing data..."))
            self.clear_data()
            self.seed_table()
        else:
            self.seed_table()

        self.stdout.write(self.style.SUCCESS("Data seeded successfully"))

    @transaction.atomic
    def clear_data(self):
        self.stdout.write(self.style.SUCCESS("Clearing existing data..."))
        Service.objects.all().delete()

    @transaction.atomic
    def seed_table(self):
        self.stdout.write(self.style.SUCCESS("Seeding data..."))
        service_data = [
            {
                "icon_name": "air-conditioner",
                "icon_color": "#DDA503",
                "icon_back_drop_color": "#FFF9E8",
                "service_code": "ac_repair",
                "service_name": "AC Repair",
                "service_individual_name": "AC Repairer",
                "service_group_name": "AC Repairers",
            },
            {
                "icon_name": "lightning-bolt",
                "icon_color": "#4A7AFF",
                "icon_back_drop_color": "#F6F9FF",
                "service_code": "electricity",
                "service_name": "Electricity",
                "service_individual_name": "Electerician",
                "service_group_name": "Electericians",
            },
            {
                "icon_name": "pipe-leak",
                "icon_color": "#5EBE30",
                "icon_back_drop_color": "#F5FFE9",
                "service_code": "plumbing",
                "service_name": "Plumbing",
                "service_individual_name": "Plumber",
                "service_group_name": "Plumbers",
            },
            {
                "icon_name": "hair-dryer",
                "icon_color": "#CA84FF",
                "icon_back_drop_color": "#FBF6FF",
                "service_code": "beauty",
                "service_name": "Beauty",
                "service_individual_name": "Beautician",
                "service_group_name": "Beauticians",
            },
        ]

        for data in service_data:
            Service.objects.create(**data)
