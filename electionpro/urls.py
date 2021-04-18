from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('ElectionResult/<slug:election_url>/',views.ElectionResult.as_view(),name='election_result_url'),
    path('LastElectionResult/',views.LastElectionResult.as_view(),name='election_result'),
    path('ElectionHistory/',views.ElectionHistory.as_view(),name='election_history'),
    path('ProfilePanel/',views.ProfilePanel.as_view(),name='profile_panel'),

]

