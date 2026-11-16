from django.contrib import admin

from .models import scraperConexoo
# Register your models here.

class ConexooAdmin(admin.ModelAdmin):
    list_display=(
                'url',
                'precio_post',
                'da',
                'traffic_organic',
                )

#     # list_filter= ('name','da','price')
#     # filter_horizontal=('name')

#admin.site.register(ScraperPrensarank, PrensarankAdmin)
admin.site.register(scraperConexoo,ConexooAdmin)