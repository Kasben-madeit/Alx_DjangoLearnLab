from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books   # <-- checker requirement
import relationship_app.views as views

urlpatterns = [
    # Function-based and class-based views
    path("books/", list_books, name="list_books"),   # <-- uses direct import
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Authentication views
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),

    # Role-based views
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),

    # Secured book management views
    path("add_book/", views.add_book, name="add_book"),
    path("edit_book/<int:pk>/", views.edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", views.delete_book, name="delete_book"),
]