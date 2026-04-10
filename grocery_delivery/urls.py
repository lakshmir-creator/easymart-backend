from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegisterUserAPI.as_view()),
    path('login/', views.LoginUserAPI.as_view()),
]