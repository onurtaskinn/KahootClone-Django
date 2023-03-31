from django.views.generic import ListView
from models.models import Questionnaire
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic import CreateView
from models.models import Question
from .forms import QuestionForm
from models.models import Answer
from .forms import AnswerForm
from .forms import GameForm
from models.models import Game
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages








class HomeView(ListView):
    model = Questionnaire
    template_name = 'servicesTemplates/home.html'
    context_object_name = 'questionnaires'
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user).order_by('-updated_at')
        return Questionnaire.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_questionnaire_list'] = context['questionnaires']
        return context

    


class QuestionnaireDetailView(LoginRequiredMixin,DetailView):
    model = Questionnaire
    template_name = 'servicesTemplates/questionnaire_detail.html'
    context_object_name = 'questionnaire'

    def get_queryset(self):
        return Questionnaire.objects.filter(user=self.request.user)



class QuestionnaireListView(LoginRequiredMixin,ListView):
    model = Questionnaire
    template_name = 'servicesTemplates/questionnaire_list.html'
    context_object_name = 'questionnaire_list' 

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user).order_by('-updated_at')
        else:
            return Questionnaire.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questionnaires'] = Questionnaire.objects.filter(user=self.request.user)
        return context        
            
        
        


class QuestionnaireRemoveView(LoginRequiredMixin,DeleteView):
    model = Questionnaire
    template_name = 'servicesTemplates/questionnaire_remove.html'
    success_url = reverse_lazy('questionnaire-list')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user)
        else:
            return Questionnaire.objects.none()

        
        


class QuestionnaireUpdateView(LoginRequiredMixin,UpdateView):
    model = Questionnaire
    fields = ['title']
    template_name = 'servicesTemplates/questionnaire_update.html'
    success_url = reverse_lazy('questionnaire-list') 


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user)
        else:
            return Questionnaire.objects.none()




class QuestionnaireCreateView(LoginRequiredMixin, CreateView):
    model = Questionnaire
    fields = ['title']
    success_url = reverse_lazy('questionnaire-list')
    template_name = 'servicesTemplates/questionnaire_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #Questionnaire.objects.filter(user=self.request.user).delete()
        response = super().form_valid(form)
        self.object.refresh_from_db()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questionnaires'] = Questionnaire.objects.filter(user=self.request.user).order_by('-created_at')
        return context


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Questionnaire.objects.filter(user=self.request.user)
        else:
            return Questionnaire.objects.none()
    def save(self, *args, **kwargs):
        # You can add any custom logic here if needed

        # Call the parent class's save method
        super(Questionnaire, self).save(*args, **kwargs)        
        
        

from django.http import Http404, HttpResponse, HttpResponseRedirect

class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'servicesTemplates/question_detail.html'
    context_object_name = 'question'
    success_url = reverse_lazy('questionnaire-list') 

    def get_object(self, queryset=None):
        question = super().get_object(queryset=queryset)
        if question.questionnaire.user != self.request.user:
            raise Http404("You are not authorized to view this question.")
        return question 
        

class QuestionRemoveView(LoginRequiredMixin,DeleteView):
    model = Question
    template_name = 'servicesTemplates/question_remove.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Question.objects.filter(questionnaire__user=self.request.user)
        else:
            return Question.objects.none()
        
    def get_success_url(self):
        return reverse('questionnaire-detail', kwargs={'pk': self.object.questionnaire.pk})    
            


class QuestionCreateView(LoginRequiredMixin,CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'servicesTemplates/question_create.html'
    success_url = reverse_lazy('questionnaire-list')

    def form_valid(self, form):
        form.instance.questionnaire = Questionnaire.objects.get(pk=self.kwargs['questionnaireid'], user=self.request.user)
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Question.objects.filter(questionnaire__author=self.request.user)
        else:
            return Question.objects.none()
    
    def get_success_url(self):
        return reverse('questionnaire-detail', kwargs={'pk': self.object.questionnaire.pk})        
    
    
class QuestionUpdateView(LoginRequiredMixin,UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'servicesTemplates/question_update.html'

    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.object.pk})

        
class AnswerCreateView(LoginRequiredMixin,CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'servicesTemplates/answer_create.html'
    # success_url = reverse_lazy('questionnaire-list') 

    def form_valid(self, form):
        form.instance.question = Question.objects.get(pk=self.kwargs['questionid'], questionnaire__user=self.request.user)
        return super().form_valid(form)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Answer.objects.filter(question__questionnaire__user=self.request.user)
        else:
            return Answer.objects.none()
    
    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.object.question.pk})        

        
        
class AnswerRemoveView(LoginRequiredMixin,DeleteView):
    model = Answer
    template_name = 'servicesTemplates/answer_remove.html'

    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.object.question.pk})
    


from django.shortcuts import get_object_or_404

class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'servicesTemplates/answer_update.html'

    def form_valid(self, form):
        answer = get_object_or_404(Answer, id=self.kwargs['pk'])
        answer.answer = form.cleaned_data.get('answer', answer.answer)
        answer.correct = form.cleaned_data.get('correct', answer.correct)

        answer.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.object.question.pk})




class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    #fields = []
    template_name = 'servicesTemplates/game_create.html'
    form_class = GameForm

    def form_valid(self, form):
        try:
            form.instance.questionnaire_id = self.kwargs['questionnaireid']
            response = super().form_valid(form)
            print("Game object before save:", self.object)
            self.object.save()  # Save the Game instance
            print("Game object after save:", self.object)
            return response
        except Exception as e:
            print("Form submission error:", e)
            return super().form_invalid(form)

    
    def get_success_url(self):
        return reverse('game-detail', kwargs={'pk': self.object.pk}) 
    
    
class GameDetailView(LoginRequiredMixin,DetailView):
    model = Game
    template_name = 'servicesTemplates/game_detail.html'
    context_object_name = 'game'

    #def get_queryset(self):
    #    return Game.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse('game-detail', kwargs={'pk': self.object.pk})      
    


#from django.shortcuts import render, redirect
#from django.views.generic import View
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib import messages
#from django.http import JsonResponse
#from models.models import Questionnaire, Game
#from .forms import GameCreateForm
#from django.views.generic.edit import FormView
#
#
#from django.shortcuts import render, redirect
#from django.views.generic import View
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib import messages
#from django.http import JsonResponse
#from models.models import Questionnaire, Game
#
#class GameCreateView(LoginRequiredMixin, View):
#    def get(self, request, questionnaireid):
#        try:
#            questionnaire = Questionnaire.objects.get(pk=questionnaireid, user=request.user)
#            game = Game.objects.create(questionnaire=questionnaire, state='waiting', countdownTime=10, questionNo=1)
#            request.session['game_id'] = game.id
#            data = {'status': 'success', 'game_id': game.id}
#            return JsonResponse(data)
#        except Questionnaire.DoesNotExist:
#            messages.error(request, 'does not belong to logged user')
#            #messages.error(request, 'Not authorized to create game')
#            return redirect('questionnaire-list')


        

        

    
