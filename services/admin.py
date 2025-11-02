from django.contrib import admin
from .models import Category, Service

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'city', 'price', 'is_active', 'category')
    list_filter = ('city', 'is_active', 'category')
    search_fields = ('name', 'description', 'provider__username')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'is_active')
    raw_id_fields = ('provider', 'category')
