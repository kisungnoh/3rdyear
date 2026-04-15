
from otree.api import *
import numpy as np
import random

doc = ''
class C(BaseConstants):
    # built-in constants
    NAME_IN_URL = 'bank_run'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    # user-defined constants
    ENDOWMENT = 10
    DELAY_COST = 2
    SUCCESS_PAYOFF = 20
    FAIL_PAYOFF = 0
    BAD_PROB = 30
    MEDIUM_PROB = 50
    GOOD_PROB = 20
    RAND_MAX = 100

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    bank_fundamental = models.StringField()

class Player(BasePlayer):
    first_decision = models.StringField(choices=['withdraw', 'stay'], label='Please make your choice:', widget=widgets.RadioSelect)
    second_decision = models.StringField(blank=True, choices=['withdraw', 'stay'], label='Please make your choice:', widget=widgets.RadioSelect)
    final_payoff = models.IntegerField()

def creating_session(subsession: Subsession):

    subsession.group_randomly()
    
    #if subsession.round_number == 1:
    #    for p in subsession.get_players():
        
    for group in subsession.get_groups():
        rand = random.randint(1, C.RAND_MAX)
        if rand <= C.BAD_PROB:
            group.bank_fundamental = 'Bad'
        elif rand <= C.BAD_PROB + C.MEDIUM_PROB:
            group.bank_fundamental = 'Medium'
        else:
            group.bank_fundamental = 'Good'
            
    if subsession.round_number == 1:
        for player in subsession.get_players():
            participant = player.participant
            participant.selected_round = random.randint(1, C.NUM_ROUNDS)


def calculate_payoffs(group: Group):
    players = group.get_players()
    fundamental = group.bank_fundamental
    
    for p in players:
        other = p.get_others_in_group()[0]
        p_action = get_player_action(p)
        other_action = get_player_action(other)
        p.payoff = get_payoff(p_action, other_action, fundamental)
    
def get_player_action(player: Player):
    if player.first_decision == 'withdraw':
        return 'early'
    elif player.second_decision == 'withdraw':
        return 'late'
    else:
        return 'stay'
    
def get_payoff(action, other_action, fundamental):
    if fundamental == 'Bad':
        if action == 'early':
            return C.ENDOWMENT
        elif action == 'late':
            return C.ENDOWMENT - C.DELAY_COST
        else:  # action == 'stay'
            return C.FAIL_PAYOFF
    elif fundamental == 'Medium':
        if action == 'early':
            return C.ENDOWMENT
        elif action == 'late':
            if other_action == 'stay':
                return C.ENDOWMENT
            else: # other_action == 'early' or 'late'
                return C.ENDOWMENT - C.DELAY_COST
        else:  # action == 'stay'
            if other_action == 'stay':
                return C.SUCCESS_PAYOFF
            else:
                return C.FAIL_PAYOFF
    else:  # fundamental == 'Good'
        if action == 'early':
            return C.ENDOWMENT
        elif action == 'late':
            return C.ENDOWMENT
        else:  # action == 'stay'
            return C.SUCCESS_PAYOFF
    

class Instructions(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        
        return player.round_number == 1
        
class FirstStage(Page):
    form_model = 'player'
    form_fields = ['first_decision']
    @staticmethod
    def vars_for_template(player: Player):
        
        return dict(round_number=player.round_number,
                    delayed_withdraw=10-C.DELAY_COST)


class AfterFirstStage(WaitPage):
    pass

class SecondStage(Page):
    form_model = 'player'
    form_fields = ['second_decision']

    @staticmethod
    def is_displayed(player: Player):
        return player.first_decision == 'stay'
    
    @staticmethod
    def vars_for_template(player: Player):
        other = player.get_others_in_group()[0]
        other_withdrew = other.first_decision == 'withdraw'
        return dict(other_withdrew=other_withdrew,
                    delayed_withdraw=10-C.DELAY_COST)
    
class AfterSecondStage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        calculate_payoffs(group)

class Results(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        
        other = player.get_others_in_group()[0]
        bank_fundamental = player.group.bank_fundamental
        return dict(
            other=other,
            bank_fundamental=bank_fundamental,
            delayed_withdraw=10-C.DELAY_COST,
            payoff_value=int(player.payoff)
        )
        
class FinalResults(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        
        return player.round_number == C.NUM_ROUNDS
        
    @staticmethod
    def vars_for_template(player: Player):
        
        selected_round = player.participant.selected_round
        selected_player = player.in_round(selected_round)
        return dict(
            selected_round=selected_round,
            selected_payoff=selected_player.payoff
        )
        
page_sequence = [Instructions, FirstStage, AfterFirstStage, SecondStage, AfterSecondStage, Results, FinalResults]