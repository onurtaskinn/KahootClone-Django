from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random

class User(AbstractUser):
    """
    Default user class, just in case we want to add something extra in the future.
    """
    pass

class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class Question(models.Model):
    question = models.TextField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    answerTime = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField()

    def __str__(self):
        return self.answer

class Game(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    state = models.CharField(max_length=50)
    countdownTime = models.IntegerField()
    questionNo = models.IntegerField()
    publicId = models.IntegerField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.publicId} - {self.questionnaire.title}"

    def save(self, *args, **kwargs):
        if not self.publicId:
            self.publicId = random.randint(1, 10**6)
        super(Game, self).save(*args, **kwargs)

class Participant(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    uuid_p = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.alias} (Game {self.game.publicId})"

class Guess(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.answer.correct:
                self.participant.points += 1
                self.participant.save()

        super(Guess, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.participant.alias} guessed {self.answer.answer}"
