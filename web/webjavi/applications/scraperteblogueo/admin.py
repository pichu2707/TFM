from django.contrib import admin

from .models import ScraperTeblogueo

# Register your models here.
class TeblogueoAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'ppvp',
        'visits_month',
    )

admin.site.register(ScraperTeblogueo, TeblogueoAdmin)