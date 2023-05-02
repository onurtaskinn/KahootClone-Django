from rest_framework import serializers
from models.models import Game, Participant, Guess, Question, User, Answer,Questionnaire


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'       


class QuestionSerializer(serializers.ModelSerializer):
    current_answers = serializers.SerializerMethodField()  # Add this line
    
    class Meta:
        model = Question
        fields = ['question','answerTime','current_answers']     #


    def get_current_answers(self, obj):
        answers = obj.answer_set.all()
        if answers.exists():
            return AnswerSerializer(answers, many = True).data
        return None


class GameSerializer(serializers.ModelSerializer):
    current_question = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'publicId', 'questionnaire', 'questionNo', 'state', 'countdownTime', 'created_at', 'current_question']
        
    def get_current_question(self, obj):
        questionnaire = obj.questionnaire
        questions = questionnaire.question_set.all()
        if questions.exists() and 0 < obj.questionNo <= len(questions):
            question = questions[obj.questionNo - 1]
            return QuestionSerializer(question).data
        return None

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']      

class ParticipantSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField(slug_field='publicId', queryset=Game.objects.all())
    
    class Meta:
        model = Participant
        fields = '__all__'

class GuessSerializer(serializers.ModelSerializer):
    participant = serializers.PrimaryKeyRelatedField(queryset=Participant.objects.all(), write_only=True)
    game = serializers.SlugRelatedField(slug_field='publicId', queryset=Game.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())  # Add this line

    class Meta:
        model = Guess
        fields = ['game', 'answer', 'participant', 'question']  
        

 
        
