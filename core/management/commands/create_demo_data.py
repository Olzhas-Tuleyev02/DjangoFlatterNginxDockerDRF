import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from services.models import Service, Category
from users.models import User
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Generates demo data for the marketplace'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to generate demo data...'))

        fake = Faker('ru_RU')
        User = get_user_model()

        # === Clean up old data ===
        User.objects.exclude(is_superuser=True).delete()
        Category.objects.all().delete()
        Service.objects.all().delete()
        self.stdout.write(self.style.WARNING('Old data cleaned up.'))

        # === Create Operator ===
        operator, _ = User.objects.get_or_create(
            username='operator',
            defaults={
                'email': 'operator@example.com',
                'role': User.Role.OPERATOR,
                'is_staff': True
            }
        )
        operator.set_password('operatorpass')
        operator.save()
        self.stdout.write(self.style.SUCCESS('Operator user created (operator/operatorpass).'))

        # === Create Providers ===
        providers = []
        provider_data = [
            {'username': 'photo_pro', 'email': 'photo@example.com'},
            {'username': 'decor_master', 'email': 'decor@example.com'},
        ]
        for data in provider_data:
            provider, _ = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'role': User.Role.PROVIDER
                }
            )
            provider.set_password('providerpass')
            provider.save()
            providers.append(provider)
        self.stdout.write(self.style.SUCCESS(f'{len(providers)} provider users created (password: providerpass).'))

        # === Create Customers ===
        customers = []
        for i in range(2):
            customer, _ = User.objects.get_or_create(
                username=f'customer{i+1}',
                defaults={
                    'email': f'customer{i+1}@example.com',
                    'role': User.Role.CUSTOMER
                }
            )
            customer.set_password('customerpass')
            customer.save()
            customers.append(customer)
        self.stdout.write(self.style.SUCCESS(f'{len(customers)} customer users created (password: customerpass).'))

        # === Create Categories ===
        categories_data = ['Фотография', 'Декор', 'Аренда', 'Музыка', 'Ведущие']
        categories = []
        for cat_name in categories_data:
            slug = slugify(cat_name)
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': cat_name}
            )
            categories.append(category)
        self.stdout.write(self.style.SUCCESS(f'{len(categories)} categories created.'))

        # === Create Services ===
        services = []
        service_data = [
            {'name': 'Свадебная фотосессия', 'provider': providers[0], 'category': categories[0], 'city': 'Алматы'},
            {'name': 'Love Story фотосессия', 'provider': providers[0], 'category': categories[0], 'city': 'Нур-Султан'},
            {'name': 'Оформление зала шарами', 'provider': providers[1], 'category': categories[1], 'city': 'Алматы'},
            {'name': 'Аренда фотобудки', 'provider': providers[1], 'category': categories[2], 'city': 'Шымкент'},
            {'name': 'DJ на мероприятие', 'provider': providers[0], 'category': categories[3], 'city': 'Алматы'},
        ]

        for data in service_data:
            slug = slugify(data['name'])
            service, created = Service.objects.get_or_create(
                slug=slug,
                defaults={
                    'provider': data['provider'],
                    'name': data['name'],
                    'description': fake.text(max_nb_chars=400),
                    'price': random.randint(500, 2000) * 100,
                    'category': data['category'],
                    'city': data['city'],
                    'available_dates': "2025-12-01,2025-12-05,2025-12-10",
                    'is_active': True
                }
            )
            if created:
                services.append(service)
        self.stdout.write(self.style.SUCCESS(f'{len(services)} services created.'))

        self.stdout.write(self.style.SUCCESS('Demo data generation complete!'))