from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required
from .forms import *


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", post_id=post.id)
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})


# Views for Categories model


def categories_list(request):
    categories = Categories.objects.all()
    return render(request, "categories_list.html", {"categories": categories})


def category_detail(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    return render(request, "category_detail.html", {"category": category})


def category_posts(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    posts = Post.objects.filter(category=category)
    return render(
        request, "category_posts.html", {"category": category, "posts": posts}
    )


# Views for Post model


def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "post_list.html", {"posts": posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, "post_detail.html", {"post": post})


def posts_by_author(request, author_id):
    author = get_object_or_404(User, id=author_id)
    posts = Post.objects.filter(author=author)
    return render(request, "posts_by_author.html", {"author": author, "posts": posts})


def posts_by_sport(request, sport_id):
    sport = get_object_or_404(Sport, id=sport_id)
    posts = Post.objects.filter(sport=sport)
    return render(request, "posts_by_sport.html", {"sport": sport, "posts": posts})


def posts_by_championship(request, championship_id):
    championship = get_object_or_404(Championship, id=championship_id)
    posts = Post.objects.filter(championship=championship)
    return render(
        request,
        "posts_by_championship.html",
        {"championship": championship, "posts": posts},
    )
