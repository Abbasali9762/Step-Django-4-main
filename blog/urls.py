from django.urls import path

from . import views

app_name = "blog"       # ad sahəsi: reverse("blog:post_detail") — başqa app-ın adları ilə qarışmır

urlpatterns = [
    # [DƏRS 7]
    path("", views.post_list, name="post_list"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("about/", views.about, name="about"),

    path("contact/", views.contact, name="contact"),
    path("categories/", views.category_list, name="category_list"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("author/<str:name>/", views.author_posts, name="author_posts"),     
    path("stats/", views.stats, name="stats"),                              
    path("tag/<slug:slug>/", views.tag_detail, name="tag_detail"),  # tapşırıq 5
    path("latest/", views.latest, name="latest"),
]
