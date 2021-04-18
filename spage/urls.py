from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('aboutUs/',views.AboutUs.as_view(),name='about'),
    path('contactUs/', views.ContactUsView, name='contact_us'),
    path('success/', views.successView.as_view(), name='contact_success'),
    path('faq/', views.FAQ.as_view(), name='faq'),
    path('', views.HomePage.as_view(), name='home'),
]
