from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'bank2_instruction_part1'
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

class Intro0(Page):
    pass

class Intro1(Page):
    pass

class Intro2(Page):
    pass

class Intro3Low_1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST)

class Intro3Low_2(Page):
    allow_back_button = True

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST)
    
class Intro3Med(Page):
    allow_back_button = True

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST)

    
class Intro3High(Page):
    allow_back_button = True
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST)

class Intro4(Page):
    pass

class Intro5(Page):
    pass

class Intro6(Page):
    pass

class WaitForAll(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants.'

# --- Comprehension check pages (one question or group per page) ---




page_sequence = [Welcome, Intro0, Intro1, Intro2, 
                 Intro3Low_1, Intro3Low_2, Intro3Med, Intro3High, 
                 Intro4, Intro5, Intro6, WaitForAll]

