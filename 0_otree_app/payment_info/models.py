from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


class Constants(BaseConstants):
    name_in_url = 'payment_info_rt'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
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

    mturk_feedback = models.TextField(
        label="Do you have any feedback for us or anything you would like to say to us?",
        blank=True
    )
