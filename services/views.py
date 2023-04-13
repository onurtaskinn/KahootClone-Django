from urllib import response
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView
from models.constants import FINISHED, WAITING
from models.models import Questionnaire
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic import CreateView
from models.models import Question
from .forms import GameForm, QuestionForm
from models.models import Answer
from .forms import AnswerForm
from models.models import Game
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from models.models import Participant
from django.views.generic import TemplateView
from django.shortcuts import render

from rest_framework import serializers



class HomeView(ListView):
    model = Questionnaire
    template_name = 'servicesTemplates/home.html'
    context_object_name = 'questionnaires'
    paginate_by = 40

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user).order_by('-updated_at')
        return Questionnaire.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_questionnaire_list'] = context['questionnaires']
        return context
    
class DoesNotBelongView(ListView):
    model = Game
    template_name = 'servicesTemplates/DNB.html'


        

    

            ### QUESTIONARIE VIEWS ###


class QuestionnaireDetailView(LoginRequiredMixin,DetailView):
    model = Questionnaire
    template_name = 'servicesTemplates/questionnaire_detail.html'

    def get_queryset(self):
        return Questionnaire.objects.filter(user=self.request.user)



class QuestionnaireListView(LoginRequiredMixin,ListView):
    model = Questionnaire
    template_name = 'servicesTemplates/questionnaire_list.html'
    context_object_name = 'questionnaire_list' 

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user).order_by('-updated_at')
        # else:
        #     return Questionnaire.objects.none()  
            
        
        


class QuestionnaireRemoveView(LoginRequiredMixin,DeleteView):
    model = Questionnaire
    template_name = 'servicesTemplates/questionnaire_remove.html'
    success_url = reverse_lazy('questionnaire-list')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user)
        # else:
        #     return Questionnaire.objects.none()

        
        


class QuestionnaireUpdateView(LoginRequiredMixin,UpdateView):
    model = Questionnaire
    fields = ['title']
    template_name = 'servicesTemplates/questionnaire_update.html'
    success_url = reverse_lazy('questionnaire-list') 

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user)
        # else:
        #     return Questionnaire.objects.none()




class QuestionnaireCreateView(LoginRequiredMixin, CreateView):
    model = Questionnaire
    fields = ['title']
    success_url = reverse_lazy('questionnaire-list')
    template_name = 'servicesTemplates/questionnaire_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response


            ### QUESTION VIEWS ###


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'servicesTemplates/question_detail.html'
    success_url = reverse_lazy('questionnaire-list') 

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Question.objects.filter(questionnaire__user=self.request.user)
        # else:
        #     return Question.objects.none()
        

class QuestionRemoveView(LoginRequiredMixin,DeleteView):
    model = Question
    template_name = 'servicesTemplates/question_remove.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Question.objects.filter(questionnaire__user=self.request.user)
        # else:
        #     return Question.objects.none()
        
    def get_success_url(self):
        return reverse('questionnaire-detail', kwargs={'pk': self.object.questionnaire.pk})    
            


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'servicesTemplates/question_create.html'

    def form_valid(self, form):
        #print("form valid")
        form.instance.questionnaire = Questionnaire.objects.get(pk=self.kwargs['questionnaireid'])
        return super().form_valid(form)

    # def get_queryset(self):
    #     print("get queryset")        
    #     if self.request.user.is_authenticated:
    #         return Question.objects.filter(questionnaire__user=self.request.user)
    #     else:
    #         return Question.objects.none()
    
    def get_success_url(self):
        #print("get success url")        
        return reverse('questionnaire-detail', kwargs={'pk': self.object.questionnaire.pk})     
    
       
    
    
class QuestionUpdateView(LoginRequiredMixin,UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'servicesTemplates/question_update.html'

    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.object.pk})
    
    
                
                
                
                ### ANSWER VIEWS ###

        
class AnswerCreateView(LoginRequiredMixin,CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'servicesTemplates/answer_create.html'

    def form_valid(self, form):
        form.instance.question = Question.objects.get(pk=self.kwargs['questionid'])
        return super().form_valid(form)

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Answer.objects.filter(question__questionnaire__user=self.request.user)
    #     else:
    #         return Answer.objects.none()
    
    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.object.question.pk})        

        
        
