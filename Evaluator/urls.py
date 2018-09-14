from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse
from . import views

app_name = 'Evaluator'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^login/$', views.user_login, name='login_users'),

    url(r'^logout/$', logout, {'template_name': 'logout.html'}),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/edit$', views.edit_profile, name='edit_profile'),
    url(r'^password/$', views.change_password, name='change_password'),

    #Question URLs
    url(r'^questions/$', views.QuestionList.as_view(), name='question_list'),
    url(r'^question/details/(?P<question_id>[0-9]+)/$', views.question_detail, name='question_detail'),
    url(r'^search/question/$', views.search_question, name='search_question'),
    url(r'^addQuestion/$', views.create_question, name='add_question'),
    url(r'^editQuestion/(?P<que_pk>\d+)/$', views.edit_question, name='edit_question'),

    #Interview URLs
    url(r'^addInterview/$', views.add_interview, name='add_interview'),

    #Candidate URLS
    url(r'^candidate/$', views.profile, name='profile'),
    url(r'^addCandidate/$', views.add_candidate, name='add_candidate'),
    url(r'^editCandidate/(?P<candidate_pk>\d+)/$', views.edit_candidate, name='edit_candidate'),
    url(r'^search/candidate/$', views.search_candidate, name='search_candidate'),

    #Exam URLs
    url(r'Exams/$', views.exams, name="allexams"),
    #url(r'addexam/$', views.create_exam, name="createExam"),
    #url(r'^exam/(?P<exam_pk>\d+)/$', views.exam_details, name='examDetails'),
    url(r'^examPreface/$', views.exam_launch_page, name='examLaunch'),

    #Question Set URLs
    url(r'questionSets/$', views.question_sets, name="allQueSets"),
    url(r'addQuestionSet/$', views.create_question_set, name="createQuestionSet"),
    url(r'^qset/(?P<qset_pk>\d+)/$', views.question_set_details, name='question_set_details'),

    ]
