import json
from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from models.constants import QUESTION
from models.models import Questionnaire, User

from django.test import Client
from django.test import TestCase
from django.urls import reverse
from models.models import Game, Questionnaire, Question, Participant, Answer, User
from services.views import GameCountdownView

class GameCountdownViewTest(TestCase):

    def setUp(self):
        
            # Create a user and log them in
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        
        login_result = self.client.login(username="testuser", password="testpassword")  
        # Create necessary objects for the test
        questionnaire = Questionnaire.objects.create(title="Test Questionnaire",user = self.user)
        question = Question.objects.create(questionnaire=questionnaire, question="Test question")

        game = Game.objects.create(questionnaire=questionnaire, publicId='123456', state='WAITING', questionNo=1)
        participant = Participant.objects.create(game=game, alias="testuser", points=0)

        self.client.session['participant_alias'] = "testuser"
        self.client.session['public_id'] = '123456'
        self.client.session['game_public_id'] = '123456'
        self.client.session.save()
    

    def test_game_countdown_view_get(self):
        
        client = Client()
        client.force_login(self.user)

        # Set the session variables
        session = client.session
        session['participant_alias'] = "TestParticipant"
        session['public_id'] = '123456'
        session['game_public_id'] = '123456'
        session.save()

        response = client.get(reverse('game-count-down'))
        #response = self.client.get(reverse('game-count-down'))

        # Test that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Test that the view uses the correct template
        self.assertTemplateUsed(response, 'countdownTemplatesForUser/countdown.html')

        # Test any other required behavior of the view
        # ...

    def test_game_countdown_view_question(self):
        game = Game.objects.get(publicId='123456')
        game.state = 'QUESTION'
        game.save()
        client = Client()
        client.force_login(self.user)

        # Set the session variables
        session = client.session
        session['participant_alias'] = "TestParticipant"
        session['public_id'] = '123456'
        session['game_public_id'] = '123456'
        session['game_state'] = 'QUESTION'  # Add this line
        session.save()



        # url = reverse('game-count-down', kwargs={'public_id': '123456'})
        # response = self.client.get(url)
        
        response = client.get(reverse('game-count-down'))



        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'countdownTemplatesForUser/question.html')

    def test_game_countdown_view_answer(self):
        game = Game.objects.get(publicId='123456')
        game.state = 'ANSWER'
        game.save()
        client = Client()
        client.force_login(self.user)

        # Set the session variables
        session = client.session
        session['participant_alias'] = "TestParticipant"
        session['public_id'] = '123456'
        session['game_public_id'] = '123456'
        session['game_state'] = 'ANSWER'  # Add this line
        session.save()        
        # url = reverse('game-count-down', kwargs={'public_id': '123456'})
        # response = self.client.get(url)
        
        response = client.get(reverse('game-count-down'))


        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'countdownTemplatesForUser/score.html')

    def test_game_countdown_view_leaderboard(self):
        print("LEADERBOARD TEST")
        
        game = Game.objects.get(publicId='123456')
        game.state = 'LEADERBOARD'
        game.save()
        client = Client()
        client.force_login(self.user)

        # Set the session variables
        session = client.session
        session['participant_alias'] = "TestParticipant"
        session['public_id'] = '123456'
        session['game_public_id'] = '123456'
        session['game_state'] = 'LEADERBOARD'  # Add this line
        session.save()        
        # url = reverse('game-count-down', kwargs={'public_id': '123456'})
        # response = self.client.get(url)
        
        response = client.get(reverse('game-count-down'))


        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'countdownTemplatesForUser/leaderboard.html')

    def test_game_countdown_view_finished(self):
        game = Game.objects.get(publicId='123456')
        game.state = 'FINISHED'
        game.save()
        client = Client()
        client.force_login(self.user)

        session = client.session
        session['participant_alias'] = "TestParticipant"
        session['public_id'] = '123456'
        session['game_public_id'] = '123456'
        session.save()        
        
        response = client.get(reverse('game-count-down'))

        self.assertEqual(response.status_code, 302) 


    def test_game_countdown_view_post_answer(self):
        game = Game.objects.get(publicId='123456')
        game.state = 'ANSWER'
        game.save()

        # Create a question and its answers
        question = Question.objects.create(questionnaire=game.questionnaire, question="Test question")
        correct_answer = Answer.objects.create(question=question, answer="Correct answer", correct=True)
        wrong_answer = Answer.objects.create(question=question, answer="Wrong answer", correct=False)

        client = Client()
        client.force_login(self.user)

        # Set the session variables
        session = client.session
        session['participant_alias'] = "TestParticipant"
        session['public_id'] = '123456'
        session['game_public_id'] = '123456'
        session['game_state'] = 'ANSWER'
        session.save()

        # Send POST request with the correct answer
        response = client.post(reverse('game-count-down'), data={'answer': correct_answer.id})

        # Test that the view returns a 302 status code (redirect)
        self.assertEqual(response.status_code, 302)

        # Test that the participant's score has been updated
        participant = Participant.objects.get(game=game, alias=self.user)
        self.assertEqual(participant.points, 10)      
        
    
    def test_game_countdown_view_post_leaderboard(self):
        game = Game.objects.get(publicId='123456')
        game.state = 'ANSWER'
        game.save()

        # Set game.questionNo to be the last question in the questionnaire
        game.questionNo = game.questionnaire.question_set.count()
        game.save()

        client = Client()
        client.force_login(self.user)

        # Set the session variables
        session = client.session
        session['participant_alias'] = "TestParticipant"
        session['public_id'] = '123456'
        session['game_public_id'] = '123456'
        session['game_state'] = 'ANSWER'
        session.save()

        # Send POST request without providing an answer
        response = client.post(reverse('game-count-down'), data={})

        # Test that the view returns a 302 status code (redirect)
        self.assertEqual(response.status_code, 302)

        # Test that the view redirects to the game-count-down view
        self.assertRedirects(response, reverse('game-count-down'))

        # Check if the game state has changed to LEADERBOARD
        session = client.session
        self.assertEqual(session['game_state'], 'FINISHED')          
        
        


