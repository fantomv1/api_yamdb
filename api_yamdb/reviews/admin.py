from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import Category, Comment, Genre, Review, Title, User


UserAdmin.fieldsets += (("Extra Fields", {"fields": ("bio", "role")}),)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    list_editable = ("role",)
    search_fields = ("username",)
    list_filter = ("role",)
    list_display_links = ("username",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "category",
        "get_genres",
    )
    list_editable = ("category",)
    search_fields = ("name",)
    list_filter = ("category",)
    list_display_links = ("name",)

    def get_genres(self, instance):
        return [genre.name for genre in instance.genres.all()]


class OrderItemTabular(admin.TabularInline):
    model = Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    search_fields = ("name",)
    ordering = ("-id",)
    inlines = [
        OrderItemTabular,
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "author",
        "score",
        "pub_date",
        "title_id",
    )
    search_fields = ("text", "author")
    list_filter = ("author",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "author",
        "pub_date",
    )
    search_fields = ("text", "author")
    list_filter = ("author",)
