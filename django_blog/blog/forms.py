"""
Forms used throughout the blog application.

These include registration and profile update forms for users as well as forms
for creating and editing posts and comments.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment, Profile, Tag

class TagWidget(forms.TextInput):
    """Widget for comma-separated tag input."""

    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs.setdefault("placeholder", "e.g. django,python,web")
        super().__init__(attrs=attrs, *args, **kwargs)



class UserRegisterForm(UserCreationForm):
    """
    Extend Django's built‑in UserCreationForm to include an email field. This
    form is used during user registration.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    """
    Allow users to update their username and email address from their profile.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating the user's Profile. Allows editing of the bio and
    uploading a new profile picture.
    """

    class Meta:
        model = Profile
        fields = ["bio", "image"]


class PostForm(forms.ModelForm):
    """
    Form used for creating and editing blog posts. Includes a tags field for
    entering comma‑separated tag names which will be parsed and created in
    the view.
    """

    tags = forms.CharField(
        required=False,
        help_text="Comma‑separated list of tags.",
        widget=TagWidget(),
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]


    widgets = {
        \"title\": forms.TextInput(attrs={\"class\": \"form-control\"}),
        \"content\": forms.Textarea(attrs={\"rows\": 8, \"class\": \"form-control\"}),
        \"tags\": TagWidget(),
    }
class CommentForm(forms.ModelForm):
    """
    Basic form used for creating and updating comments on a post.
    """

    class Meta:
        model = Comment
        fields = ["content"]

    def clean_content(self):
        """Ensure that the comment content is not empty or whitespace only."""
        content = self.cleaned_data.get("content", "")
        if not content.strip():
            raise forms.ValidationError("Comment cannot be empty.")
        return content