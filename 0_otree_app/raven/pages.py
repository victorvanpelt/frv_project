from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
import time

class Instruct_one(Page):
    form_model = 'player'
    form_fields = ['Instr1', 'Instr1_wrong']

    def is_displayed(self):
        return self.round_number == 1

    # def error_message(self, values):
    #     if values["Instr1"] != 1:
    #         return 'Your answer is incorrect. Please read the instructions carefully and provide the correct answer.'

class Instruct_two(Page):
    form_model = 'player'
    form_fields = ['Instr2', 'Instr2_wrong']

    def is_displayed(self):
        return self.round_number == 1

    # def error_message(self, values):
    #     if values["Instr2"] != 5:
    #         return 'Your answer is incorrect. Please read the instructions carefully and provide the correct answer.'

class Start_study(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # user has 5 minutes to complete as many pages as possible
        self.player.participant.expiry = time.time() + 5*60

class Task(Page):
    form_model = 'player'
    form_fields = ['task', 'check_task']

    timer_text = 'Total time left:'

    def is_displayed(self):
        return self.round_number < Constants.num_rounds and self.player.participant.no_time_left == False

    def get_timeout_seconds(self):
        participant = self.player.participant
        return participant.expiry - time.time()

    def error_message(self, value):
        if value["check_task"] == None:
            return 'Please provide an answer in the box.'

    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.no_time_left = True
            self.player.set_score()
            self.player.participant.wait_page_arrival = time.time()

class Task_last(Page):
    form_model = 'player'
    form_fields = ['task', 'check_task']

    timer_text = 'Total time left:'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.player.participant.no_time_left == False

    def get_timeout_seconds(self):
        participant = self.player.participant
        return participant.expiry - time.time()

    def error_message(self, value):
        if value["check_task"] == None:
            return 'Please provide an answer in the box.'

    def before_next_page(self):
        self.player.set_score()
        self.player.participant.wait_page_arrival = time.time()
        if self.timeout_happened:
            self.player.participant.no_time_left = True

page_sequence = [
    Instruct_one,
    Instruct_two,
    Start_study,
    Task,
    Task_last,
]
