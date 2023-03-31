from django.urls import path
from . import views

#app_name = 'app_name'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('questionnaire/<int:pk>/', views.QuestionnaireDetailView.as_view(), name='questionnaire-detail'),
    path('questionnairelist/', views.QuestionnaireListView.as_view(), name='questionnaire-list'),
    path('questionnaireremove/<int:pk>/', views.QuestionnaireRemoveView.as_view(), name='questionnaire-remove'),
    path('questionnaireupdate/<int:pk>/', views.QuestionnaireUpdateView.as_view(), name='questionnaire-update'),
    path('questionnairecreate/', views.QuestionnaireCreateView.as_view(), name='questionnaire-create'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('questionremove/<int:pk>/', views.QuestionRemoveView.as_view(), name='question-remove'),
    path('questionupdate/<int:pk>/', views.QuestionUpdateView.as_view(), name='question-update'),
    path('questioncreate/<int:questionnaireid>/', views.QuestionCreateView.as_view(), name='question-create'),
    path('answercreate/<int:questionid>/', views.AnswerCreateView.as_view(), name='answer-create'),
    path('answerremove/<int:pk>/', views.AnswerRemoveView.as_view(), name='answer-remove'),
    path('answerupdate/<int:pk>/', views.AnswerUpdateView.as_view(), name='answer-update'),
    path('gamecreate/<int:questionnaireid>/', views.GameCreateView.as_view(), name='game-create'),
    path('game_succesfuly_created.html/', views.GameCreateView.as_view(), name='game-created-succesfuly'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),

]