class AnswerRemoveView(LoginRequiredMixin,DeleteView):
    model = Answer
    template_name = 'servicesTemplates/answer_remove.html'

    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.object.question.pk})
    



class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'servicesTemplates/answer_update.html'
    
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Answer.objects
        # else:
        #     return Answer.objects.none()

    def form_valid(self, form):
        answer = Answer.objects.get(pk=self.kwargs['pk'])
        form.instance.question = answer.question
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.object.question.pk})
    
    



            ### GAME VIEWS ###







class GameCreateView(View):
    def get(self, request, questionnaireid):
        # Retrieve the corresponding Questionnaire object based on the ID
        questionnaire = Questionnaire.objects.get(id=questionnaireid)
        
        if questionnaire.user != request.user:
            # Redirect to another page if the user is not the owner of the questionnaire
            return redirect('doesNot-Belong')

        # Create a new Game instance with the corresponding questionnaire
        game = Game.objects.create(questionnaire=questionnaire)
        game.save()
        
        request.session['game_public_id'] = game.publicId
        request.session['game_state'] = WAITING
        #request.session['game'] = game
        
        participant = Participant.objects.create(game=game, alias = self.request.user , points = 10)
        participant = Participant.objects.create(game=game, alias = "ozan" , points = 10)
        participant = Participant.objects.create(game=game, alias = "mehmet" , points = 10)
        participant = Participant.objects.create(game=game, alias = "gulen" , points = 10)
        

        # Redirect to the detail view for the newly created game
        return redirect('game-updateparticipant', public_id=game.publicId)




class GameUpdateParticipantView(TemplateView):
    template_name = 'servicesTemplates/game_updateparticipant.html'
    participants_template = 'servicesTemplates/participants_list_ajax.html'

    def get(self, request, *args, **kwargs):
        public_id = self.kwargs.get('public_id') or self.request.session.get('game_public_id')
        game = Game.objects.filter(publicId=public_id).first()
        
        #request.session['game'] = game
        if(game):
            request.session['game_public_id'] = game.publicId

        if not game or game.questionnaire.user != request.user:
            return redirect('doesNot-Belong')

        context = self.get_context_data(public_id=public_id, game=game)
        if request.is_ajax():
            return render(request, self.participants_template, context)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if not self.request.user.is_authenticated:
        #     return {'error_message': 'does not belong to logged user'}

        game = kwargs.get('game')

        # if not game:
        #     return {'error_message': 'game not found'}
        # if game.questionnaire.user != self.request.user:
        #     return {'error_message': 'This game does not belong to the logged user'}

        context.update({
            'public_id': kwargs.get('public_id'),
            'questionarie': game.questionnaire,
            'game': game,
            'participants': game.participants.all()
        })

        return context
    
    
    
    
    
    
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from models.constants import WAITING, QUESTION, ANSWER, LEADERBOARD
from models.models import Game, Question, Participant


