from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView , TemplateView
from .forms import CustomUserCreationForm

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

class ResetPassword(TemplateView):
    template_name = 'registration/password_reset_form.html'