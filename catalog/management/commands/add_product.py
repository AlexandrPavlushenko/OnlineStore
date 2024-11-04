from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Add test product to the database'

    def handle(self, *args, **options):

        # Category.objects.all().delete()
        # Product.objects.all().delete()

        # call_command('loaddata', 'category_fixture.json')
        # call_command('loaddata', 'product_fixture.json')

        category, _ = Category.objects.get_or_create(name='Test Category')
        products = [{'name': 'Product1', 'description': 'description_product1', 'price': 100, 'category': category},
                    {'name': 'Product2', 'description': 'description_product2', 'price': 200, 'category': category},]
        for product in products:
            product, created = Product.objects.get_or_create(**product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Product created: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exist: {product.name}'))