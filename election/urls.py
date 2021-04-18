from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('newelection/', views.newelectionView, name='newelection'),

    url(r'^(?P<election_url>([A-Z]*[a-z]*[0-9]*)+)/check_national_code$',
        views.checkNationalCode,
        name='national_num_check'),

    url('submit/(?P<election_url>([A-Z]*[a-z]*[0-9]*[%]*)+)/(?P<national_number>(\d{10}))/$',views.submitVote, name='submit_vote')  ,
    path('votedone/', views.Votedone.as_view(), name='votedone'),
]