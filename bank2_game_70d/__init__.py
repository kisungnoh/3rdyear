from otree.api import *
import numpy as np
import random

doc = ''
class C(BaseConstants):
    # built-in constants
    NAME_IN_URL = 'bank2_game_70d'
    PLAYERS_PER_GROUP = 2
    PART2_ROUNDS = 2
    NUM_ROUNDS = 5
    # user-defined constants
    ENDOWMENT = 10
    DELAY_COST = 1
    SUCCESS_PAYOFF = 18
    FAIL_PAYOFF = 0
    LOW_PROB = 15
    MEDIUM_PROB = 70
    HIGH_PROB = 15
    STATE_CORR = 70
    RAND_MAX = 100
    BELIEF_REWARD = 4  # payment for correct belief report
    REAL_WORLD_CURRENCY_PER_POINT = 0.5

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    prebank_state = models.StringField()
    prebank_a_count = models.IntegerField(blank=True)
    your_state = models.StringField()
    
class Player(BasePlayer):
    first_decision = models.StringField(
        choices=[['action_a', 'Action A'], ['action_b', 'Action B']],
        label='',
        widget=widgets.RadioSelect)
    second_decision = models.StringField(
        blank=True,
        choices=[['action_a', 'Action A'], ['action_b', 'Action B']],
        label='',
        widget=widgets.RadioSelect)

    # Action path
    path = models.StringField(blank=True)
    other_path = models.StringField(blank=True)

    # Stage 1 belief - other's action
    belief_s1 = models.IntegerField(
        blank=True,
        label='How likely do you think the other depositor chose action A in Stage 1? (%)')
    belief_draw1_s1 = models.IntegerField(blank=True)
    belief_draw2_s1 = models.IntegerField(blank=True)
    belief_rewarded_s1 = models.BooleanField(blank=True)

    # Stage 1 belief - state
    belief_low = models.IntegerField(blank=True, label='Probability the state is Low (%)')
    belief_med = models.IntegerField(blank=True, label='Probability the state is Medium (%)')
    belief_high = models.IntegerField(blank=True, label='Probability the state is High (%)')
    belief_draw1_state = models.IntegerField(blank=True)
    belief_draw2_state = models.IntegerField(blank=True)
    belief_rewarded_state = models.BooleanField(blank=True)

    # Stage 2 belief - other's action (elicited only, not paid)
    belief_s2 = models.IntegerField(
        blank=True,
        label='How likely do you think the other depositor will choose action A in Stage 2? (%)')

    # Observer message
    received_message = models.StringField(blank=True, label='Message from the observer (if any):')

# --- bank1_game data pool ---
# Plug in the collected bank1_game data here before running the actual experiment.
# Each entry is [state, a_count] where state is 'Low'/'Medium'/'High' and
# a_count is the number of A-choosers (early + late) in that match.
# Example: PREBANK_DATA = [['Low', 2], ['Medium', 1], ['High', 0], ...]
# When non-empty, each group's prebank_state and prebank_a_count are drawn by random.choice().
# When empty (default), falls back to probability-based random draw with hardcoded demo A_COUNT
# (Low→2, Medium→1, High→0).
PREBANK_DATA = []

DEMO_A_COUNT = {'Low': 2, 'Medium': 1, 'High': 0}

# --- Helper functions ---

def draw_state(rand):
    if rand <= C.LOW_PROB:
        return 'Low'
    elif rand <= C.LOW_PROB + C.MEDIUM_PROB:
        return 'Medium'
    else:
        return 'High'


def draw_correlated_state(prebank_state):
    rand = random.randint(1, C.RAND_MAX)
    if rand <= C.STATE_CORR:
        return prebank_state
    else:
        other_states = [s for s in ['Low', 'Medium', 'High'] if s != prebank_state]
        return random.choice(other_states)


def get_player_action(player: Player):
    if player.first_decision == 'action_a':
        return 'early'
    elif player.second_decision == 'action_a':
        return 'late'
    else:
        return 'stay'


