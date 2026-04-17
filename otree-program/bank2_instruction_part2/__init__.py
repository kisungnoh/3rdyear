from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'bank2_instruction_part2'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    # user-defined constants
    ENDOWMENT = 10
    DELAY_COST = 1
    SUCCESS_PAYOFF = 18
    FAIL_PAYOFF = 0
    LOW_PROB = 15
    MEDIUM_PROB = 70
    HIGH_PROB = 15
    STATE_CORR = 70
    REAL_WORLD_CURRENCY_PER_POINT = 0.5


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    comprehension_q1 = models.StringField(blank=True)
    comprehension_q2 = models.StringField(blank=True)
    comprehension_q3 = models.StringField(blank=True)
    comprehension_q4_low  = models.StringField(blank=True)
    comprehension_q4_med  = models.StringField(blank=True)
    comprehension_q4_high = models.StringField(blank=True)
    comprehension_q5_low  = models.StringField(blank=True)
    comprehension_q5_med  = models.StringField(blank=True)
    comprehension_q5_high = models.StringField(blank=True)
    comprehension_q6_low  = models.StringField(blank=True)
    comprehension_q6_med  = models.StringField(blank=True)
    comprehension_q6_high = models.StringField(blank=True)
    comprehension_q7 = models.StringField(blank=True)
    comprehension_q8 = models.StringField(blank=True)
    comprehension_q9 = models.StringField(blank=True)


class Intro1(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            unmatched_corr=(100 - C.STATE_CORR) // 2,
            delayed_a=C.ENDOWMENT - C.DELAY_COST,
        )

class Intro2(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            unmatched_corr=(100 - C.STATE_CORR) // 2,
            delayed_a=C.ENDOWMENT - C.DELAY_COST,
        )
    
class Intro3(Page):
    pass

class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = [
        'comprehension_q1', 'comprehension_q2', 'comprehension_q3',
        'comprehension_q4_low', 'comprehension_q4_med', 'comprehension_q4_high',
        'comprehension_q5_low', 'comprehension_q5_med', 'comprehension_q5_high',
        'comprehension_q6_low', 'comprehension_q6_med', 'comprehension_q6_high',
        'comprehension_q7', 'comprehension_q8', 'comprehension_q9',
    ]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            delayed_a=C.ENDOWMENT - C.DELAY_COST,
            unmatched_corr=(100 - C.STATE_CORR) // 2,
        )

page_sequence = [Intro1, Intro2, Intro3, ComprehensionCheck]
