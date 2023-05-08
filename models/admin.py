from django.contrib import admin
from .models import (
    User, Questionnaire, Question, Answer,
    Game, Participant, Guess
)


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question', 'questionnaire', 'answerTime',
        'created_at', 'updated_at'
    )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'correct')


class GameAdmin(admin.ModelAdmin):
    list_display = (
        'publicId', 'questionnaire', 'state',
        'countdownTime', 'questionNo', 'created_at'
    )


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('alias', 'game', 'points', 'uuidP')


class GuessAdmin(admin.ModelAdmin):
    list_display = ('participant', 'game', 'question', 'answer')


admin.site.register(User)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Guess, GuessAdmin)