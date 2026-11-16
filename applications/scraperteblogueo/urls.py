from django.urls import path

from . import views

app_name = "scraperteblogueo_app"

urlpatterns = [
    path('teblogueo/', 
        views.ListTeblogueo.as_view(),
        name='lista-teblogueo',
    ),
]