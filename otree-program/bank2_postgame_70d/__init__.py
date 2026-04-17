from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'bank2_postgame_70d'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PARTICIPATION_FEE = 5
    REAL_WORLD_CURRENCY_PER_POINT = 0.5

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # Stage 1
    stage1_choice = models.StringField(
        choices=[['action_a', 'Action A'], ['action_b', 'Action B'], ['even', 'Even']],
        widget=widgets.RadioSelect,
        label=""
    )
    stage1_certainty = models.IntegerField(
        min=50, max=100,
        blank=True,
        label=""
    )

    # Stage 2
    stage2_choice = models.StringField(
        choices=[['action_a', 'Action A'], ['action_b', 'Action B'], ['even', 'Even']],
        widget=widgets.RadioSelect,
        label=""
    )
    stage2_certainty = models.IntegerField(
        min=50, max=100,
        blank=True,
        label=""
    )

    # Explanation
    ba_reason = models.LongStringField(
        blank=True,
        label=""
    )

    # CRT
    CRT1 = models.FloatField(blank=True)
    CRT2 = models.FloatField(blank=True)
    CRT3 = models.FloatField(blank=True)

    # Demographics
    age = models.IntegerField(label="What is your age?")
    gender = models.StringField(
        choices=[['M', 'Male'], ['F', 'Female'], ['NB', 'Non-binary'], ['PNTS', 'Prefer not to say']],
        label="How do you describe your gender?",
        widget=widgets.RadioSelect
    )
    major = models.StringField(
        choices=[
            ['ECON', 'Economics or Business'],
            ['PSY', 'Psychology and Brain Sciences'],
            ['SOC', 'Other Social Science Studies'],
            ['HUM', 'Humanities'],
            ['NAT', 'Mathematics, Computer Science, Engineering or Natural Sciences'],
            ['OTHERS', 'Other major (not listed)'],
            ['PNTS', 'Prefer not to say']],
        label="What is your field of study?"
    )


def action_label(action):
    if action == 'early':
        return 'Action A in Stage 1'
    elif action == 'late':
        return 'Action B in Stage 1 → Action A in Stage 2 (BA)'
    else:  # stay
        return 'Action B in Stage 1 → Action B in Stage 2 (BB)'


class PostSurveyQ1(Page):
    form_model = 'player'
    form_fields = ['stage1_choice', 'stage1_certainty']

    @staticmethod
    def error_message(player, values):
        if values['stage1_certainty'] is None:
            return dict(stage1_certainty='Please move the slider to indicate your certainty.')

class PostSurveyQ2(Page):
    form_model = 'player'
    form_fields = ['stage2_choice', 'stage2_certainty']

    @staticmethod
    def error_message(player, values):
        if values['stage2_certainty'] is None:
            return dict(stage2_certainty='Please move the slider to indicate your certainty.')

class PostSurveyQ3(Page):
    form_model = 'player'
    form_fields = ['ba_reason']

class CRT(Page):
    form_model = 'player'
    form_fields = ['CRT1', 'CRT2', 'CRT3']

class Demographic(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major']

class Payment(Page):
    @staticmethod
    def vars_for_template(player: Player):
        p1_payoff      = int(player.participant.b1_p1_payoff)
        p2_payoff      = int(player.participant.b1_p2_payoff)
        bel_s1_payoff  = int(player.participant.b1_bel_s1_payoff)
        bel_s1_a = int(player.participant.b1_bel_s1)
        bel_s1_b = 100 - bel_s1_a
        bel_s1_other_a = player.participant.b1_bel_s1_other_action == 'action_a'
        r1 = int(player.participant.b1_bel_s1_draw1)
        r2 = int(player.participant.b1_bel_s1_draw2)
        if bel_s1_other_a:
            bel_s1_cond1 = bel_s1_a > r1
            bel_s1_cond2 = bel_s1_a > r2
        else:
            bel_s1_cond1 = bel_s1_b > r1
            bel_s1_cond2 = bel_s1_b > r2
        bel_s1_rewarded    = bel_s1_cond1 or bel_s1_cond2
        p1_payoff_usd      = round(p1_payoff     * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        p2_payoff_usd      = round(p2_payoff     * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        bel_s1_payoff_usd  = round(bel_s1_payoff * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        bret_payoff_usd    = player.participant.bret_payoff_dollars or 0.0
        total_earnings_usd = round((p1_payoff + p2_payoff + bel_s1_payoff) * C.REAL_WORLD_CURRENCY_PER_POINT + bret_payoff_usd, 2)
        total_payment = total_earnings_usd + C.PARTICIPATION_FEE
        player.participant.b1_total_payment = total_payment
        return dict(
            p1_round=player.participant.b1_p1_round,
            p1_payoff=p1_payoff,
            p1_payoff_usd=p1_payoff_usd,
            p1_state=player.participant.b1_p1_state,
            p1_action=action_label(player.participant.b1_p1_action),
            p1_other_action=action_label(player.participant.b1_p1_other_action),

            p2_round=player.participant.b1_p2_round,
            p2_payoff=p2_payoff,
            p2_payoff_usd=p2_payoff_usd,
            p2_state=player.participant.b1_p2_state,
            p2_action=action_label(player.participant.b1_p2_action),
            p2_other_action=action_label(player.participant.b1_p2_other_action),

            bel_round=player.participant.b1_bel_round,
            bel_s1_payoff=bel_s1_payoff,
            bel_s1_payoff_usd=bel_s1_payoff_usd,
            bel_state=player.participant.b1_bel_state,
            bel_s1_a=bel_s1_a,
            bel_s1_b=bel_s1_b,
            bel_s1_other_action=player.participant.b1_bel_s1_other_action,
            bel_s1_draw1=r1,
            bel_s1_draw2=r2,
            bel_s1_cond1=bel_s1_cond1,
            bel_s1_cond2=bel_s1_cond2,
            bel_s1_rewarded=bel_s1_rewarded,
            
            bret_payoff_usd=bret_payoff_usd,
            total_earnings_usd=total_earnings_usd,
            total_payment=total_payment
        )

page_sequence = [PostSurveyQ1, PostSurveyQ2, PostSurveyQ3, CRT, Demographic, Payment]
