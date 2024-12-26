from django.core.management.base import BaseCommand
from ...models import Role

class Command(BaseCommand):
    help = "Seed initial roles into the database"

    def handle(self, *args, **kwargs):
        roles = [
            {"name": "Admin", "description": "Has full access to the system"},
            {"name": "User", "description": "Regular user with limited access"},
            {"name": "Driver", "description": "Responsible for deliveries"},
            {"name": "Seller", "description": "Can manage their own products"},
        ]

        for role_data in roles:
            role, created = Role.objects.get_or_create(
                name=role_data["name"],
                defaults={"description": role_data["description"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Role '{role.name}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"Role '{role.name}' already exists."))
