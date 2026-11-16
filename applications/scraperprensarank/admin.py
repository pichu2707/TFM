from django.contrib import admin
from .models import ScraperPrensarank

# Register your models here.

class PrensarankAdmin(admin.ModelAdmin):
    list_display=(
                'name',
                'price',
                'da',
                'traffic',
                )

#     # list_filter= ('name','da','price')
#     # filter_horizontal=('name')

#admin.site.register(ScraperPrensarank, PrensarankAdmin)
admin.site.register(ScraperPrensarank, PrensarankAdmin)