import google.generativeai as genai
import re

# Configure the Gemini API
GEMINI_API = ''
genai.configure(api_key=GEMINI_API)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get ORM statement based on user query
def get_orm_statement(query):
    # Provide the model with the database structure and table names
    schema_info = """
    The following are the table names and their structures:

    Table Name: Supplier
    Fields:
        - name: CharField (max_length=255)
        - contact_info: TextField
        - product_categories_offered: TextField
    Relationships:
        - products: ForeignKey to Product (one-to-many)

    Table Name: Product
    Fields:
        - name: CharField (max_length=255)
        - brand: CharField (max_length=255)
        - price: DecimalField (max_digits=10, decimal_places=2)
        - category: CharField (max_length=255)
        - description: TextField
        - supplier: ForeignKey to Supplier (many-to-one)
    """

    # Construct the prompt by including the schema information and the query
    prompt = f"""
    The database schema is as follows: {schema_info} and understand the query better way.
    Write a single-line ORM query using Django's filter and all methods to {query}.
    Provide only the ORM statement, no explanation.
    Please use __iexact for case-insensitive filtering.please,please
    Example Queries:
    - "Show me all products under brand X." -> Product.objects.filter(brand__iexact='X')
    - "Which suppliers provide laptops?" -> Supplier.objects.filter(product_categories_offered__icontains='Laptops')
    - "Give me details of product ABC." -> Product.objects.get(name__='ABC')

    """

    # Generate the ORM statement based on the prompt
    response = model.generate_content(prompt)
    orm_statement = response.text.strip()

    # Remove unwanted prefixes like "``` python"
    if orm_statement.startswith("``` python"):
        orm_statement = orm_statement = re.sub(r"^```python\s*", "", orm_statement)
    return orm_statement
