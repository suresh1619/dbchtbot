from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Supplier
from .serializers import ProductSerializer, SupplierSerializer
from .gpt import get_orm_statement
from django.shortcuts import render


class QueryAPIView(APIView):
    """
    API View to handle user queries and return ORM results.
    """
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query")  # Get the query from the request
        results = None
        orm_query = None
        column_titles = []

        if query:
            try:
                # Generate ORM query string using GPT
                orm_query = get_orm_statement(query)
                table_name = orm_query.split('.')[0]  # Extract the table name (e.g., "Product")

                # Map table name to the corresponding model
                model = None
                serializer_class = None
                if table_name == "Product":
                    model = Product
                    serializer_class = ProductSerializer
                elif table_name == "Supplier":
                    model = Supplier
                    serializer_class = SupplierSerializer

                if not model or not serializer_class:
                    return Response(
                        {"error": f"Invalid table name: {table_name}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Safely execute the ORM query
                context = {'Product': Product, 'Supplier': Supplier}
                exec(f"results = list({orm_query})", {}, context)
                results = context.get('results')

                # Serialize the results
                if results:
                    serialized_data = serializer_class(results, many=True).data
                    return Response(
                        {
                            "query": query,
                            "orm_query": orm_query,
                            "results": serialized_data,
                        },
                        status=status.HTTP_200_OK
                    )

                return Response(
                    {"query": query, "orm_query": orm_query, "results": []},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"error": f"Error executing query: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"error": "No query provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )
# Django view to process and execute the ORM query
from django.shortcuts import render
from .models import Product, Supplier
from .gpt import get_orm_statement

def query_view(request):
    """
    Handle user queries and display the results.
    """
    query = request.GET.get("query")  # Get the query from the request
    results = None
    orm_query = None
    column_titles=None

    if query:
        orm_query = get_orm_statement(query)  # Get ORM query from GPT model
        print(orm_query)
        table_name = orm_query.split('.')[0]  # Get the table/model name (before the dot)

            # Dynamically map the table name to the correct model
        model = None
        if table_name == "Product":
            model = Product
        elif table_name == "Supplier":
            model = Supplier
        if model:
            column_titles = [field.name for field in model._meta.fields]
        

        try:
            # Safely evaluate the ORM query using Python's exec with a controlled environment
            context = {'Product': Product, 'Supplier': Supplier}
            exec(f"results = list({orm_query})", {}, context)
            results = context.get('results')
        except Exception as e:
            # Handle errors for invalid queries
            results = f"Error executing query: {e}"

    return render(request, "home.html", {"query": query,'column_titles':column_titles, "results": results, "orm_query": orm_query})