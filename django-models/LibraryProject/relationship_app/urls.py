from django.urls import path
from .views import list_books, LibraryDetailView, UserLoginView, UserLogoutView, register, admin_view

urlpatterns = [
    # Existing views
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Authentication views
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("admin-view/", admin_view, name="admin_view"),  # <-- new Admin-only view

]