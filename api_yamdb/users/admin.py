from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from reviews.models import Category, Comment, Genre, Genre_title, Review, Title

from .models import User


@admin.register(
    User,
)
class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': (
            'bio',
            'role',
        )}),
    )

    list_display = (
        'username',
        'email',
        'bio',
        'role',
        'is_staff',
    )

    list_filter = (
        'role',
        'username',
    )

    list_editable = (
        'role',
    )

    search_fields = (
        'username',
    )

    list_display_links = (
        'username',
    )


@admin.register(
    Category,
)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


@admin.register(
    Genre,
)
class GenreAdmins(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


@admin.register(
    Comment,
)
class CommentAdmin(admin.ModelAdmin):
    model = Comment

    list_display = (
        'text',
        'author',
        'review',
        'pub_date',
    )
    list_filter = (
        'pub_date',
        'author__username',
    )
    list_editable = (
        'text',
    )
    search_fields = (
        'author__username',
    )
    list_display_links = (
        'pub_date',
    )


@admin.register(
    Title,
)
class TitleAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'year',
        'category',
        'get_genre_list',
        'description',
    )

    filter_horisontal = (
        'category',
        'get_genre_list',
    )

    list_filter = (
        'name',
        'year',
        'category__name',
    )

    list_editable = (
        'category',
    )

    search_fields = (
        'name',
        'year',
        'category__name',
    )

    list_display_links = (
        'name',
    )


@admin.register(
    Review,
)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'title',
        'pub_date',
        'score',
    )

    list_filter = (
        'text',
        'author__username',
        'title',
        'score',
        'pub_date'
    )

    list_editable = (
        'text',
    )

    search_fields = (
        'text',
        'author__username',
        'title',
        'score',
    )

    list_display_links = (
        'title',
    )


@admin.register(
    Genre_title,
)
class Genre_titleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'genre',
    )

    list_editable = (
        'genre',
    )


admin.site.empty_value_display = 'Не задано'
