import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbchatbot.settings')  # Ensure this is correct
django.setup()

from faker import Faker
from logic.models import Supplier, Product

# Setup Django environment

# Initialize Faker
fake = Faker()

# Function to populate the database
def populate_data(n):
    for _ in range(n):  # Create n fake suppliers
        # Create a supplier
        supplier = Supplier.objects.create(
            name=fake.company(),
            contact_info=fake.phone_number(),
            product_categories_offered=fake.word() + ', ' + fake.word()
        )
        print(f"Supplier {supplier.name} created.")
        
        # Create fake products for each supplier
        for _ in range(n // 2):  # Create n/2 products for each supplier
            Product.objects.create(
                name=fake.word(),
                brand=fake.company(),
                price=fake.random_number(digits=2),
                category=fake.word(),
                description=fake.sentence(),
                supplier=supplier
            )
            print(f"Product {fake.word()} created for {supplier.name}.")

# Call the populate function with the number of suppliers to create
if __name__ == "__main__":
    populate_data(20)  # Populate 20 suppliers and their products
    print("Data population complete.")
