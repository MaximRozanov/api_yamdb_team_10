from django.contrib import admin

# Register your models here.

from .models import Review, Titles, Genre, GenreTitle, Category, Comment

# Register your models here.

admin.site.register(Review)
admin.site.register(Titles)
admin.site.register(Genre)
admin.site.register(GenreTitle)
admin.site.register(Category)
admin.site.register(Comment)
