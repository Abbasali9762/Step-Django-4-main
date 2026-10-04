from django.contrib import admin

from .models import (
    Post, 
    Category, 
    Comment,
    Tag
)

class CommentInline(admin.TabularInline):  # TabularInline — cədvəl, StackedInline — blok
    model = Comment
    extra = 1  # əlavə boş formaların sayı
    

# [DƏRS 9] müəllim yazır
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "is_published", "is_featured", "views"]
    # ↑ [EV 9] is_featured əlavə olundu — list_editable-dakı sahə list_display-də də olmalıdır
    list_filter = ["is_published", "is_featured", "category"]     # sağda filtr paneli ([EV 9] is_featured)
    search_fields = ["title", "content"]                          # yuxarıda axtarış qutusu

    # [EV 9] tapşırıq 6 — checkbox-u cədvəldən birbaşa dəyişmək
    list_editable = ["is_published", "is_featured"]

    # [EV 9] bonus — "Seçilmiş et" action-u
    actions = ["make_featured"]
    inlines = [CommentInline]  # Post-un altında Comment-ləri də göstərmək üçün
    # filter_horizontal = ["tags"]  # tags sahəsi üçün horizontal filter (çoxlu seçim üçün)

    @admin.action(description="Seçilmiş et")
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)                        # seçilən hamısını bir sorğu ilə


# [PRAKTİKA 9] tələbə yazır
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}  
    
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}                      # ad yazdıqca slug özü dolur
    

# admin.site.register(Comment)  # Comment üçün ayrıca admin paneli yaratmaq istəmədik, ona görə register() ilə qeyd etdik
# admin.site.register(Tag)      # Tag üçün ayrıca admin paneli yaratmaq istəmədik, ona görə register() ilə qeyd etdik