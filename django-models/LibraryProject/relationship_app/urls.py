from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    UserLoginView,
    register,
    admin_view,
    librarian_view,
    member_view,
    add_book,
    edit_book,
    delete_book,
)
from django.contrib.auth.views import LogoutView   # <-- add this import

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Authentication views (checker requirement)
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),   # <-- built-in LogoutView
    path("register/", register, name="register"),           # <-- views.register

    path("admin-view/", admin_view, name="admin_view"),
    path("librarian-view/", librarian_view, name="librarian_view"),
    path("member-view/", member_view, name="member_view"),

    # Secured book management views
    path("add_book/", add_book, name="add_book"),
    path("edit_book/<int:pk>/", edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", delete_book, name="delete_book"),
]