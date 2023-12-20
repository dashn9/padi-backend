# myapp/management/commands/generate_fake_data.py

import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ratings.models import Rating
from faker import Faker


class Command(BaseCommand):
    help = "Generate faker ratings"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of instances to create (default: 10)",
        )
        parser.add_argument(
            "--target_id",
            type=int,
            help="ID of target",
        )
        parser.add_argument(
            "--target_type",
            type=str,
            help="Type of target",
        )

    def handle(self, *args, **options):
        count = options["count"]
        target_id = options["target_id"]
        target_type = options["target_type"]

        self.generate_ratings(count, target_id, target_type)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully generated {count} ratings of type {target_type} on {target_type}_id {target_id}"
            )
        )

    def __get_random_user(self):
        user = get_user_model()
        total_users = user.objects.count()

        if total_users > 0:
            random_index = random.randint(0, total_users - 1)

            # Retrieve the service at the random index
            random_user = user.objects.all()[random_index]

            return random_user
        else:
            # Handle the case where there are no services
            return None

    def generate_ratings(self, count, target_id, target_type):
        faker = Faker()
        for i in range(count):
            self.stdout.write(self.style.NOTICE(f"Generating Review {i+1} of {count}."))
            Rating.objects.create(
                rating_giver=self.__get_random_user(),
                rating_target_id=target_id,
                rating_target_type=target_type,
                rating_comment=faker.text(max_nb_chars=200),
                rating_stars_point=random.randint(1, 5),
            )
            self.stdout.write(
                self.style.SUCCESS(f"Generated Rating {i + 1} of {count}")
            )
