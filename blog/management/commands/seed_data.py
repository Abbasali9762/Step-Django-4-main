from django.core.management.base import BaseCommand

from blog.models import Category, Post


class Command(BaseCommand):
    help = "Category və Post üçün nümunə data yaradır (əl ilə admin-də doldurmadan)."

    def handle(self, *args, **options):
        categories = [
            {"name": "Proqramlaşdırma", "slug": "proqramlasdirma", "description": "Kod, dillər və alətlər"},
            {"name": "Oyunlar", "slug": "oyunlar", "description": "Oyunlar, taktikalar və maraqlı faktlar"},
            {"name": "Kitablar", "slug": "kitablar", "description": "Oxuduqlarımız və tövsiyələr"},
        ]

        for cat in categories:
            obj, created = Category.objects.get_or_create(slug=cat["slug"], defaults=cat)
            self.stdout.write(self.style.SUCCESS(f"Category: {obj.name} ({'yeni' if created else 'mövcud'})"))

        posts = [
            {
                "title": "Python-da ilk addım",
                "author": "nigar",
                "content": "Python öyrənməyə haradan başlamaq lazımdır? Əvvəlcə dəyişənlər, sonra şərtlər və döngülər.",
                "is_published": True,
                "is_featured": False,
            },
            {
                "title": "Git nədir və niyə lazımdır?",
                "author": "nigar",
                "content": "Git kodun tarixçəsini saxlayır. Səhv etsən, köhnə versiyaya qayıda bilərsən.",
                "is_published": True,
                "is_featured": True,
            },
            {
                "title": "FIFA-da ən yaxşı taktika",
                "author": "murad",
                "content": "4-3-3 sxemi hücum üçün, 5-3-2 isə müdafiə üçün yaxşıdır.",
                "is_published": True,
                "is_featured": False,
            },
            {
                "title": "Harri Potter kitablarını hansı ardıcıllıqla oxumalı?",
                "author": "aysel",
                "content": "Yeddi kitabın hamısını çıxış ilinə görə oxumaq ən yaxşısıdır.",
                "is_published": True,
                "is_featured": False,
            },
        ]

        for post in posts:
            obj, created = Post.objects.get_or_create(title=post["title"], defaults=post)
            self.stdout.write(self.style.SUCCESS(f"Post: {obj.title} ({'yeni' if created else 'mövcud'})"))

        self.stdout.write(self.style.SUCCESS("Data yaratma bitdi."))
