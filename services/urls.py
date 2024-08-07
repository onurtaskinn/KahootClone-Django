from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('doesNotBelongToCurrentUser', views.DoesNotBelongView.as_view(), name='doesNot-Belong'),
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
    re_path(r'^services/gameUpdateParticipant/(?P<public_id>[0-9]+)?/$', views.GameUpdateParticipantView.as_view(), name='game-updateparticipant'),
    path('game-count-down/', views.GameCountdownView.as_view(), name='game-count-down'),
    path('game/createparticipant/<str:public_id>/', views.CreateParticipantView.as_view(), name='participant-create'),
    path('game/play/<int:public_id>/', views.GamePlayView.as_view(), name='game-play'),
    path('game/state/<str:public_id>/', views.GetGameStateView.as_view(), name='game-state'),
    

    ]

