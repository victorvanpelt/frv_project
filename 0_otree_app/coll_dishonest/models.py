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


author = 'Victor Farah'

doc = """
FRV Experiments
"""


class Constants(BaseConstants):
    name_in_url = 'coll_dishonest'
    players_per_group = 2
    num_rounds = 1
    AgreeChoices = [
        [1, 'Strongly disagree'],
        [2, 'Disagree'],
        [3, 'Neither agree nor disagree'],
        [4, 'Agree'],
        [5, 'Strongly agree'],
    ]

class Subsession(BaseSubsession):
    def group_by_arrival_time_method(self, waiting_players):
        if len(waiting_players) >= 2:
            return waiting_players[:2]
        for player in waiting_players:
            if player.waiting_too_long():
                # make a single-player group.
                return [player]

class Group(BaseGroup):
    incentives = models.IntegerField()
    rpi = models.IntegerField()

    # Part 1 data
    number_correct_one = models.IntegerField()
    time_left_one = models.FloatField()
    number_correct_two = models.IntegerField()
    time_left_two = models.FloatField()
    payoff_part1_one = models.CurrencyField()
    payoff_part1_two = models.CurrencyField()
    winner_part1_one = models.IntegerField()
    winner_part1_two = models.IntegerField()

    def assign_stuff(self):
        for p in self.get_players():
            #Load dropout variables
            p.drop_out = p.participant.is_dropout
            p.drop_out_mate = p.participant.is_dropout_mate
            p.no_partner = p.participant.no_partner

            # Load conditions based on session config else randomize per dyad
        if self.session.config['incentives'] == 1:
            self.incentives = 1
        else:
            self.incentives = 0
        if self.session.config['rpi'] == 1:
            self.rpi = 1
        else:
            self.rpi = 0

        self.number_correct_one = self.get_player_by_id(1).participant.number_correct
        self.number_correct_two = self.get_player_by_id(2).participant.number_correct
        self.time_left_one = self.get_player_by_id(1).participant.time_left
        self.time_left_two = self.get_player_by_id(2).participant.time_left

        if self.incentives == 0:
            self.payoff_part1_one = cu(0.90)
            self.payoff_part1_two = cu(0.90)
            if self.number_correct_one > self.number_correct_two:
                self.winner_part1_one = 1
                self.winner_part1_two = 0
            elif self.number_correct_one < self.number_correct_two:
                self.winner_part1_one = 0
                self.winner_part1_two = 1
            elif self.number_correct_one == self.number_correct_two:
                if self.time_left_one > self.time_left_two:
                    self.winner_part1_one = 1
                    self.winner_part1_two = 0
                elif self.time_left_one < self.time_left_two:
                    self.winner_part1_one = 0
                    self.winner_part1_two = 1
                else:
                    self.payoff_part1_one = 0
                    self.payoff_part1_two = 0
        elif self.incentives == 1:
            if self.number_correct_one > self.number_correct_two:
                self.winner_part1_one = 1
                self.winner_part1_two = 0
                self.payoff_part1_one = cu(1.80)
                self.payoff_part1_two = cu(0)
            elif self.number_correct_one < self.number_correct_two:
                self.winner_part1_one = 0
                self.winner_part1_two = 1
                self.payoff_part1_one = cu(0)
                self.payoff_part1_two = cu(1.80)
            elif self.number_correct_one == self.number_correct_two:
                if self.time_left_one > self.time_left_two:
                    self.winner_part1_one = 1
                    self.winner_part1_two = 0
                    self.payoff_part1_one = cu(1.80)
                    self.payoff_part1_two = cu(0)
                elif self.time_left_one < self.time_left_two:
                    self.winner_part1_one = 0
                    self.winner_part1_two = 1
                    self.payoff_part1_one = cu(0)
                    self.payoff_part1_two = cu(1.80)
                else:
                    self.payoff_part1_one = cu(0)
                    self.payoff_part1_two = cu(0)
                    self.payoff_part1_one = 0
                    self.payoff_part1_two = 0

    check_report_one = models.IntegerField(initial=None, blank=True)
    check_report_two = models.IntegerField(initial=None, blank=True)
    report_one = models.IntegerField(initial=0, blank=False, min=1, max=6)
    report_two = models.IntegerField(initial=0, blank=False, min=1, max=6)

    # Payoffs saved at the end
    payoff_part2_one = models.CurrencyField(blank=True, initial=None)
    payoff_part2_two = models.CurrencyField(blank=True, initial=None)

    # This method triggers when a participant has to wait too long before part 2
    def no_partner_trigger(self):
        for p in self.get_players():
            p.participant.no_partner = True
            p.no_partner = True
            p.payoff = cu(0.90)

    def drop_out_trigger_one(self):
        for p in self.get_players():
            if p.id_in_group == 1:
                p.participant.is_dropout = True
                p.drop_out = True
                p.payoff = self.payoff_part1_one
            elif p.id_in_group == 2:
                p.participant.is_dropout_mate = True
                p.drop_out_mate = True
                if p.participant.is_dropout == False:
                    p.payoff = self.payoff_part1_two

    def drop_out_trigger_two(self):
        for p in self.get_players():
            if p.id_in_group == 2:
                p.participant.is_dropout = True
                p.drop_out = True
                p.payoff = self.payoff_part1_two
            elif p.id_in_group == 1:
                p.participant.is_dropout_mate = True
                p.drop_out_mate = True
                if p.participant.is_dropout == False:
                    p.payoff = self.payoff_part1_one

    def set_report_payoffs(self):
        #Assign payoffs at group level
        #Baseline payoff = 0.90
        if self.report_one == self.report_two:
            if self.report_one == 1:
                self.payoff_part2_one = cu(0.30)
                self.payoff_part2_two = cu(0.30)
            elif self.report_one == 2:
                self.payoff_part2_one = cu(0.60)
                self.payoff_part2_two = cu(0.60)
            elif self.report_one == 3:
                self.payoff_part2_one = cu(0.90)
                self.payoff_part2_two = cu(0.90)
            elif self.report_one == 4:
                self.payoff_part2_one = cu(1.20)
                self.payoff_part2_two = cu(1.20)
            elif self.report_one == 5:
                self.payoff_part2_one = cu(1.50)
                self.payoff_part2_two = cu(1.50)
            elif self.report_one == 6:
                self.payoff_part2_one = cu(1.80)
                self.payoff_part2_two = cu(1.80)
            else:
                self.payoff_part2_one = cu(0)
                self.payoff_part2_two = cu(0)
        else:
            self.payoff_part2_one = cu(0)
            self.payoff_part2_two = cu(0)

        # Set payoffs on player level (will be registered as Pay)
        for p in self.get_players():
            if p.id_in_group == 1:
                p.payoff = self.payoff_part1_one + self.payoff_part2_one
            elif p.id_in_group == 2:
                p.payoff = self.payoff_part1_two + self.payoff_part2_two

