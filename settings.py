from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.0, participation_fee=0.0)
SESSION_CONFIGS = [
                dict(name='bret', display_name='bret', num_demo_participants=2, app_sequence=['bret']),

                dict(name='bank1_instruction', display_name='bank1_instruction', num_demo_participants=2, app_sequence=['bank1_instruction']),
                dict(name='bank1_game', display_name='bank1_game', num_demo_participants=2, app_sequence=['bank1_game']),
                dict(name='bank1_postgame', display_name='bank1_postgame', num_demo_participants=2, app_sequence=['bank1_postgame']),
                dict(name='bank1', display_name='bank1', num_demo_participants=2, app_sequence=['bank1_instruction','bank1_game','bret','bank1_postgame']),
               

                dict(name='bank2_practice', display_name='bank2_practice', num_demo_participants=2, app_sequence=['bank2_practice']),
                dict(name='bank2_instruction_part1', display_name='bank2_instruction_part1', num_demo_participants=2, app_sequence=['bank2_instruction_part1']),
                dict(name='bank2_instruction_part2', display_name='bank2_instruction_part2', num_demo_participants=2, app_sequence=['bank2_instruction_part2']),
                dict(name='bank2_game_70d', display_name='bank2_game_70d', num_demo_participants=2, app_sequence=['bank2_game_70d']),
                dict(name='bank2_postgame_70d', display_name='bank2_postgame_70d', num_demo_participants=2, app_sequence=['bank2_postgame_70d']),

                dict(name='bank2_pilot', display_name='bank2_pilot', num_demo_participants=2, app_sequence=['bank2_instruction_part1','bank2_instruction_part2','bank2_game_70d', 'bret', 'bank2_postgame_70d'])
                ]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = [
    'b1_p1_round', 'b1_p1_payoff', 'b1_p1_state', 'b1_p1_action', 'b1_p1_other_action',
    'b1_p2_round', 'b1_p2_payoff', 'b1_p2_state', 'b1_p2_action', 'b1_p2_other_action',
    'b1_bel_round', 'b1_bel_state', 'b1_bel_s1', 'b1_bel_s1_other_action', 'b1_bel_s1_draw1', 'b1_bel_s1_draw2', 'b1_bel_s1_payoff',
    'b1_total_payment', 'b1_total_earnings',
    
    'b2_p2_round', 'b2_p2_payoff', 'b2_p2_state', 'b2_p2_action', 'b2_p2_other_action',
    'b2_p3_round', 'b2_p3_payoff', 'b2_p3_state', 'b2_p3_action', 'b2_p3_other_action',
    'b2_bel_s1_round', 'b2_bel_s1', 'b2_bel_s1_other_action', 'b2_bel_s1_draw1', 'b2_bel_s1_draw2', 'b2_bel_s1_payoff',
    'b2_bel_state_round', 'b2_bel_act_state', 'b2_bel_picked_state', 'b2_bel_state_reported', 'b2_bel_state_draw1', 'b2_bel_state_draw2', 'b2_bel_state_payoff',
    'b2_total_payment',

    'bret_boxes_collected','bret_bomb','bret_payoff_dollars',
]
SESSION_FIELDS = []
THOUSAND_SEPARATOR = ''
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = '82a812983eb3641cd91d6646538ae450fcd94e9ff69fdb0d58fc5c10cf223963a35c011d131625eaad0eeabe786ffcdb9769'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
