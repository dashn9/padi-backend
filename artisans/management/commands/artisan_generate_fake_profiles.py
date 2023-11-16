# myapp/management/commands/generate_fake_data.py

import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from artisans.models import Artisan, Service
from faker import Faker


class Command(BaseCommand):
    help = "Generate faker artisan profiles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of instances to create (default: 10)",
        )
        parser.add_argument(
            "--password",
            action="store_true",
            default="password",
            help="Password field when generating artisan profiles(Default: password)",
        )

    def handle(self, *args, **options):
        count = options["count"]
        password = options["password"]

        self.generate_artisan_profiles(count, password)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated {count} instances of the Artisans model."
            )
        )

    def __get_random_service(self):
        # Get the total number of services
        total_services = Service.objects.count()

        # Check if there are any services
        if total_services > 0:
            # Generate a random index within the range of total services
            random_index = random.randint(0, total_services - 1)

            # Retrieve the service at the random index
            random_service = Service.objects.all()[random_index]

            return random_service
        else:
            # Handle the case where there are no services
            return None

    def generate_artisan_profiles(self, count, password):
        faker = Faker()
        User = get_user_model()
        for i in range(count):
            self.stdout.write(
                self.style.NOTICE(f"Generating Artisan {i+1} of {count}.")
            )
            user = User.objects.create_user(
                password=password or "password",
                email=faker.email(),
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                ip_addresses=[faker.ipv4()],
            )
            artisan = Artisan(
                user=user,
                bio=faker.text(max_nb_chars=200),
                birth_date=faker.date_of_birth(minimum_age=18, maximum_age=65),
                state=random.choice(Artisan.STATE_CHOICES)[0],
            )
            artisan.save()
            artisan.services.add(self.__get_random_service())
            self.stdout.write(
                self.style.SUCCESS(f"Generated Artisan {i + 1} of {count}")
            )
