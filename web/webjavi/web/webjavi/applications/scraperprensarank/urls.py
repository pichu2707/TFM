from django.urls import path

from . import views

app_name = "scraperprensarank_app"

urlpatterns = [
    path('prensarank/', 
        views.Prensarank.as_view(),
        name='lista-prensarank',
    ),
]