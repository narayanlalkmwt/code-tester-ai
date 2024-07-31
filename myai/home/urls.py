from django.urls import path
from .views import index, language, setquestion, level, answer, login, signup, feedback

urlpatterns = [
    path("", index, name='home'),
    path("language", language, name='language'),
    path("setquestion", setquestion, name='setquestion'),
    path("level", level, name='level'),
    path("answer", answer, name='answer'),
    path("login", login, name='login'),
    path("signup", signup, name='signup'),
    path("feedback", feedback, name='feedback'),
]
