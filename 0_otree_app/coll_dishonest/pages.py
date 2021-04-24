from otree.api import Currency as cu, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class WaitForMatch(WaitPage):
    group_by_arrival_time = True
    title_text = "Please wait"
    body_text = "Please wait for the other participant."

    def app_after_this_page(self, upcoming_apps):
        if len(self.group.get_players()) == 1:
            self.group.no_partner_trigger()
            return upcoming_apps[-1]
        if len(self.group.get_players()) == 2:
            self.group.assign_stuff()

class BeforeResults(Page):
    def is_displayed(self):
        return self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def get_timeout_seconds(self):
        return 120

    def vars_for_template(self):
        return {
            'payoff_part1_one': self.group.payoff_part1_one,
            'payoff_part1_two': self.group.payoff_part1_two,
        }

    def before_next_page(self):
        if self.timeout_happened:
            if self.player.id_in_group == 1:
                self.group.drop_out_trigger_one()
            elif self.player.id_in_group == 2:
                self.group.drop_out_trigger_two()

class Instruct_one(Page):
    form_model = 'player'
    form_fields = ['Instr1', 'Instr1_wrong']

    def is_displayed(self):
        return self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def get_timeout_seconds(self):
        return 120

    def before_next_page(self):
        if self.timeout_happened:
            if self.player.id_in_group == 1:
                self.group.drop_out_trigger_one()
            elif self.player.id_in_group == 2:
                self.group.drop_out_trigger_two()

class Instruct_two(Page):
    form_model = 'player'
    form_fields = ['Instr2', 'Instr2_wrong']

    def is_displayed(self):
        return self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def get_timeout_seconds(self):
        return 120

    def before_next_page(self):
        if self.timeout_happened:
            if self.player.id_in_group == 1:
                self.group.drop_out_trigger_one()
            elif self.player.id_in_group == 2:
                self.group.drop_out_trigger_two()

class Instruct_three(Page):
    form_model = 'player'
    form_fields = ['Instr3', 'Instr3_wrong']

    def is_displayed(self):
        return self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def get_timeout_seconds(self):
        return 120

    def before_next_page(self):
        if self.timeout_happened:
            if self.player.id_in_group == 1:
                self.group.drop_out_trigger_one()
            elif self.player.id_in_group == 2:
                self.group.drop_out_trigger_two()

class Start_study(Page):
    def is_displayed(self):
        return self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def get_timeout_seconds(self):
        return 120

    def before_next_page(self):
        if self.timeout_happened:
            if self.player.id_in_group == 1:
                self.group.drop_out_trigger_one()
            elif self.player.id_in_group == 2:
                self.group.drop_out_trigger_two()

class Report_one(Page):
    form_model = 'group'
    form_fields = ['report_one', 'check_report_one']

    def is_displayed(self):
        return self.player.id_in_group == 1 and self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def get_timeout_seconds(self):
        return 120

    def error_message(self, value):
        if value["check_report_one"] == None:
            return 'Please report about the outcome of your die in the box.'

    def before_next_page(self):
        if self.timeout_happened:
            self.group.drop_out_trigger_one()

class WaitForP1(WaitPage):
    title_text = "Please wait"
    body_text = "Please wait for the other participant to roll their die and report."
    def is_displayed(self):
        return self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

class Report_two(Page):
    form_model = 'group'
    form_fields = ['report_two', 'check_report_two']

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def get_timeout_seconds(self):
        return 120

    def error_message(self, value):
        if value["check_report_two"] == None:
            return 'Please report about the outcome of your die in the box.'

    def before_next_page(self):
        if self.timeout_happened:
            self.group.drop_out_trigger_two()

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_report_payoffs'
    title_text = "Please wait"
    body_text = "Please wait for the other participant to roll their die and report."

    def is_displayed(self):
        return self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

class AfterResults(Page):
    def is_displayed(self):
        return self.group.rpi == 1 and self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def vars_for_template(self):
        return {
            'participation_fee': cu(0.50),
            'payoff_part2_one': self.group.payoff_part2_one,
            'payoff_part2_two': self.group.payoff_part2_two
        }

class Results(Page):
    def is_displayed(self):
        return self.group.rpi == 0 and self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def vars_for_template(self):
        return {
            'payoff_part1_one': self.group.payoff_part1_one,
            'payoff_part1_two': self.group.payoff_part1_two,
            'payoff_part2_one': self.group.payoff_part2_one,
            'payoff_part2_two': self.group.payoff_part2_two,
            'participation_fee': cu(0.50),
        }

class PEQ_one(Page):
    form_model = 'player'
    form_fields = [
        'incentives_check',
        'rpi_check',
        'gender',
        'age',
        'english',
        'trusting',
        'trustworthy',
        'risk',
        'corona',
        'attention_check'
    ]

    def is_displayed(self):
        return self.player.participant.is_dropout == False and self.player.participant.is_dropout_mate == False

    def get_form_fields(self):
        fields = self.form_fields
        random.shuffle(fields)
        return fields

page_sequence = [
    WaitForMatch,
    BeforeResults,
    Instruct_one,
    Instruct_two,
    Instruct_three,
    Start_study,
    Report_one,
    WaitForP1,
    Report_two,
    ResultsWaitPage,
    AfterResults,
    Results,
    PEQ_one
]
