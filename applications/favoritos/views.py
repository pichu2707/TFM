from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
#
from django.views.generic import (
    ListView,
    View,
    DeleteView,
)

from applications.entrada.models import Entry

from .models import Favorites


class UserPageListView(LoginRequiredMixin,ListView):
    template_name = "favoritos/perfil.html"
    context_object_name='entradas_user'
    login_url=reverse_lazy('users_app:user-login')

    def get_queryset(self):
        return Favorites.objects.entradas_user(self.request.user)
    
    
class AddFavoritosView(LoginRequiredMixin, View):
    login_url=reverse_lazy('users_app:user-login')
    def post(self,request, *args, **kwargs):
        #recuperamos el favorito
        usuario=self.request.user
        entrada=Entry.objects.get(id=self.kwargs['pk'])
        #Registramos el favorito
        Favorites.objects.create(
            user=usuario,
            entry=entrada,
        )
        
        return HttpResponseRedirect(
            reverse(
                'favoritos_app:perfil',
            )
        )

class FavoritesDeleteView(DeleteView):
    model = Favorites
    success_url = reverse_lazy('favoritos_app:perfil')


