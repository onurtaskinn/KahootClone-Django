import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from models.constants import ANSWER, LEADERBOARD, QUESTION, WAITING, FINISHED
from models.models import Answer, Game, Participant, Question, Questionnaire, Guess
from .forms import AnswerForm, GameForm, ParticipantForm, QuestionForm




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
        


class QuestionnaireRemoveView(LoginRequiredMixin,DeleteView):
    model = Questionnaire
    template_name = 'servicesTemplates/questionnaire_remove.html'
    success_url = reverse_lazy('questionnaire-list')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user)
        
        


class QuestionnaireUpdateView(LoginRequiredMixin,UpdateView):
    model = Questionnaire
    fields = ['title']
    template_name = 'servicesTemplates/questionnaire_update.html'
    success_url = reverse_lazy('questionnaire-list') 

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user)




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
        

class QuestionRemoveView(LoginRequiredMixin,DeleteView):
    model = Question
    template_name = 'servicesTemplates/question_remove.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Question.objects.filter(questionnaire__user=self.request.user)

        
    def get_success_url(self):
        return reverse('questionnaire-detail', kwargs={'pk': self.object.questionnaire.pk})    
            


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'servicesTemplates/question_create.html'

    def form_valid(self, form):
        form.instance.questionnaire = Questionnaire.objects.get(pk=self.kwargs['questionnaireid'])
        return super().form_valid(form)
    
    def get_success_url(self):      
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
        
        #participant = Participant.objects.create(game=game, alias = self.request.user , points = 10)

        # Redirect to the detail view for the newly created game
        return redirect('game-updateparticipant', public_id=game.publicId)




class GameUpdateParticipantView(TemplateView):
    template_name = 'servicesTemplates/game_updateparticipant.html'
    participants_template = 'servicesTemplates/participants_list_ajax.html'

    def get(self, request, *args, **kwargs):
        public_id = (
            self.kwargs.get('public_id') or self.request.session.get('game_public_id')
        )
        game = Game.objects.filter(publicId=public_id).first()

        if game:
            request.session['game_public_id'] = game.publicId

        if not game or game.questionnaire.user != request.user:
            return redirect('doesNot-Belong')

        context = self.get_context_data(public_id=public_id, game=game)
        if request.is_ajax():
            return render(request, self.participants_template, context)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        game = kwargs.get('game')
        context.update({
            'public_id': kwargs.get('public_id'),
            'questionarie': game.questionnaire,
            'game': game,
            'participants': game.participants.all()
        })

        return context
    
    
    
    
    
    



class GameCountdownView(View):
    def get_context_data(self, game_state, game):
        public_id = (
            self.kwargs.get('public_id') or self.request.session.get('game_public_id')
        )
        game = Game.objects.filter(publicId=public_id).first()
        numberOfQuestions = game.questionnaire.question_set.count()
        if game_state == WAITING:
            return {}
        
        elif game_state == QUESTION:

            if(numberOfQuestions >= game.questionNo):
                question = Question.objects.filter(questionnaire = game.questionnaire)[game.questionNo-1]
                return {'question': question}
            
        elif game_state == ANSWER:
            leaderboard = Participant.objects.filter(game=game).order_by('-points')
            return {'leaderboard': leaderboard}

        elif game_state == "LEADERBOARD":
            leaderboard = Participant.objects.filter(game=game).order_by('-points')
            return {'leaderboard': leaderboard}

    
    def get(self, request, *args, **kwargs):
        public_id = self.request.session.get('game_public_id') or self.kwargs.get('public_id') #or self.request.session.get('public_id')
        participant_alias = self.request.session.get('participant_alias')
        game = Game.objects.filter(publicId=public_id).first()
        
        numberOfQuestions = game.questionnaire.question_set.count() 
        
        
        if game.state == WAITING:
            context = self.get_context_data(game.state, game)    
            request.session['game_state'] = QUESTION
            game.state = QUESTION
            game.save()
            return render(request, 'countdownTemplatesForUser/countdown.html',context)

        current_state = request.session.get('game_state', None)
        

        if current_state == QUESTION:
            context = self.get_context_data(game.state, game)   
            request.session['game_state'] = ANSWER
            game.state = ANSWER
            game.save()
            return render(request, 'countdownTemplatesForUser/question.html', context)

        if current_state == ANSWER:
            context = self.get_context_data(game.state, game)                                    
            request.session['game_state'] = QUESTION if not numberOfQuestions==game.questionNo else LEADERBOARD
            game.questionNo += 1
            game.state = request.session['game_state']
            game.save()
            return render(request, 'countdownTemplatesForUser/score.html', context)


        if current_state == LEADERBOARD:
            request.session['game_state'] = FINISHED
            context = self.get_context_data(game.state, game)                        
            game.state = FINISHED
            game.save()
            return render(request, 'countdownTemplatesForUser/leaderboard.html', context)

        return redirect('/')  # Replace with an appropriate redirect URL in case of any issues
    
    
    def post(self, request, *args, **kwargs):
        public_id = self.kwargs.get('public_id') or self.request.session.get('game_public_id')
        current_state = request.session.get('game_state', None)
        game = Game.objects.filter(publicId=public_id).first()
        numberOfQuestions = game.questionnaire.question_set.count()

        if current_state == ANSWER:
            # Get the selected answer from the form data
            answer_id = request.POST.get('answer', None)
            
            if answer_id:
                # Get the answer object from the database
                selected_answer = Answer.objects.filter(id=answer_id).first()
                if selected_answer:
                    # Compare the selected answer with the correct answer and update the score
                    is_correct = selected_answer.correct
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
        
        



