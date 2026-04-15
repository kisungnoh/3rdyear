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
        # Game payoffs
        p2_payoff        = int(player.participant.b2_p2_payoff)
        p3_payoff        = int(player.participant.b2_p3_payoff)

        # Stage 1 belief — other's action (BQSR)
        bel_s1_payoff    = int(player.participant.b2_bel_s1_payoff)
        bel_s1_a         = int(player.participant.b2_bel_s1)
        bel_s1_b         = 100 - bel_s1_a
        bel_s1_other_action = player.participant.b2_bel_s1_other_action
        r1_s1            = int(player.participant.b2_bel_s1_draw1)
        r2_s1            = int(player.participant.b2_bel_s1_draw2)
        if bel_s1_other_action == 'action_a':
            bel_s1_rewarded = (bel_s1_a > r1_s1) or (bel_s1_a > r2_s1)
        else:
            bel_s1_rewarded = (bel_s1_b > r1_s1) or (bel_s1_b > r2_s1)

        # State belief (BQSR)
        bel_state_payoff  = int(player.participant.b2_bel_state_payoff)
        bel_act_state     = player.participant.b2_bel_act_state
        bel_picked_state  = player.participant.b2_bel_picked_state
        bel_state_rep     = int(player.participant.b2_bel_state_reported)
        bel_state_comp    = 100 - bel_state_rep
        r1_st             = int(player.participant.b2_bel_state_draw1)
        r2_st             = int(player.participant.b2_bel_state_draw2)
        if bel_act_state == bel_picked_state:
            bel_state_rewarded = (bel_state_rep > r1_st) or (bel_state_rep > r2_st)
        else:
            bel_state_rewarded = (bel_state_comp > r1_st) or (bel_state_comp > r2_st)

        # USD conversions
        p2_payoff_usd        = round(p2_payoff        * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        p3_payoff_usd        = round(p3_payoff        * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        bel_s1_payoff_usd    = round(bel_s1_payoff    * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        bel_state_payoff_usd = round(bel_state_payoff * C.REAL_WORLD_CURRENCY_PER_POINT, 2)
        bret_payoff_usd      = player.participant.bret_payoff_dollars or 0.0
        total_earnings_usd   = round(
            (p2_payoff + p3_payoff + bel_s1_payoff + bel_state_payoff) * C.REAL_WORLD_CURRENCY_PER_POINT
            + bret_payoff_usd, 2
        )
        total_payment = total_earnings_usd + C.PARTICIPATION_FEE
        player.participant.b2_total_payment = total_payment

        return dict(
            # Part 2 game (rounds 1–2)
            p2_round=player.participant.b2_p2_round,
            p2_payoff=p2_payoff,
            p2_payoff_usd=p2_payoff_usd,
            p2_state=player.participant.b2_p2_state,
            p2_action=action_label(player.participant.b2_p2_action),
            p2_other_action=action_label(player.participant.b2_p2_other_action),

            # Part 3 game (rounds 3–5)
            p3_round=player.participant.b2_p3_round,
            p3_payoff=p3_payoff,
            p3_payoff_usd=p3_payoff_usd,
            p3_state=player.participant.b2_p3_state,
            p3_action=action_label(player.participant.b2_p3_action),
            p3_other_action=action_label(player.participant.b2_p3_other_action),

            # Stage 1 belief — other's action
            bel_s1_round=player.participant.b2_bel_s1_round,
            bel_s1_payoff=bel_s1_payoff,
            bel_s1_payoff_usd=bel_s1_payoff_usd,
            bel_s1_a=bel_s1_a,
            bel_s1_b=bel_s1_b,
            bel_s1_other_action=bel_s1_other_action,
            bel_s1_draw1=r1_s1,
            bel_s1_draw2=r2_s1,
            bel_s1_rewarded=bel_s1_rewarded,

            # State belief
            bel_state_round=player.participant.b2_bel_state_round,
            bel_state_payoff=bel_state_payoff,
            bel_state_payoff_usd=bel_state_payoff_usd,
            bel_act_state=bel_act_state,
            bel_picked_state=bel_picked_state,
            bel_state_rep=bel_state_rep,
            bel_state_comp=bel_state_comp,
            bel_state_draw1=r1_st,
            bel_state_draw2=r2_st,
            bel_state_rewarded=bel_state_rewarded,

            bret_payoff_usd=bret_payoff_usd,
            total_earnings_usd=total_earnings_usd,
            total_payment=total_payment,
        )

page_sequence = [PostSurveyQ1, PostSurveyQ2, PostSurveyQ3, CRT, Demographic, Payment]
