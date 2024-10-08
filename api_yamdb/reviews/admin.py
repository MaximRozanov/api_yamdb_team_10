from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_display_links = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    list_editable = (
        'text',
    )
    search_fields = ('review', 'author',)
    list_filter = ('pub_date',)
    list_display_links = ('author',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_display_links = ('name',)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'genre',
    )
    list_display_links = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'text',
        'score',
        'pub_date',
    )
    list_editable = (
        'text',
        'score',
    )
    search_fields = ('title', 'author',)
    list_filter = ('pub_date', 'score',)
    list_display_links = ('author',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category',
        'description',
    )
    list_editable = (
        'category',
        'description',
    )
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genre',)
    list_display_links = ('name',)
    filter_horizontal = ('genre',)