from django.urls import reverse
from django.test import TestCase, Client
from models.models import Game, Questionnaire, User

class GameUpdateParticipantViewTest(TestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        # Create necessary objects for the test
        questionnaire = Questionnaire.objects.create(title="Test Questionnaire", user=self.user)
        self.game = Game.objects.create(questionnaire=questionnaire, publicId='123456', state='WAITING', questionNo=1)

    def test_game_update_participant_view_ajax(self):
        url = reverse('game-updateparticipant', kwargs={'public_id': '123456'})

        # Simulate an AJAX request by adding the 'HTTP_X_REQUESTED_WITH' header
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Test that the view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Test that the view uses the correct




from django.urls import reverse
from django.test import TestCase, Client
from django.http import JsonResponse
from models.models import Game, Participant, Questionnaire, Question, Answer, User


# Create your tests here.
class GamePlayViewTest(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        questionnaire = Questionnaire.objects.create(title='Test Questionnaire', user = self.user)
        question1 = Question.objects.create(question='Test Question1', questionnaire=questionnaire)
        question2 = Question.objects.create(question='Test Question2', questionnaire=questionnaire)
        answer1 = Answer.objects.create(answer='Test Answer', correct=True, question=question1)
        answer2 = Answer.objects.create(answer='Test Answer', correct=True, question=question2)

        game = Game.objects.create(
            publicId='123456',
            state='QUESTION',
            questionNo=2,
            questionnaire=questionnaire
        )

        participant = Participant.objects.create(
            alias='TestParticipant',
            game=game
        )

    def test_game_play_view_get(self):
        client = Client()
        client.force_login(self.user)

        session = client.session
        session['participant_alias'] = 'TestParticipant'
        session['public_id'] = '123456'
        session.save()

        response = client.get(reverse('game-play', kwargs={'public_id': '123456'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'participantTemplates/game_play.html')

    def test_game_play_view_post(self):
        client = Client()
        client.force_login(self.user)

        session = client.session
        session['participant_alias'] = 'TestParticipant'
        session['public_id'] = '123456'
        session.save()

        question = Question.objects.first()
        correct_answer = question.answer_set.first()

        response = client.post(
            reverse('game-play', kwargs={'public_id': '123456'}),
            data=json.dumps({'selected_answer_id': correct_answer.id}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

        participant = Participant.objects.get(alias='TestParticipant', game__publicId='123456')
        self.assertEqual(participant.points, 10)

        
        
class CreateParticipantViewTest(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        questionnaire = Questionnaire.objects.create(title='Test Questionnaire', user = self.user)        
        
        game = Game.objects.create(
            publicId='123456',
            state='WAITING',
            questionNo=1,
            questionnaire=questionnaire
        )

    def test_create_participant_view_get(self):
        client = Client()

        response = client.get(reverse('participant-create', kwargs={'public_id': '123456'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicesTemplates/create_participant.html')

    def test_create_participant_view_post(self):
        client = Client()

        response = client.post(
            reverse('participant-create', kwargs={'public_id': '123456'}),
            data={'alias': 'TestParticipant'}
        )

        self.assertEqual(response.status_code, 302)  # Check for redirect



from django.urls import reverse
from django.test import TestCase, Client

# Create your tests here.
class GetGameStateViewTest(TestCase):
    def setUp(self):
        # Create test data
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        questionnaire = Questionnaire.objects.create(title='Test Questionnaire', user = self.user)              
        
        game = Game.objects.create(
            publicId='123456',
            state='WAITING',
            questionNo=1,
            questionnaire=questionnaire
        )

    def test_get_game_state_view(self):
        client = Client()

        response = client.get(reverse('game-state', kwargs={'public_id': '123456'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        response_data = response.json()
        self.assertEqual(response_data['game_state'], 'WAITING')
        self.assertNotIn('error', response_data)
      
        


