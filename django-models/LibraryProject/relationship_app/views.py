from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library   # <-- explicit import required by checks

# Function-based view: List all books
def list_books(request):
    # Explicit query required by checks
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view: Display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Explicitly include all books in this library
        context["books"] = self.object.books.all()
        return context