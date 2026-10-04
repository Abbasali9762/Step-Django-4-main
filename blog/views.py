from django.shortcuts import render, get_object_or_404

from .models import Post, Category, Tag

# ─────────────────────────── [DƏRS 9] ───────────────────────────

def post_list(request):
    posts = Post.objects.filter(is_published=True)        # SELECT ... WHERE is_published
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=True)   # tapmasa → 404

    # [EV 9] tapşırıq 1 — hər açılışda baxış sayı artır
    post.views += 1
    post.save()

    return render(request, "blog/post_detail.html", {"post": post})


def about(request):
    return render(request, "blog/about.html")


# ───────────────────────── [PRAKTİKA 9] ─────────────────────────

def category_list(request):
    categories = Category.objects.all()
    return render(request, "blog/category_list.html", {"categories": categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # posts = Post.objects.filter(category=slug, is_published=True)   # Dərs 10-da bu sətir sadələşəcək
    posts = category.posts.filter(is_published=True)  # SELECT ... WHERE category_id=... AND is_published
    context = {"category": category, "posts": posts}
    return render(request, "blog/category_detail.html", context)


# ─────────────────────────── [EV 9] ───────────────────────────

def contact(request):
    return render(request, "blog/contact.html")


def author_posts(request, name):                                  # tapşırıq 2
    posts = Post.objects.filter(author=name, is_published=True)
    context = {"name": name, "posts": posts}
    return render(request, "blog/author_posts.html", context)


def latest(request):                                              # tapşırıq 3
    posts = Post.objects.filter(is_published=True).order_by("-created_at")[:3]
    return render(request, "blog/latest.html", {"posts": posts})


def stats(request):                                               # tapşırıq 4
    published = Post.objects.filter(is_published=True)
    context = {
        "post_count": published.count(),                          # SELECT COUNT(*) — siyahını yükləmir
        "category_count": Category.objects.count(),
        "top_post": published.order_by("-views").first(),         # ən çox baxılan; yoxdursa None
    }
    return render(request, "blog/stats.html", context)


def tag_detail(request, slug):                                           # tapşırıq 5
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.posts.filter(is_published=True)
    context = {"tag": tag, "posts": posts}
    return render(request, "blog/tag_detail.html", context)