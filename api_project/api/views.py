# api/views.py
from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser





# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()       # all books from the database
    serializer_class = BookSerializer   # use the serializer to format output

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can access


# BookViewSet uses TokenAuthentication
# Only authenticated users can access endpoints
# Tokens are retrieved via /api/token/ using username/password