def get_payoff(action, other_action, state):
    if state == 'Low':
        if action == 'early':
            return C.ENDOWMENT
        elif action == 'late':
            return C.ENDOWMENT - C.DELAY_COST
        else:  # stay
            return C.FAIL_PAYOFF
    elif state == 'Medium':
        if action == 'early':
            return C.ENDOWMENT
        elif action == 'late':
            if other_action == 'stay':
                return C.ENDOWMENT
            else:  # other is early or late
                return C.ENDOWMENT - C.DELAY_COST
        else:  # stay
            if other_action == 'stay':
                return C.SUCCESS_PAYOFF
            else:
                return C.FAIL_PAYOFF
    else:  # High
        if action == 'early':
            return C.ENDOWMENT
        elif action == 'late':
            return C.ENDOWMENT
        else:  # stay
            return C.SUCCESS_PAYOFF


def calculate_payoffs(group: Group):
    state = group.your_state
    for p in group.get_players():
        other = p.get_others_in_group()[0]
        p.payoff = get_payoff(
            get_player_action(p),
            get_player_action(other),
            state
        )


# --- Session creation ---

def creating_session(subsession: Subsession):
    subsession.group_randomly()

    for group in subsession.get_groups():
        if PREBANK_DATA:
            prebank_state, a_count = random.choice(PREBANK_DATA)
        else:
            prebank_state = draw_state(random.randint(1, C.RAND_MAX))
            a_count = DEMO_A_COUNT[prebank_state]
        group.prebank_state = prebank_state
        group.prebank_a_count = a_count
        group.your_state = draw_correlated_state(prebank_state)

    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.b2_p2_round = random.randint(1, C.PART2_ROUNDS)

    if subsession.round_number == C.PART2_ROUNDS + 1:
        for player in subsession.get_players():
            r1, r2, r3 = random.sample(range(C.PART2_ROUNDS + 1, C.NUM_ROUNDS + 1), 3)
            player.participant.b2_p3_round    = r1  # game payoff round
            player.participant.b2_bel_s1_round = r2  # belief_s1 payment round (other's Stage 1 action)
            player.participant.b2_bel_state_round  = r3  # state belief payment round



class Part2Intro(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        
        return player.round_number == 1
        
class FirstStage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        fields = ['first_decision']
        if player.round_number > C.PART2_ROUNDS:
            fields += ['belief_s1', 'belief_low', 'belief_med', 'belief_high']
        return fields

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
            delayed_a=10-C.DELAY_COST,
            unmatched_corr=(100-C.STATE_CORR)//2,
            show_beliefs=player.round_number > C.PART2_ROUNDS,
            prebank_a_count=player.group.prebank_a_count,
        )

    @staticmethod
    def error_message(player: Player, values):
        if player.round_number <= C.PART2_ROUNDS:
            return None
        low  = values.get('belief_low')  or 0
        med  = values.get('belief_med')  or 0
        high = values.get('belief_high') or 0
        if low + med + high != 100:
            return f'Your state beliefs must sum to 100% (currently {low + med + high}%).'

class AfterFirstStage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            other = player.get_others_in_group()[0]
            if player.first_decision == 'action_a':
                player.received_message = ''
            else:
                state = group.your_state
                other_chose_a_s1 = (other.first_decision == 'action_a')
                if state == 'Low':
                    player.received_message = 'Left'
                elif state == 'High':
                    player.received_message = 'Right'
                else:  # Medium
                    player.received_message = 'Left' if other_chose_a_s1 else 'Right'

class SecondStage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        fields = ['second_decision']
        if player.round_number > C.PART2_ROUNDS:
            fields += ['belief_s2']
        return fields

    @staticmethod
    def is_displayed(player: Player):
        return player.first_decision == 'action_b'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
            delayed_a=10-C.DELAY_COST,
            unmatched_corr=(100-C.STATE_CORR)//2,
            show_beliefs=player.round_number > C.PART2_ROUNDS,
            prebank_a_count=player.group.prebank_a_count,
            received_message=player.received_message,
        )
    
