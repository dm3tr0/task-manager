from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, FormView, TemplateView, View

from authentication.forms import LoginForm, RegistrationForm
from authentication.models import UserToken

User = get_user_model()

class LoginView(FormView):
    
    form_class = LoginForm
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('auth:account')

    def form_valid(self, form):
        login(self.request, User.objects.get(email=form.cleaned_data['email']), backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


class RegisterView(CreateView):
    
    form_class = RegistrationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        return super().form_valid(form)


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/account.html'


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('auth:login'))

class UserConfirmView(View):
    def get(self, request, token=None):
        token = get_object_or_404(UserToken, token=token)
        if token.used_at:
            return HttpResponseNotFound()
        user = token.user
        token.used_at = now()
        token.save()
        user.is_active = True
        user.save()

        return HttpResponseRedirect(reverse_lazy('auth:login'))

class AdminView(TemplateView):
    template_name = 'authentication/admin.html'