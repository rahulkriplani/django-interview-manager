from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'Evaluator'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/edit$', views.edit_profile, name='edit_profile'),
    url(r'^password/$', views.change_password, name='change_password'),

    #Question URLs
    url(r'^question/$', views.QuestionList.as_view(), name='question_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.question_detail, name='question_detail'),
    url(r'^search/question/$', views.search_question, name='search_question'),
    url(r'^addquestion/$', views.QuestionCreate.as_view(), name='add_question'),


    #Candidate URLS
    url(r'^candidate/$', views.profile, name='profile'),
    url(r'^addcandidate/$', views.add_candidate, name='add_candidate'),
    url(r'^candidate/edit$', views.edit_candidate, name='edit_candidate'),
    url(r'^search/candidate/$', views.search_candidate, name='search_candidate'),

    ]
