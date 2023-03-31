# Populate database
# This file has to be placed within the
# catalog/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# that is, populate.py.
#
# execute python manage.py  populate
#
# use module Faker generator to generate data
# (https://zetcode.com/python/faker/)
import os

from django.core.management.base import BaseCommand
from models.models import User as User
from models.models import Questionnaire as Questionnaire
from models.models import Question as Question
from models.models import Answer as Answer
from models.models import Game as Game
from models.models import Participant as Participant
from models.models import Guess as Guess
from models.constants import WAITING


from faker import Faker


# The name of this class is not optional must be Command
# otherwise manage.py will not process it properly
class Command(BaseCommand):
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = """populate kahootclone database
           """
    # if you want to pass an argument to the function
    # uncomment this line
    # def add_arguments(self, parser):
    #    parser.add_argument('publicId',
    #        type=int,
    #        help='game the participants will join to')
    #    parser.add_argument('sleep',
    #        type=float,
    #        default=2.,
    #        help='wait this seconds until inserting next participant')

    def __init__(self, sneaky=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # "if 'RENDER'" allows you to deal with different
        # behaviour in render.com and locally
        # That is, we check a variable ('RENDER')
        # that is only defined in render.com
        if 'RENDER' in os.environ:
            pass
        else:
            pass

        self.NUMBERUSERS = 4
        self.NUMBERQESTIONARIES = 30
        self.NUMBERQUESTIONS = 100
        self.NUMBERPARTICIPANTS = 20
        self.NUMBERANSWERPERQUESTION = 4
        self.NUMBERGAMES = 4

    # handle is another compulsory name, do not change it"
    # handle function will be executed by 'manage populate'
    def handle(self, *args, **kwargs):
        "this function will be executed by default"

        self.cleanDataBase()   # clean database
        # The faker.Faker() creates and initializes a faker generator,
        self.faker = Faker()
        self.user()  # create users
        self.questionnaire()  # create questionaries
        self.question()  # create questions
        self.answer()  # create answers
        self.game()  # create games

    def cleanDataBase(self):
        Guess.objects.all().delete()
        Participant.objects.all().delete()
        Game.objects.all().delete()
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Questionnaire.objects.all().delete()
        User.objects.all().delete()
        print("Cleaned database")


    def user(self):
        print("Users")
        for _ in range(self.NUMBERUSERS):
            user = User.objects.create(username=self.faker.user_name())
            print(f"Created user {user.username}")


    def questionnaire(self):
        print("Questionnaire")
        users = User.objects.all()
        for _ in range(self.NUMBERQESTIONARIES):
            questionnaire = Questionnaire.objects.create(title=self.faker.sentence(),
                                                          user=self.faker.random_element(users))
            print(f"Created questionnaire {questionnaire.title}")

    def question(self):
        print("Question")
        questionnaires = Questionnaire.objects.all()
        for _ in range(self.NUMBERQUESTIONS):
            question = Question.objects.create(question=self.faker.sentence(),
                                               questionnaire=self.faker.random_element(questionnaires),
                                               answerTime=self.faker.random_int(min=10, max=60))
            print(f"Created question {question.question}")


    def answer(self):
        print("Answer")
        questions = Question.objects.all()
        for question in questions:
            correct_answer = self.faker.random_int(min=0, max=3)
            for i in range(self.NUMBERANSWERPERQUESTION):
                answer = Answer.objects.create(answer=self.faker.sentence(),
                                               question=question,
                                               correct=(i == correct_answer))
                print(f"Created answer {answer.answer}")


    def game(self):
        print("Game")
        questionnaires = Questionnaire.objects.all()
        for _ in range(self.NUMBERGAMES):
            game = Game.objects.create(questionnaire=self.faker.random_element(questionnaires),
                                       state=WAITING,
                                       countdownTime=self.faker.random_int(min=5, max=30),
                                       questionNo=self.faker.random_int(min=1, max=10))
            print(f"Created game {game.publicId}")
