from django.urls import path
from .views import QueryAPIView,query_view

urlpatterns = [
    path('query/', QueryAPIView.as_view(), name='query-api'),
    path('',query_view,name='query_view')
]
