from django.urls import path
from . import views
from django.views.generic import TemplateView
from todo.views import *
urlpatterns = [
    path('', views.index,name='index'),
    path('single_blog',views.Blog,name='single_blog'),
    path('blogs/<str:pk>',views.singleblog,name='blogs'),
    #path('post/<str:pk>', views.post, name='post'),
    #path('boss',views.boss_article,name='boss'),
    path('search',views.search,name='search'),
    path('shopInterface',views.shopInterface,name='shopInterface'),
    path('quiz',views.attemptQuiz,name='quiz'),
    path('contact',views.contact,name='contact'),
    path('service',views.service,name='service'),
    path('verse',views.showVerse,name='list_verse1'), 
    path('hadith',views.showHadith,name='list_hadith1'),
    path('home',views.homepage,name='home'),
]
