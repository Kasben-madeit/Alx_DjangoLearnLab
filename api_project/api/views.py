from django.shortcuts import render
# api/views.py
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets





# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()       # all books from the database
    serializer_class = BookSerializer   # use the serializer to format output


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
