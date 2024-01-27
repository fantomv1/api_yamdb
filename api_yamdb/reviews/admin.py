from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import User, Category, Comment, Genre, Review, Title


UserAdmin.fieldsets += (("Extra Fields", {"fields": ("bio", "role")}),)

admin.site.register(User, UserAdmin)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category'
    )
    list_editable = (
        'category',
    )
    search_fields = ('name',)
    list_filter = ('category',)
    list_display_links = ('name',)


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Comment)
