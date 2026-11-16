from django.contrib import admin

from .models import  Entry, Category, Tag
# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Entry)