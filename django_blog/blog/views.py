"""
Views for the blog application.

These views implement user registration and profile management along with CRUD
operations for blog posts and comments. The views leverage Django's generic
class‑based views where appropriate and function based views for bespoke logic.
"""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    PostForm,
    CommentForm,
)
from .models import Post, Comment, Tag


class PostListView(ListView):
    """
    Display a list of all blog posts. This view is the landing page for the
    blog and shows the latest posts first.
    """

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10


class PostDetailView(DetailView):
    """
    Display a single blog post along with its comments and a comment form for
    authenticated users.
    """

    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all()
        context["comment_form"] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create new blog posts. Tags entered in the
    comma‑separated tags field are parsed and associated with the post.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # Handle tags after the post has been created
        tags_str = form.cleaned_data.get("tags", "")
        if tags_str:
            tags_list = [t.strip() for t in tags_str.split(",") if t.strip()]
            for tag_name in tags_list:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                form.instance.tags.add(tag_obj)
        return response

    def get_success_url(self) -> str:
        return reverse("post-detail", kwargs={"pk": self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow the author of a post to edit its title, content and tags. Only the
    original author may update their post.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        # Update tags
        self.object.tags.clear()
        tags_str = form.cleaned_data.get("tags", "")
        if tags_str:
            tags_list = [t.strip() for t in tags_str.split(",") if t.strip()]
            for tag_name in tags_list:
                tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                self.object.tags.add(tag_obj)
        return response

    def test_func(self) -> bool:
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self) -> str:
        return reverse("post-detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow the author of a post to delete it. Confirmation is handled by a
    dedicated template.
    """

    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog-home")

    def test_func(self) -> bool:
        post = self.get_object()
        return self.request.user == post.author


def register(request):
    """
    Handle user registration. On successful registration the user is logged in
    and redirected to the home page.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully!")
            return redirect("blog-home")
    else:
        form = UserRegisterForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    """
    Allow authenticated users to view and update their profile, including
    username, email, bio and profile picture.
    """
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "blog/profile.html", context)


@login_required
def add_comment(request, pk: int):
    """
    Allow authenticated users to add a comment to a post. After successful
    submission the user is redirected back to the post detail page.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Your comment has been added!")
            return redirect("post-detail", pk=pk)
    return redirect("post-detail", pk=pk)


# Remove legacy function‑based comment edit and delete views. Comment CRUD
# functionality is now handled via class‑based views below.


class PostByTagListView(ListView):
    """List posts filtered by tag slug/name. Used for /tags/<slug:tag_slug>/ URLs."""

    model = Post
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag_slug", "")
        # We treat slug as the tag name (case-insensitive) for simplicity.
        return Post.objects.filter(tags__name__iexact=tag_slug).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_name"] = self.kwargs.get("tag_slug")
        return context


class TagListView(ListView):
    """
    Display all posts associated with a given tag. The tag name is passed in
    the URL as <str:tag_name>.
    """

    model = Post
    template_name = "blog/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get("tag_name")
        return Post.objects.filter(tags__name__iexact=tag_name).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_name"] = self.kwargs.get("tag_name")
        return context


# Comment CRUD class‑based views
class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new comment for a given post.  The post ID is provided via the
    URL keyword argument ``post_id``.  On successful creation the user is
    redirected back to the post detail page.
    """

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id") or self.kwargs.get("pk"))
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add the parent post ID to the context so the template can provide
        a cancel link back to the post detail page when creating a new
        comment.
        """
        context = super().get_context_data(**kwargs)
        context.setdefault("post_id", self.kwargs.get("post_id") or self.kwargs.get("pk"))
        return context

    def get_success_url(self) -> str:
        return reverse("post-detail", kwargs={"pk": self.kwargs.get("post_id") or self.kwargs.get("pk")})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing comment. Only the comment's author may update it.

    Supports both URL styles:
    - /posts/<post_id>/comments/<comment_id>/update/
    - /comment/<pk>/update/
    """

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_object(self, queryset=None):  # type: ignore[override]
        comment_pk = self.kwargs.get("comment_id") or self.kwargs.get("pk")
        if self.kwargs.get("post_id"):
            return get_object_or_404(Comment, id=comment_pk, post__pk=self.kwargs["post_id"])
        return get_object_or_404(Comment, id=comment_pk)

    def test_func(self) -> bool:
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self) -> str:
        comment = self.get_object()
        return reverse("post-detail", kwargs={"pk": comment.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = getattr(self, "object", None) or self.get_object()
        context.setdefault("post_id", comment.post.pk)
        return context



class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a comment.  Only the comment's author may delete it.  A confirmation
    page is displayed before deletion.  On success the user is redirected back
    to the post detail page.
    """

    model = Comment
    template_name = "blog/comment_confirm_delete.html"
    pk_url_kwarg = "comment_id"

    def get_object(self, queryset=None):  # type: ignore[override]
        return get_object_or_404(
            Comment,
            id=self.kwargs["comment_id"],
            post__pk=self.kwargs.get("post_id") or self.kwargs.get("pk"),
        )

    def test_func(self) -> bool:
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self) -> str:
        return reverse("post-detail", kwargs={"pk": self.kwargs.get("post_id") or self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the parent post ID to the template for the cancel link
        context["post_id"] = self.kwargs.get("post_id")
        return context


def search(request):
    """
    Basic search function that filters posts by title, content and tags. The
    search term is passed as a GET parameter `q`.
    """
    query = request.GET.get("q", "")
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()
    return render(
        request,
        "blog/search_results.html",
        {"query": query, "results": results},
    )