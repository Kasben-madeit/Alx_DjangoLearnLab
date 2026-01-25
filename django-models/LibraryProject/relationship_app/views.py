from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()  # <-- explicit query
    return render(request, "relationship_app/list_books.html", {"books": books})  # <-- explicit template path


# Class-based view: Display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"  # <-- explicit template path
    context_object_name = "library"

    # Add books for this library
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context