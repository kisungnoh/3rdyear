from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'bank1_instruction'
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
    RAND_MAX = 100
    REAL_WORLD_CURRENCY_PER_POINT = 0.5

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    your_state = models.StringField()

class Player(BasePlayer):
    # Comprehension check fields
    comprehension_q1 = models.StringField(
        choices=[['same', 'The same participant'], ['new', 'A new participant']],
        label='', widget=widgets.RadioSelect)
    comprehension_q2 = models.StringField(
        choices=[['fixed', 'Always 10, regardless of bank state or the other\'s choice'],
                 ['depends', 'It depends on the bank state or the other\'s choice']],
        label='', widget=widgets.RadioSelect)
    comprehension_q3 = models.StringField(
        choices=[['after', 'After learning the other depositor\'s Stage 1 choice'],
                 ['without', 'Without knowing the other depositor\'s Stage 1 choice']],
        label='', widget=widgets.RadioSelect)
    comprehension_q4_a  = models.IntegerField(label='')
    comprehension_q4_ba = models.IntegerField(label='')
    comprehension_q4_bb = models.IntegerField(label='')
    comprehension_q5_a  = models.IntegerField(label='')
    comprehension_q5_ba = models.IntegerField(label='')
    comprehension_q5_bb = models.IntegerField(label='')
    comprehension_q6_a  = models.IntegerField(label='')
    comprehension_q6_ba = models.IntegerField(label='')
    comprehension_q6_bb = models.IntegerField(label='')
    comprehension_q7_a  = models.IntegerField(label='')
    comprehension_q7_ba = models.IntegerField(label='')
    comprehension_q7_bb = models.IntegerField(label='')
    comprehension_q8 = models.StringField(
        choices=[['true', 'True'], ['false', 'False']],
        label='', widget=widgets.RadioSelect)


# --- Helper functions ---

def draw_state(rand):
    if rand <= C.LOW_PROB:
        return 'Low'
    elif rand <= C.LOW_PROB + C.MEDIUM_PROB:
        return 'Medium'
    else:
        return 'High'


# --- Session creation ---

def creating_session(subsession: Subsession):
    subsession.group_randomly()

    for group in subsession.get_groups():
        group.your_state = draw_state(random.randint(1, C.RAND_MAX))




class Welcome(Page):
    pass

class Intro1(Page):
    pass

class Intro2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            state=player.group.your_state,
            delayed_a=C.ENDOWMENT - C.DELAY_COST,
        )

class Intro3(Page):
    pass

class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = [
        'comprehension_q1', 'comprehension_q2', 'comprehension_q3',
        'comprehension_q4_a', 'comprehension_q4_ba', 'comprehension_q4_bb',
        'comprehension_q5_a', 'comprehension_q5_ba', 'comprehension_q5_bb',
        'comprehension_q6_a', 'comprehension_q6_ba', 'comprehension_q6_bb',
        'comprehension_q7_a', 'comprehension_q7_ba', 'comprehension_q7_bb',
        'comprehension_q8',
    ]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(delayed_a=C.ENDOWMENT - C.DELAY_COST)



class WaitForAll(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants to finish the comprehension check.'

page_sequence = [Welcome, Intro1, Intro2, Intro3, ComprehensionCheck, WaitForAll]
