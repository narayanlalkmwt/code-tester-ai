from django.contrib import admin
from django.urls import path
from .views import index, language, setquestion, level, answer, login,logout, signup, feedback

urlpatterns = [
    path("", index, name='home'),
    path("index", index, name='index'),
    path("language", language, name='language'),
    path("setquestion", setquestion, name='setquestion'),
    path("level", level, name='level'),
    path("answer", answer, name='answer'),
    path("login", login, name='login'),
    path("logout", logout, name='logout'),
    path("signup", signup, name='signup'),
    path('feedback/<int:answer_id>/', feedback, name='feedback'),
]