class GameCountdownView(View):
    def get_context_data(self, game_state, game):
        public_id = self.kwargs.get('public_id') or self.request.session.get('game_public_id')
        game = Game.objects.filter(publicId=public_id).first()
        numberOfQuestions = game.questionnaire.question_set.count()
        if game_state == WAITING:
            #print("get_contex_data WAITING")
            return {}
        elif game_state == QUESTION:
            #print("get_contex_data QUESTION")
            if(numberOfQuestions >= game.questionNo):
                question = Question.objects.filter(questionnaire = game.questionnaire)[game.questionNo-1]
                return {'question': question}
        elif game_state == ANSWER:
            #print("get_contex_data ANSWER")
            # Get the score, you may need to modify this based on your implementation
            points = Participant.objects.get(alias=self.request.user, game=game).points
            return {'score': points}
        elif game_state == "LEADERBOARD":
            #print("get_contex_data LEADERBOARD")
            points = Participant.objects.get(alias=self.request.user, game=game).points
            leaderboard = Participant.objects.filter(game=game).order_by('-points')
            return {'leaderboard': leaderboard}
        # elif game_state == "FINISHED":
        #     #print("get_contex_data LEADERBOARD")
        #     points = Participant.objects.get(alias=self.request.user, game=game).points
        #     leaderboard = Participant.objects.filter(game=game).order_by('-points')
        #     return {'leaderboard': leaderboard,}
    
    def get(self, request, *args, **kwargs):
        public_id = self.request.session.get('game_public_id') or self.kwargs.get('public_id') #or self.request.session.get('public_id')
        participant_alias = self.request.session.get('participant_alias')
        game = Game.objects.filter(publicId=public_id).first()
        
        numberOfQuestions = game.questionnaire.question_set.count() 
        
        
        if game.state == WAITING:
            #print("WAITING _ GET")
            context = self.get_context_data(game.state, game)    
            request.session['game_state'] = QUESTION
            #request.session['first'] = "true"
            game.state = QUESTION
            game.save()
            return render(request, 'countdownTemplatesForUser/countdown.html',context)

        current_state = request.session.get('game_state', None)
        
        # if game.state == COUNTDOWN:
        #     context = self.get_context_data(game.state, game)              
        #     print("COUNTDOWN state")
        #     request.session['game_state'] = QUESTION
        #     game.state = QUESTION
        #     game.save()
        #     print("if : countdown, state: question ")                  
        #     return render(request, 'countdownTemplatesForUser/countdown.html',context)

        if current_state == QUESTION:
            #print("QUESTION_ GET")
            context = self.get_context_data(game.state, game)   
            #question = Question.objects.first()  # Replace with the appropriate question retrieval method
            request.session['game_state'] = ANSWER
            game.state = ANSWER
            game.save()
            return render(request, 'countdownTemplatesForUser/question.html', context)

        if current_state == ANSWER:
            #print("ANSWER _ GET")
            context = self.get_context_data(game.state, game)                                    
            request.session['game_state'] = QUESTION if not numberOfQuestions==game.questionNo else LEADERBOARD
            game.questionNo += 1
            game.state = request.session['game_state']
            game.save()
            return render(request, 'countdownTemplatesForUser/score.html', context)


        if current_state == LEADERBOARD:
            #print("LEADERBOARD _ GET")
            request.session['game_state'] = FINISHED
            context = self.get_context_data(game.state, game)                        
            game.state = FINISHED
            game.save()
            leaderboard = []              # Replace with the actual leaderboard calculation logic
            return render(request, 'countdownTemplatesForUser/leaderboard.html', context)

        return redirect('/')  # Replace with an appropriate redirect URL in case of any issues
    
    
    def post(self, request, *args, **kwargs):
        #print("POST")
        public_id = self.kwargs.get('public_id') or self.request.session.get('game_public_id')
        current_state = request.session.get('game_state', None)
        game = Game.objects.filter(publicId=public_id).first()
        numberOfQuestions = game.questionnaire.question_set.count()

        if current_state == ANSWER:
            # Get the selected answer from the form data
            answer_id = request.POST.get('answer', None)
            #print("answer id : ", answer_id)
            
            if answer_id:
                # Get the answer object from the database
                selected_answer = Answer.objects.filter(id=answer_id).first()
                if selected_answer:
                    # Compare the selected answer with the correct answer and update the score
                    is_correct = selected_answer.correct
                    #print(Participant.objects.all())
                    participant = Participant.objects.get(alias=self.request.user, game=game)
                    if is_correct:
                        participant.points += 10
                        participant.save()

            # Move to the next question or leaderboard
            request.session['game_state'] = QUESTION if not numberOfQuestions==game.questionNo else LEADERBOARD
            game.questionNo += 1
            game.save()

        # Redirect to the appropriate view based on the game state
        if request.session['game_state'] == QUESTION:
            return redirect('game-count-down')
        elif request.session['game_state'] == LEADERBOARD:
            return redirect('game-count-down')

        #return redirect('/')  # Replace with an appropriate redirect URL in case of any issues
        
        