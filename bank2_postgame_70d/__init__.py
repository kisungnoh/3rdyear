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

    # Period 1 — by Pre-Bank withdrawal count (0, 1, 2)
    period1_choice_0 = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_certainty_0 = models.IntegerField(min=50, max=100, blank=True, label="")

    period1_choice_1 = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_certainty_1 = models.IntegerField(min=50, max=100, blank=True, label="")

    period1_choice_2 = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period1_certainty_2 = models.IntegerField(min=50, max=100, blank=True, label="")

    # Period 2 — by Observer message (Left / Right)
    period2_choice_left = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period2_certainty_left = models.IntegerField(min=50, max=100, blank=True, label="")

    period2_choice_right = models.StringField(
        choices=[['withdraw', 'Withdraw'], ['stay', 'Stay']],
        widget=widgets.RadioSelect,
        label=""
    )
    period2_certainty_right = models.IntegerField(min=50, max=100, blank=True, label="")

    # Explanation
    sw_reason = models.LongStringField(
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
        return 'Withdraw in Period 1 (W)'
    elif action == 'late':
        return 'Stay in Period 1 → Withdraw in Period 2 (SW)'
    else:  # stay
        return 'Stay in Period 1 → Stay in Period 2 (SS)'


class PostSurveyQ1(Page):
    form_model = 'player'
    form_fields = [
        'period1_choice_0', 'period1_certainty_0',
        'period1_choice_1', 'period1_certainty_1',
        'period1_choice_2', 'period1_certainty_2',
    ]

    @staticmethod
    def error_message(player, values):
        errors = {}
        for n in [0, 1, 2]:
            if values[f'period1_certainty_{n}'] is None:
                errors[f'period1_certainty_{n}'] = 'Please move the slider to indicate your certainty.'
        return errors if errors else None

class PostSurveyQ2(Page):
    form_model = 'player'
    form_fields = [
        'period2_choice_left', 'period2_certainty_left',
        'period2_choice_right', 'period2_certainty_right',
    ]

    @staticmethod
    def error_message(player, values):
        errors = {}
        for side in ['left', 'right']:
            if values[f'period2_certainty_{side}'] is None:
                errors[f'period2_certainty_{side}'] = 'Please move the slider to indicate your certainty.'
        return errors if errors else None


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
        total_payment = round(total_earnings_usd + C.PARTICIPATION_FEE, 0)
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

            bret_boxes_collected=player.participant.bret_boxes_collected,
            bret_bomb=player.participant.bret_bomb,
            bret_payoff_usd=bret_payoff_usd,
            total_earnings_usd=total_earnings_usd,
            total_payment=total_payment,
        )

page_sequence = [PostSurveyQ1, PostSurveyQ2, CRT, Demographic, Payment]
