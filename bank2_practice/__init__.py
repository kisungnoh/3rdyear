from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'bank2_practice'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    ENDOWMENT = 10
    DELAY_COST = 1
    SUCCESS_PAYOFF = 18
    FAIL_PAYOFF = 0

# Fixed states for each practice round
    PRACTICE_STATES = ['Low', 'High', 'Medium']


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
    practice_payoff = models.IntegerField(initial=0)


# --- Helper functions ---

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
        else:
            return C.FAIL_PAYOFF
    elif state == 'Medium':
        if action == 'early':
            return C.ENDOWMENT
        elif action == 'late':
            return C.ENDOWMENT if other_action == 'stay' else C.ENDOWMENT - C.DELAY_COST
        else:
            return C.SUCCESS_PAYOFF if other_action == 'stay' else C.FAIL_PAYOFF
    else:  # High
        if action == 'early':
            return C.ENDOWMENT
        elif action == 'late':
            return C.ENDOWMENT
        else:
            return C.SUCCESS_PAYOFF


# --- Session creation ---

def creating_session(subsession: Subsession):
    subsession.group_randomly()
    state = C.PRACTICE_STATES[subsession.round_number - 1]
    for group in subsession.get_groups():
        group.your_state = state


# --- Pages ---

class FirstStage(Page):
    form_model = 'player'
    form_fields = ['first_decision']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
            state=player.group.your_state,
            delayed_a=C.ENDOWMENT - C.DELAY_COST,
        )


class AfterFirstStage(WaitPage):
    pass


class SecondStage(Page):
    form_model = 'player'
    form_fields = ['second_decision']

    @staticmethod
    def is_displayed(player: Player):
        return player.first_decision == 'action_b'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
            state=player.group.your_state,
            delayed_a=C.ENDOWMENT - C.DELAY_COST,
        )


class AfterSecondStage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        state = group.your_state
        for p in group.get_players():
            other = p.get_others_in_group()[0]
            p.practice_payoff = get_payoff(
                get_player_action(p),
                get_player_action(other),
                state
            )
            p.payoff = 0  # practice rounds do not contribute to payment


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other = player.get_others_in_group()[0]
        return dict(
            round_number=player.round_number,
            other=other,
            delayed_a=C.ENDOWMENT - C.DELAY_COST,
            your_state=player.group.your_state,
            payoff_value=player.practice_payoff,
        )


page_sequence = [FirstStage, AfterFirstStage, SecondStage, AfterSecondStage, Results]
