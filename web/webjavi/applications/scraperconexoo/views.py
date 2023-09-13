from django.db.models.query import QuerySet
from django.shortcuts import render
import requests
from django.views.generic import (
    ListView,
)

# Create your views here.

from .models import scraperConexoo
# Create your views here.
class Prensarank(ListView):
    
    context_object_name='Conexoo'
    paginate_by = 15
    model = scraperConexoo
    template_name="scrapers/conexoo.html"