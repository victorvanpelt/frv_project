from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as cu,
    currency_range,
)
import time

author = 'Victor'

doc = """
Raven Pre-tests
"""


class Constants(BaseConstants):
    name_in_url = 'raven'
    players_per_group = None
    num_rounds = 10
    AgreeChoices = [
        [1, 'Strongly disagree'],
        [2, 'Disagree'],
        [3, 'Neither agree nor disagree'],
        [4, 'Agree'],
        [5, 'Strongly agree']
    ]
    ConfidenceChoices = [
        [1, 'Not at all confident'],
        [2, 'Slightly confident'],
        [3, 'Somewhat confident'],
        [4, 'Fairly confident'],
        [5, 'Completely confident']
    ]

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            # p.participant.is_dofus = False
            p.participant.is_dropout = False
            p.participant.is_dropout_mate = False
            p.participant.no_time_left = False
            p.participant.number_correct = 0
            p.participant.no_time_left = 0
            p.participant.no_partner = False

            if self.session.config['incentives'] == 1:
                p.incentives = 1
            else:
                p.incentives = 0

            if self.session.config['rpi'] == 1:
                p.rpi = 1
            else:
                p.rpi = 0

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    incentives = models.IntegerField()
    rpi = models.IntegerField()

    #Control questions
    Instr1 = models.IntegerField(blank=False, choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect)
    Instr2 = models.IntegerField(blank=False, initial=None, min=1, max=8)

    Instr1_wrong = models.IntegerField(max=1, blank=True)
    Instr2_wrong = models.IntegerField(max=1, blank=True)

    task = models.IntegerField(initial=0, min=1, max=8)
    check_task = models.IntegerField(initial=None, blank=True)

    number_correct = models.IntegerField(initial=None, min=0, max=C.NUM_ROUNDS)
    time_left = models.FloatField(initial=None)

    def set_score(self):
        # Correct answers EASY
        #correct_answers = [5, 2, 4, 2, 4, 3, 7, 2, 7, 1]
        # Correct answers HARD
        correct_answers = [7, 4, 6, 2, 4, 7, 8, 7, 5, 5]
        #Correct Ansers MIXED
        #correct_answers = [3, 7, 2, 7, 1, 7, 4, 6, 2, 4]
        given_answers = []
        for i in range(1,self.subsession.round_number+1):
            given_answers.append(self.in_round(i).task)
        z = [int(i == j) for i, j in zip(correct_answers, given_answers)]
        self.number_correct = sum(z)
        self.participant.number_correct = self.number_correct
        self.time_left = max(self.participant.expiry - time.time(), 0)
        self.participant.time_left = self.time_left
        self.participant.answers = z