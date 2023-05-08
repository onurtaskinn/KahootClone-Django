from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from unittest.mock import Mock, MagicMock
from restServer.views import UserListView
from unittest.mock import patch
from models.models import Participant, User,Question,Answer,Questionnaire,Game,Guess
from .serializers import GameSerializer, GuessSerializer, ParticipantSerializer,UserSerializer,QuestionSerializer
import json

class HomeViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_home_view(self):
        url = reverse('api-home')  # Make sure to define the name 'home' in your urlpatterns
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = {
            "message": "Welcome to my API!",
            "endpoints": {
                "answers": "/api/answers/",
                "users": "/api/users/",
                "games": "/api/games/",
                "participants": "/api/participants/",
                "guesses": "/api/guess/",
            }
        }
        self.assertDictEqual(response.data, expected_data)


from django.contrib.auth import get_user_model
from restServer.serializers import UserSerializer

class UserListViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(username='user1', password='testpassword')
        self.user2 = get_user_model().objects.create_user(username='user2', password='testpassword')

    def test_user_list_view(self):
        url = reverse('user-list')  # Make sure to define the name 'user_list' in your urlpatterns
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertListEqual(response.data, serializer.data)

    
    
class TestAnswerListView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.questionnaire = Questionnaire.objects.create(title="Test Questionnaire", user=self.user)
        self.question = Question.objects.create(question="Test Question", questionnaire=self.questionnaire)
        self.answer = Answer.objects.create(answer="Test Answer", question=self.question, correct=True)
        self.url = reverse("answer-list")

    def test_get_all_answers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["answer"], "Test Answer")

    @patch("models.models.Answer.objects.all")
    def test_get_answers_exception(self, mock_all):
        mock_all.side_effect = Answer.DoesNotExist
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "User not found."})


class TestGameListView(APITestCase):
    
    def setUp(self):
        # Create sample data
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.questionnaire = Questionnaire.objects.create(title="Test Questionnaire", user=self.user)

        self.game1 = Game.objects.create(questionnaire=self.questionnaire)
        self.game2 = Game.objects.create(questionnaire=self.questionnaire)

    def test_get_games(self):
        response = self.client.get(reverse("game-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        self.assertEqual(response.data, serializer.data)

    @patch("models.models.Game.objects.all")
    def test_get_games_exception(self, mock_game_objects_all):
        mock_game_objects_all.side_effect = Game.DoesNotExist
        response = self.client.get(reverse("game-list"))
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Game not found."})
        


class TestGuessListView(APITestCase):

    def setUp(self):
        # Create sample data
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.questionnaire = Questionnaire.objects.create(title="Test Questionnaire", user=self.user)
        self.game = Game.objects.create(questionnaire=self.questionnaire)
        self.question = Question.objects.create(question="Test Question", questionnaire=self.questionnaire)
        self.answer1 = Answer.objects.create(answer="Test Answer 1", question=self.question, correct=True)
        self.answer2 = Answer.objects.create(answer="Test Answer 2", question=self.question, correct=False)
        self.participant = Participant.objects.create(game=self.game, alias="Test Participant")

    def test_get_guesses(self):
        response = self.client.get(reverse("guess-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        guesses = Guess.objects.all()
        serializer = GuessSerializer(guesses, many=True)
        self.assertEqual(response.data, serializer.data)

    @patch("models.models.Guess.objects.all")
    def test_get_guesses_exception(self, mock_guess_objects_all):
        mock_guess_objects_all.side_effect = Guess.DoesNotExist
        response = self.client.get(reverse("guess-list"))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Game not found."})




class TestParticipantListView(APITestCase):

    def setUp(self):
        # Create sample data
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.questionnaire = Questionnaire.objects.create(title="Test Questionnaire", user=self.user)
        self.game = Game.objects.create(questionnaire=self.questionnaire)
        self.participant = Participant.objects.create(game=self.game, alias="Test Participant")

    def test_get_participants(self):
        response = self.client.get(reverse("participant-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        participants = Participant.objects.all()
        serializer = ParticipantSerializer(participants, many=True)
        self.assertEqual(response.data, serializer.data)

    @patch("models.models.Participant.objects.all")
    def test_get_participants_exception(self, mock_participant_objects_all):
        mock_participant_objects_all.side_effect = Participant.DoesNotExist
        response = self.client.get(reverse("participant-list"))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Game not found."})

    def test_post_participant(self):
        data = {
            "game": self.game.publicId,
            "alias": "New Participant"
        }
        response = self.client.post(reverse("participant-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        participant = Participant.objects.get(pk=response.data["id"])
        self.assertEqual(participant.game, self.game)
        self.assertEqual(participant.alias, data["alias"])

    def test_post_participant_alias_exists(self):
        data = {
            "game": self.game.publicId,
            "alias": "Test Participant"
        }
        response = self.client.post(reverse("participant-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
class TestQuestionDetailView(APITestCase):

    def setUp(self):
        # Create sample data
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.questionnaire = Questionnaire.objects.create(title="Test Questionnaire", user=self.user)
        self.question = Question.objects.create(question="Sample Question", questionnaire=self.questionnaire)

    def test_get_question(self):
        response = self.client.get(reverse("api-question-detail", kwargs={"id": self.question.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = QuestionSerializer(self.question)
        self.assertEqual(response.data, serializer.data)

    @patch("models.models.Question.objects.get")
    def test_get_question_exception(self, mock_question_objects_get):
        mock_question_objects_get.side_effect = Question.DoesNotExist
        response = self.client.get(reverse("api-question-detail", kwargs={"id": 9999}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Question not found."})        
        


class TestGameParticipantsDetailView(APITestCase):

    def setUp(self):
        # Create sample data
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.questionnaire = Questionnaire.objects.create(title="Test Questionnaire", user=self.user)
        self.game = Game.objects.create(questionnaire=self.questionnaire, publicId=1234)
        self.participant1 = Participant.objects.create(game=self.game, alias="Participant 1")
        self.participant2 = Participant.objects.create(game=self.game, alias="Participant 2")

    def test_get_game_participants(self):
        response = self.client.get(reverse("game-participants", kwargs={"publicId": self.game.publicId}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        participants = Participant.objects.filter(game=self.game)
        serializer = ParticipantSerializer(participants, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_game_participants_not_found(self):
        response = self.client.get(reverse("game-participants", kwargs={"publicId": 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        