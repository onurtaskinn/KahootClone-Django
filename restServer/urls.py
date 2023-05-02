from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='api-home'),
    
    path('answers/', views.AnswerListView.as_view(), name='answer-list'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('guess/', views.GuessListView.as_view(), name='guess-list'),
    path('games/', views.GameListView.as_view(), name='game-list'),
    path('participants/', views.ParticipantListView.as_view(), name='participant-list'),

]