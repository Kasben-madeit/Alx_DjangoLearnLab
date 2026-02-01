# api/urls.py
from .views import BookList
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet



router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
        path('books/', BookList.as_view(), name='book-list'),

    # Keep the simple ListAPIView route
    path('books/', BookList.as_view(), name='book-list'),

    # Include router-generated routes
    path('', include(router.urls)),
]
