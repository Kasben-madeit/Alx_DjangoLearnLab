from django.shortcuts import render
from django.views.generic.detail import DetailView   # <-- explicit import required
from .models import Book
from .models import Library   # <-- explicit line required
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import UserProfile


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
    

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Login view (built-in)
class UserLoginView(LoginView):
    template_name = "relationship_app/login.html"


# Logout view (built-in)
class UserLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


# Registration view (custom)
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in immediately after registration
            return redirect("list_books")  # redirect to a page in your app
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def admin_view(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role == "Admin":   # <-- exact string required
            return render(request, "relationship_app/admin_view.html")
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden("No profile found for this user.")
    

# Helper functions for role checks
def is_librarian(user):
    try:
        return user.userprofile.role == "Librarian"
    except UserProfile.DoesNotExist:
        return False

def is_member(user):
    try:
        return user.userprofile.role == "Member"
    except UserProfile.DoesNotExist:
        return False


# Librarian-only view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


# Member-only view
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")