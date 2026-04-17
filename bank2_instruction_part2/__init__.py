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
    comprehension_q1 = models.StringField(
        choices=[['same', 'The same participant throughout all games'],
                 ['new', 'A participant who may be different each game']],
        label='In each game, you are likely to be paired with:',
        widget=widgets.RadioSelect)
    comprehension_q2 = models.StringField(
        choices=[['same', 'The same across all 10 games today'],
                 ['different', 'Different for each game today']],
        label='The bank selected from the previous experiment (Pre-Bank) will be:',
        widget=widgets.RadioSelect)
    comprehension_q3 = models.StringField(
        choices=[['both', "Both the Pre-Bank's state and your bank's state"],
                 ['only-prebank', "Only the Pre-Bank's state"],
                 ['only-yours', "Only your bank's state"],
                 ['neither', "Neither the Pre-Bank's state nor your bank's state"]],
        label="In today's experiment, when making decisions you will know:",
        widget=widgets.RadioSelect)
    comprehension_q4_low  = models.IntegerField(label='Low (%)', min=0, max=100)
    comprehension_q4_med  = models.IntegerField(label='Medium (%)', min=0, max=100)
    comprehension_q4_high = models.IntegerField(label='High (%)', min=0, max=100)
    comprehension_q5_low  = models.IntegerField(label='Low (%)', min=0, max=100)
    comprehension_q5_med  = models.IntegerField(label='Medium (%)', min=0, max=100)
    comprehension_q5_high = models.IntegerField(label='High (%)', min=0, max=100)
    comprehension_q6_low  = models.IntegerField(label='Low (%)', min=0, max=100)
    comprehension_q6_med  = models.IntegerField(label='Medium (%)', min=0, max=100)
    comprehension_q6_high = models.IntegerField(label='High (%)', min=0, max=100)
    comprehension_q7 = models.StringField(
        choices=[['stage1-only', 'Action A in only Stage 1'],
                 ['stage2-only', 'Action A in only Stage 2 (BA)'],
                 ['either', 'Action A in either Stage 1 or Stage 2 (A or BA)']],
        label='In Stage 1, you will be informed of the number of Pre-Bank depositors who chose:',
        widget=widgets.RadioSelect)
    comprehension_q8 = models.StringField(
        choices=[['a-stage1', 'Only if you choose action A in Stage 1'],
                 ['b-stage1', 'Only if you choose action B in Stage 1 and move to Stage 2'],
                 ['both-a', 'Only if both you and the other depositor choose action A in Stage 1'],
                 ['both-b', 'Only if both you and the other depositor choose action B in Stage 1 and move to Stage 2']],
        label='You receive a message from the Observer:',
        widget=widgets.RadioSelect)
    comprehension_q9 = models.StringField(
        choices=[['true', 'True'], ['false', 'False']],
        label="At the end of today's experiment, one of the 10 games will be randomly selected for payment, and your points will be converted to cash at 1 point = $0.50.",
        widget=widgets.RadioSelect)


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

class Intro2b(Page):
    pass

class Intro2c_mockupB(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            unmatched_corr=(100 - C.STATE_CORR) // 2,
            delayed_a=C.ENDOWMENT - C.DELAY_COST,
        )

class Intro3(Page):
    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            unmatched_corr=(100 - C.STATE_CORR) // 2,
        )


# --- Comprehension check pages (one question or group per page) ---

class CQ1(Page):
    form_model = 'player'
    form_fields = ['comprehension_q1']

class CQ2(Page):
    form_model = 'player'
    form_fields = ['comprehension_q2']

class CQ3(Page):
    form_model = 'player'
    form_fields = ['comprehension_q3']

class CQ4(Page):
    form_model = 'player'
    form_fields = ['comprehension_q4_low', 'comprehension_q4_med', 'comprehension_q4_high']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(unmatched_corr=(100 - C.STATE_CORR) // 2)

class CQ5(Page):
    form_model = 'player'
    form_fields = ['comprehension_q5_low', 'comprehension_q5_med', 'comprehension_q5_high']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(unmatched_corr=(100 - C.STATE_CORR) // 2)

class CQ6(Page):
    form_model = 'player'
    form_fields = ['comprehension_q6_low', 'comprehension_q6_med', 'comprehension_q6_high']

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(unmatched_corr=(100 - C.STATE_CORR) // 2)

class CQ7(Page):
    form_model = 'player'
    form_fields = ['comprehension_q7']

class CQ8(Page):
    form_model = 'player'
    form_fields = ['comprehension_q8']

class CQ9(Page):
    form_model = 'player'
    form_fields = ['comprehension_q9']


page_sequence = [Intro1, Intro2, Intro2b, Intro2c_mockupB, Intro3, CQ1, CQ2, CQ3, CQ4, CQ5, CQ6, CQ7, CQ8, CQ9]
