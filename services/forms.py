from django import forms
from models.models import Question, Answer, Game, Participant

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer','correct']      
        
class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['state']


        