from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
    form_model = 'player'
    form_fields = [
        'mturk_feedback'
    ]

    def vars_for_template(self):
        return {
            #.to_real_world_currency(self.session)
            'payoff': self.participant.payoff,
            'participation_fee': self.session.config['participation_fee'],
            'total_eur': self.participant.payoff_plus_participation_fee(),
            'is_dropout': self.participant.is_dropout,
            'is_dropout_mate': self.participant.is_dropout_mate,
            # 'is_dofus': self.participant.is_dofus,
            'no_partner': self.participant.no_partner
            # 'completion_code': self.session.config['completion_code']
        }

page_sequence = [PaymentInfo]
