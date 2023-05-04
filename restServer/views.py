from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from models.constants import QUESTION
from models.models import Answer, Game, Participant, Guess, Question, Questionnaire, User
from .serializers import (GameSerializer, ParticipantSerializer,
                          GuessSerializer, UserSerializer, AnswerSerializer, QuestionSerializer)
from rest_framework.exceptions import ValidationError
from rest_framework import generics


class HomeView(APIView):
    def get(self, request):
        data = {
            "message": "Welcome to my API!",
            "endpoints": {
                "answers": "/api/answers/",
                "users": "/api/users/",
                "games": "/api/games/",
                "participants": "/api/participants/",
                "guesses": "/api/guess/",
            }
        }
        return Response(data)


class UserListView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            users = User.objects.all()
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(users, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class AnswerListView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            answers = Answer.objects.all()
        except Answer.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AnswerSerializer(answers, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    

class GameListView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            games = Game.objects.all()
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GameSerializer(games, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Prevent creating a new game
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)    








class GuessListView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            guess = Guess.objects.all()
        except Guess.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GuessSerializer(guess, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        gamePublicId = request.data.get('game')
        game = Game.objects.filter(publicId=gamePublicId).first()
        # if game and game.state != QUESTION:
        #     raise ValidationError({'detail': 'wait until the question is shown'})
        
        questionlist = game.questionnaire.question_set.all()
        question = questionlist[game.questionNo-1]

        # Retrieve the participant using the provided uuidp
        print(request.data)
        uuidp = request.data.get('uuidp')
        participant = Participant.objects.filter(uuidP=uuidp).first()

        if not participant:
            return Response({'detail': 'Participant not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the participant has already guessed for the current question
        existing_guess = Guess.objects.filter(participant=participant, question=question).first()
        if existing_guess:
            return Response({'detail': 'Participant already made a guess for this question'}, status=status.HTTP_403_FORBIDDEN)  # Add this line

        # Find the current question based on the game
        answerpk = request.data.get('answer')
        answerList = question.answer_set.all()
        answer = answerList[answerpk]
        
        # Update request data to include the participant's primary key and the question's primary key
        request_data = request.data.copy()
        request_data['participant'] = participant.pk
        request_data['question'] = question.pk 
        request_data['answer'] = answer.pk
        
        serializer = GuessSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ParticipantListView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            participants = Participant.objects.all()
        except Participant.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ParticipantSerializer(participants, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Get the game and alias from the request data
        game_public_id = request.data.get('game')
        alias = request.data.get('alias')

        # Check if a participant with the same alias exists
        game = Game.objects.filter(publicId=game_public_id).first()
        if game is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        participant_exists = game.participants.filter(alias=alias).exists()

        if participant_exists:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Create the participant if the alias is unique
        serializer = ParticipantSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



        
class GameDetailView(APIView):
    permission_classes = [permissions.AllowAny]


    
    def get(self, request, publicId):
        try:
            game = Game.objects.get(publicId=publicId)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, publicId):
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, publicId):
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)


    


    
class ParticipantDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    
    def get(self, request, pk):
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GuessDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)
    
    
class QuestionDetailView(APIView):
    permission_classes = [permissions.AllowAny]


    
    def get(self, request, id):
        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class GameParticipantsDetailView(generics.GenericAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def get(self, request, publicId):
        game = get_object_or_404(Game, publicId=publicId)
        participants = Participant.objects.filter(game=game)
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data)
    