class Player(BasePlayer):
    #Dropout indicator
    drop_out = models.BooleanField(initial=False)
    drop_out_mate = models.BooleanField(initial=False)
    no_partner = models.BooleanField(initial=False)

    #Control questions
    Instr1 = models.IntegerField(blank=False, choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect)
    Instr2 = models.IntegerField(blank=False, choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect)
    Instr3 = models.IntegerField(blank=False, choices=[[1, 'True'], [2, 'False']], widget=widgets.RadioSelect)

    Instr1_wrong = models.IntegerField(max=1, blank=True)
    Instr2_wrong = models.IntegerField(max=1, blank=True)
    Instr3_wrong = models.IntegerField(max=1, blank=True)

    def waiting_too_long(self):
        # import time
        # assumes you set wait_page_arrival in PARTICIPANT_FIELDS.
        return (time.time() - self.participant.wait_page_arrival) > 5*60

    #PEQ
    corona = models.IntegerField(
        label="I am worried about the Corona virus (COVID2019).",
        blank=False,
        choices=Constants.AgreeChoices
    )

    incentives_check = models.IntegerField(
        label="The other participant and I received the same earnings in part 1.",
        blank=False,
        choices=Constants.AgreeChoices
    )

    rpi_check = models.IntegerField(
        label="I knew both my individual rank and the other participant’s individual rank in part 1 before we continued to part 2.",
        blank=False,
        choices=Constants.AgreeChoices
    )

    attention_check = models.IntegerField(
        label="If you’re still paying attention, please select “Disagree.”",
        blank=False,
        choices=Constants.AgreeChoices
    )

    gender = models.IntegerField(
        label="Please select your gender.",
        blank=False,
        choices=[
            [1, 'Male'],
            [2, 'Female'],
            [3, 'Other']
        ]
    )

    age = models.IntegerField(label="Please enter your age.", min=18, max=90, blank=False)

    english = models.IntegerField(
        label="Please rate your English on a percentage scale between 0 and 100.",
        min=0,
        step=1,
        max=100,
        blank=False,
        initial=None
    )

    risk = models.IntegerField(
        label="Please rate your willingness to take risks in general on a scale from 0 (not at all willing) to 10 (very willing)",
        min=0,
        step=1,
        max=10,
        blank=False,
        initial=None
    )

    trustworthy = models.IntegerField(
        label="If someone does me a favor, I am ready to return it. Please rate on a scale from 0 (does not apply to me at all) to 10 (applies to me completely)",
        min=0,
        step=1,
        max=10,
        blank=False,
        initial=None
    )

    trusting = models.IntegerField(
        label="Generally speaking, would you say that most people can be trusted or that you can’t be too careful in dealing with people?",
        blank=False,
        choices=[
            [1, 'Most people can be trusted'],
            [0, 'One can`t be too careful']
        ]
    )

    #Competitiveness
    competitive_one = models.IntegerField(
        label="It was important to me to score higher than the other participant in part 1.",
        blank=False,
        choices=Constants.AgreeChoices
    )

    competitive_two = models.IntegerField(
        label="I worked hard to score higher than the other participant in part 1.",
        blank=False,
        choices=Constants.AgreeChoices
    )

    competitive_three = models.IntegerField(
        label="I cared about scoring more than the other participant in part 1.",
        blank=False,
        choices=Constants.AgreeChoices
    )

    #SSS
    self_social_status = models.IntegerField(
        label="My position on the ladder:",
        blank=False,
        min=1,
        max=10
    )
    other_social_status = models.IntegerField(
        label="The other participant's position on the ladder:",
        blank=False,
        min=1,
        max=10
    )