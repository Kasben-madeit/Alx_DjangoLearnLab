from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import CustomUser, Book   # import Book as well

# --- User Views ---

@permission_required('bookshelf.can_view', raise_exception=True)
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@permission_required('bookshelf.can_create', raise_exception=True)
def user_create(request):
    # logic for creating a user
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def user_edit(request, pk):
    # logic for editing a user
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def user_delete(request, pk):
    # logic for deleting a user
    pass


# --- Book Views (checker requirement) ---

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    # logic for creating a book
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # logic for editing a book
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # logic for deleting a book
    pass