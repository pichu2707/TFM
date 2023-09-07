
from django.db.models.query import QuerySet
from django.shortcuts import render
import requests
from django.views.generic import (
    ListView,
)

from .models import ScraperPrensarank
# Create your views here.
class Prensarank(ListView):
    
    context_object_name='prensarank'
    paginate_by = 15
    model = ScraperPrensarank
    template_name="scrapers/prensarank.html"
    
    # def get_queryset(self):
    #     kword = self.request.GET.get("kword", '')
    #     country = self.request.GET.get("country", '')
    #     # consulta de búsqueda
    #     resultado = ScraperPrensarank.objects.buscar_web(kword, country)
    #     return resultado