# views.py


class GamePlayView(View):
    template_name = 'participantTemplates/game_play.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'participantTemplates/game_play.html', context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        public_id = context['public_id']
        participant_alias = context['participant_alias']
        game = Game.objects.filter(publicId=public_id).first()
        participant = Participant.objects.filter(game=game, alias=participant_alias).first()

        data = json.loads(request.body)
        selected_answer_id = data.get('selected_answer_id')

        selected_answer = Answer.objects.get(id=selected_answer_id)
        question = selected_answer.question
        
        guess =  Guess(participant=participant, game=game, question=question, answer=selected_answer)
        guess.save()
        
        if selected_answer.correct:
            request.session['previous_answer_correct'] = True
        else:
            request.session['previous_answer_correct'] = False

        participant.save()
        
        return JsonResponse({'success': True})

    
    def get_context_data(self,**kwargs):
        
        context = {}
        
        previous_answer_correct = self.request.session.get('previous_answer_correct', None)
        context['previous_answer_correct'] = previous_answer_correct
        
        participant_alias = self.request.session.get('participant_alias')
        public_id = self.kwargs.get('public_id')

        self.request.session['participant_alias'] = participant_alias
        self.request.session['public_id'] = public_id

        game = Game.objects.filter(publicId=public_id).first()
        participant = (
            Participant.objects.filter(game=game, alias=participant_alias).first()
        )
        numberOfQuestions = game.questionnaire.question_set.count()
        
        if(game.questionNo-1 >= 1):
            previous_question = Question.objects.filter(questionnaire = game.questionnaire)[game.questionNo-2]   
            context['previous_question'] = previous_question 
        
        if(numberOfQuestions>= game.questionNo):
            question = Question.objects.filter(questionnaire = game.questionnaire)[game.questionNo-1]       
            context['question'] = question     
            
        
        leaderboard = Participant.objects.filter(game=game).order_by('-points')
        context.update({
            'participant_alias': participant_alias,
            'public_id': public_id,
            'game_state': game.state,
            'game' : game,
            'question_no' : game.questionNo,
            'participant' : participant,
            'participants': game.participants.all(),
            'leaderboard' : leaderboard
        })
        return context
    



class CreateParticipantView(View):
    template_name = 'servicesTemplates/create_participant.html'

    def get(self, request, *args, **kwargs):
        public_id = self.kwargs.get('public_id')
        game = Game.objects.filter(publicId=public_id).first()
        

        form = ParticipantForm()
        context = {
            'form': form,
            'public_id': public_id,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        public_id = self.kwargs.get('public_id')
        game = Game.objects.filter(publicId=public_id).first()


        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.game = game
            participant.save()
            request.session['participant_alias'] = participant.alias

            # Redirect to the game page
            return redirect('game-play', public_id=public_id)

    
    
    
    
    # views.py

class GetGameStateView(View):
    def get(self, request, public_id):
        game = Game.objects.filter(publicId=public_id).first()
        data = {
            'game_state': game.state,
        }
        return JsonResponse(data)