class AfterSecondStage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        calculate_payoffs(group)

        for player in group.get_players():
            other = player.get_others_in_group()[0]
            player.path = get_player_action(player)
            player.other_path = get_player_action(other)

            # Part 2 game payoff storage
            if player.round_number == player.participant.b2_p2_round:
                player.participant.b2_p2_payoff = float(player.payoff)
                player.participant.b2_p2_state = player.group.your_state
                player.participant.b2_p2_action = get_player_action(player)
                player.participant.b2_p2_other_action = get_player_action(other)

            if player.round_number > C.PART2_ROUNDS:

                # Part 3 game payoff storage
                if player.round_number == player.participant.b2_p3_round:
                    player.participant.b2_p3_payoff = float(player.payoff)
                    player.participant.b2_p3_state = player.group.your_state
                    player.participant.b2_p3_action = get_player_action(player)
                    player.participant.b2_p3_other_action = get_player_action(other)

                # Other's action belief payment (Stage 1, BQSR)
                if player.round_number == player.participant.b2_bel_s1_round:
                    other_chose_a_s1 = (other.first_decision == 'action_a')
                    player.participant.b2_bel_s1 = player.belief_s1                    
                    player.participant.b2_bel_s1_other_action = 'action_a' if other_chose_a_s1 else 'action_b'

                    r1_s1 = random.randint(0, 100)
                    r2_s1 = random.randint(0, 100)
                    player.belief_draw1_s1 = r1_s1
                    player.belief_draw2_s1 = r2_s1
                    player.participant.b2_bel_s1_draw1 = r1_s1
                    player.participant.b2_bel_s1_draw2 = r2_s1

                    if other_chose_a_s1:
                        player.belief_rewarded_s1 = (player.belief_s1 > r1_s1) or (player.belief_s1 > r2_s1)
                    else:
                        player.belief_rewarded_s1 = ((100 - player.belief_s1) > r1_s1) or ((100 - player.belief_s1) > r2_s1)
                    
                    player.participant.b2_bel_s1_payoff = (
                        C.BELIEF_REWARD if player.belief_rewarded_s1 else 0
                    )

                # State belief payment (Stage 1, BQSR)
                if player.round_number == player.participant.b2_bel_state_round:
                    actual_state = player.group.your_state
                    player.participant.b2_bel_act_state = actual_state

                    picked_state = random.choice(['Low', 'Medium', 'High'])
                    player.participant.b2_bel_picked_state = picked_state

                    if picked_state == 'Low':
                        reported_p = player.belief_low
                    elif picked_state == 'Medium':
                        reported_p = player.belief_med
                    else:
                        reported_p = player.belief_high
                    player.participant.b2_bel_state_reported = reported_p

                    r1_state = random.randint(0, 100)
                    r2_state = random.randint(0, 100)
                    player.belief_draw1_state = r1_state
                    player.belief_draw2_state = r2_state
                    player.participant.b2_bel_state_draw1 = r1_state
                    player.participant.b2_bel_state_draw2 = r2_state

                    if actual_state == picked_state:
                        player.belief_rewarded_state = (reported_p > r1_state) or (reported_p > r2_state)
                    else:
                        player.belief_rewarded_state = ((100 - reported_p) > r1_state) or ((100 - reported_p) > r2_state)
                    player.participant.b2_bel_state_payoff = (
                        C.BELIEF_REWARD if player.belief_rewarded_state else 0
                    )

class Results(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        
        other = player.get_others_in_group()[0]
        return dict(
            round_number=player.round_number,
            other=other,
            delayed_a=10-C.DELAY_COST,
            your_state=player.group.your_state,
            prebank_state=player.group.prebank_state,
            payoff_value=int(player.payoff)
        )

class Part2Outro(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == C.PART2_ROUNDS


class AfterPart2(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants to finish Part 2.'

    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == C.PART2_ROUNDS


class Part3Intro(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.PART2_ROUNDS

    @staticmethod
    def vars_for_template(_player: Player):
        return dict(
            part3_rounds=C.NUM_ROUNDS-C.PART2_ROUNDS,
        )

class Part3Outro(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class AfterPart3(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants to finish Part 3.'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class FinalResults(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        p2_round = player.participant.b2_p2_round
        p3_round = player.participant.b2_p3_round
        return dict(
            b2_p2_round=p2_round,
            b2_p2_payoff=player.participant.b2_p2_payoff,
            b2_p2_state=player.participant.b2_p2_state,
            b2_p3_round=p3_round,
            b2_p3_payoff=player.participant.b2_p3_payoff,
            b2_p3_state=player.participant.b2_p3_state,
        )

page_sequence = [Part2Intro, FirstStage, AfterFirstStage, SecondStage, AfterSecondStage, 
                 Results, Part2Outro, AfterPart2, Part3Intro, Part3Outro, AfterPart3]