from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Post, Category, Location


User = get_user_model()

admin.site.empty_value_display = 'Не задано'


class UserAdmin(BaseUserAdmin):

    list_display = BaseUserAdmin.list_display + ('post_count',)

    def post_count(self, obj):
        """Возвращает количество постов пользователя"""
        return Post.objects.filter(author=obj).count()

    post_count.short_description = 'Количество постов'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'pub_date', 'is_published')
    list_filter = ('is_published', 'category', 'pub_date')
    search_fields = ('title', 'author__username')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    search_fields = ('title', 'slug')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    search_fields = ('name',)
