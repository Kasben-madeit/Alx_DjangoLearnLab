from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import CustomUser



# Create your views here.



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