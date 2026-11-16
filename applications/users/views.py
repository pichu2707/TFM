from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic.edit import(
    View,
    CreateView
)

from django.views.generic.edit import(
    FormView
)

from .forms import(
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
)

from .models import User
# Create your views here.

class UserRigesterView(FormView):
    template_name ='users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            full_name=form.cleaned_data['full_name'],
            date_birth=form.cleaned_data['date_birth']
        )
        return super(UserRigesterView, self).form_valid(form)

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('favoritos_app:perfil')

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)
    
class LogoutView(View):
    def get(self, requests, *arg, **kargs):
        logout(requests)
        return HttpResponseRedirect(
            reverse(
            'users_app:user-login'
            )
        )

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/apdate.html'
    from_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            email=usuario.email,
            password=form.clean_data['password1']
        )

        if user:
            new_password = form.clean_data['password2']
            usuario.set_password(new_password)
            usuario.save
    
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)