from django import forms
from .models import Book, CustomUser

# Example form required by checker
class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


# Optional: Model forms for safe CRUD operations
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn"]

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "date_of_birth", "profile_photo"]