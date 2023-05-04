from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='api-home'),
    
    path('answers/', views.AnswerListView.as_view(), name='answer-list'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('guess/', views.GuessListView.as_view(), name='guess-list'),
    path('games/', views.GameListView.as_view(), name='game-list'),
    path('participants/', views.ParticipantListView.as_view(), name='participant-list'),
    
    
    path('games/<int:publicId>/', views.GameDetailView.as_view(), name='game-detail'),
    path('guesses/<int:pk>/', views.GuessDetailView.as_view(), name='guess-detail'),
    path('participants/<int:pk>/', views.ParticipantDetailView.as_view(), name='participant-detail'),
    path('questions/<int:id>/', views.QuestionDetailView.as_view(), name='api-question-detail'),
    
    path('game-participants/<int:publicId>/', views.GameParticipantsDetailView.as_view(), name='game-participants'),
]