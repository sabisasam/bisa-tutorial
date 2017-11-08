from django.contrib import admin

from .models import Category, Fortune


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')


@admin.register(Fortune)
class FortuneAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'text')
