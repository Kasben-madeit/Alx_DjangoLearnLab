from django.shortcuts import render
from django.views.generic.detail import DetailView   # <-- explicit import required
from .models import Book
from .models import Library   # <-- explicit line required

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()  # <-- explicit query required
    return render(request, "relationship_app/list_books.html", {"books": books})

# Class-based view: Display details of a specific library
class LibraryDetailView(DetailView):   # <-- must use DetailView
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context