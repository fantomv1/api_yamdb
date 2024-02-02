from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from reviews.models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "role")
    list_editable = ("role",)
    search_fields = ("username",)
    list_filter = ("role",)
    list_display_links = ("username",)
    BaseUserAdmin.fieldsets += (("Extra Fields", {"fields": ("bio", "role")}),)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "category",
        "_genre",
    )
    search_fields = ("name",)
    list_filter = ("category",)
    list_display_links = ("name",)

    @admin.display(
        description="Жанры",
    )
    def _genre(self, obj):
        return ",".join([genre.name for genre in obj.genre.all()])


class OrderItemTabular(admin.TabularInline):
    model = Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    list_editable = ("slug",)
    search_fields = ("name",)
    list_display_links = ("name",)
    ordering = ("-id",)
    inlines = [
        OrderItemTabular,
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    list_editable = ("slug",)
    search_fields = ("name",)
    list_display_links = ("name",)


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
