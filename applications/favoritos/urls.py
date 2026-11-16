from django.urls import path
from . import views

app_name="favoritos_app"

urlpatterns = [
    path(
        'perfil/',
        views.UserPageListView.as_view(),
        name='perfil',
    ),
    path(
        'add-entrada/<pk>/',
        views.AddFavoritosView.as_view(),
        name='add-favoritos',
    ),
    path(
        'delete-favorites/<pk>/',
        views.FavoritesDeleteView.as_view(),
        name='delete-favoritos',
    ),
]