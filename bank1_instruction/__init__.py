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
        choices=[['same', 'The same participant'],
                 ['new', 'A new participant']],
        label='In each game, you are likely to be paired with:',
        widget=widgets.RadioSelect)
    comprehension_q2 = models.StringField(
        choices=[['fixed', 'You receive 10, regardless of the state of the bank or the other\'s choice.'],
                 ['depends', 'It depends on the state of the bank or the other\'s choice.']],
        label='If you choose to withdraw in Period 1,',
        widget=widgets.RadioSelect)
    comprehension_q3a = models.IntegerField(
        label='You choose to stay in Period 1 and to withdraw in Period 2:', 
        min=0, max=100)
    comprehension_q3b = models.IntegerField(
        label='You choose to stay in Period 1 and to stay in Period 2:', 
        min=0, max=100)
    comprehension_q4a = models.IntegerField(
        label='You choose to stay in Period 1 and to withdraw in Period 2:', 
        min=0, max=100)
    comprehension_q4b = models.IntegerField(
        label='You choose to stay in both Period 1 and Period 2:', 
        min=0, max=100)
    comprehension_q5a = models.IntegerField(
        label='The other chooses to withdraw in Period 1:', 
        min=0, max=100)
    comprehension_q5b = models.IntegerField(
        label='The other chooses to stay in both Period 1 and Period 2:',
        min=0, max=100)
    comprehension_q5c = models.IntegerField(
        label='The other chooses to stay in both Period 1 and Period 2:',
        min=0, max=100)
    comprehension_q6a = models.IntegerField(
        label='The other chooses to withdraw in Period 1:', 
        min=0, max=100)
    comprehension_q6b = models.IntegerField(
        label='The other chooses to stay in Period 1 and to withdraw in Period 2:',
        min=0, max=100)
    comprehension_q6c = models.IntegerField(
        label='The other chooses to stay in both Period 1 and Period 2:',
        min=0, max=100)
    comprehension_q7 = models.StringField(
        choices=[['true', 'True'], ['false', 'False']],
        label='At the end of the experiment, one game will be randomly selected for payment at the rate of 1 point = 0.5 dollar.',
        widget=widgets.RadioSelect)
    


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
    pass

class Intro3Low(Page):
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

class CQ1(Page):
    form_model = 'player'
    form_fields = ['comprehension_q1']

class CQ2(Page):
    form_model = 'player'
    form_fields = ['comprehension_q2']

class CQ3(Page):
    form_model = 'player'
    form_fields = ['comprehension_q3a', 'comprehension_q3b']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST)
    
class CQ4(Page):
    form_model = 'player'
    form_fields = ['comprehension_q4a', 'comprehension_q4b']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST)
    
class CQ5(Page):
    form_model = 'player'
    form_fields = ['comprehension_q5a', 'comprehension_q5b', 'comprehension_q5c']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST)
    
class CQ6(Page):
    form_model = 'player'
    form_fields = ['comprehension_q6a', 'comprehension_q6b', 'comprehension_q6c']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(sw_payoff=C.ENDOWMENT - C.DELAY_COST)
    
class CQ7(Page):
    form_model = 'player'
    form_fields = ['comprehension_q7']



class WaitForAll2(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants to finish the comprehension check.'

page_sequence = [Welcome, Intro1, Intro2, Intro3Low, Intro3Med, Intro3High, Intro4, Intro5, Intro6, WaitForAll, 
                 CQ1, CQ2, CQ3, CQ4, CQ5, CQ6, CQ7, WaitForAll2]


