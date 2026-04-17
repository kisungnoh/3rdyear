from tokenize import group

from otree.api import *
import numpy as np
import random

class C(BaseConstants):
    # built-in constants
    NAME_IN_URL = 'bank1_game'
    PLAYERS_PER_GROUP = 2
    PART1_ROUNDS = 1
    NUM_ROUNDS = 3
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

    # Belief fields - other's choice
    belief_s1 = models.IntegerField(
        blank=True,
        label='How likely do you think the other depositor chose action A in Stage 1? (%)')
    belief_draw1_s1 = models.IntegerField(blank=True)
    belief_draw2_s1 = models.IntegerField(blank=True)
    belief_rewarded_s1 = models.BooleanField(blank=True)


# --- Helper functions ---

def draw_state(rand):
    if rand <= C.LOW_PROB:
        return 'Low'
    elif rand <= C.LOW_PROB + C.MEDIUM_PROB:
        return 'Medium'
    else:
        return 'High'

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
        group.your_state = draw_state(random.randint(1, C.RAND_MAX))

    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.b1_p1_round = random.randint(1, C.PART1_ROUNDS)

    if subsession.round_number == C.PART1_ROUNDS + 1:
        for player in subsession.get_players():
            r1, r2 = random.sample(range(C.PART1_ROUNDS + 1, C.NUM_ROUNDS + 1), 2)

            player.participant.b1_p2_round = r1
            player.participant.b1_bel_round = r2


class Part1Intro(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == 1

class FirstStage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        fields = ['first_decision']
        if player.round_number > C.PART1_ROUNDS:
            fields += ['belief_s1']
        return fields

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
            state=player.group.your_state,
            delayed_a=C.ENDOWMENT - C.DELAY_COST,
            show_beliefs=player.round_number > C.PART1_ROUNDS,
        )

class AfterFirstStage(WaitPage):
    pass

class SecondStage(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        fields = ['second_decision']
        return fields

    @staticmethod
    def is_displayed(player: Player):
        return player.first_decision == 'action_b'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(round_number=player.round_number,
                    state=player.group.your_state,
                    delayed_a=10-C.DELAY_COST,
                    your_state=player.group.your_state)

class AfterSecondStage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        calculate_payoffs(group)

        # Store payoffs for selected rounds in participant vars
        for player in group.get_players():
            if player.round_number == player.participant.b1_p1_round:
                player.participant.b1_p1_payoff = float(player.payoff)
                player.participant.b1_p1_state = player.group.your_state
                player.participant.b1_p1_action = get_player_action(player)
                other = player.get_others_in_group()[0]
                player.participant.b1_p1_other_action = get_player_action(other)

            if player.round_number == player.participant.b1_p2_round:
                player.participant.b1_p2_payoff = float(player.payoff)
                player.participant.b1_p2_state = player.group.your_state
                player.participant.b1_p2_action = get_player_action(player)
                other = player.get_others_in_group()[0]
                player.participant.b1_p2_other_action = get_player_action(other)

            if player.round_number == player.participant.b1_bel_round:
                player.participant.b1_bel_state = player.group.your_state
                other = player.get_others_in_group()[0]

                # S1 belief payment (belief_s1) using BQSR mechanism
                other_chose_a_s1 = (other.first_decision == 'action_a')
                player.participant.b1_bel_s1 = player.belief_s1
                player.participant.b1_bel_s1_other_action = 'action_a' if other_chose_a_s1 else 'action_b'

                r1_s1 = random.randint(0, 100)
                r2_s1 = random.randint(0, 100)
                player.belief_draw1_s1 = r1_s1
                player.belief_draw2_s1 = r2_s1
                player.participant.b1_bel_s1_draw1 = r1_s1
                player.participant.b1_bel_s1_draw2 = r2_s1

                if other_chose_a_s1:
                    player.belief_rewarded_s1 = (player.belief_s1 > r1_s1) or (player.belief_s1 > r2_s1)
                else:
                    player.belief_rewarded_s1 = ((100 - player.belief_s1) > r1_s1) or ((100 - player.belief_s1) > r2_s1)

                player.participant.b1_bel_s1_payoff = (
                    C.BELIEF_REWARD if player.belief_rewarded_s1 else 0
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
            your_state = player.group.your_state,
            payoff_value=int(player.payoff)
        )


class Part1Outro(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == C.PART1_ROUNDS


class AfterPart1(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants to finish Part 1.'

    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == C.PART1_ROUNDS


class Part2Intro(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.PART1_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):

        other = player.get_others_in_group()[0]
        return dict(
            part2_rounds=C.NUM_ROUNDS-C.PART1_ROUNDS,
        )

class Part2Outro(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class AfterPart2(WaitPage):
    wait_for_all_groups = True
    title_text = 'Please wait'
    body_text = 'Waiting for all participants to finish Part 2.'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [Part1Intro, FirstStage, AfterFirstStage, SecondStage, AfterSecondStage,
                 Results, Part1Outro, AfterPart1, Part2Intro, Part2Outro, AfterPart2]
