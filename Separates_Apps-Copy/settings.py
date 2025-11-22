from os import environ
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, 
    participation_fee=0,
    num_demo_participants=4,
    bot_strategy='majority_cooperate')

SESSION_CONFIGS = [
    dict(
        name='Public_Goods',
        display_name='Public Goods (Manual)',
        num_demo_participants=4,
        app_sequence=['Introduction','public_goods_simple','survey'],
    ),
    dict(
        name='Public_Goods_With_2_Bots', 
        display_name='Public Goods with a Twist',
        num_demo_participants=4, 
        app_sequence=['Introduction','public_goods_simple','survey'],
        bot_player_positions=[3, 4],
    ),
    dict(
        name='Survey_Troubleshoot', 
        display_name='Public Goods Survey',
        num_demo_participants=4, 
        app_sequence=['Introduction','survey'],
        bot_player_positions=[3, 4],
    ),
]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['bot_strategy']
SESSION_FIELDS = []
ROOMS = [dict(name='Group_With_Bots_A', display_name='Room A'),
    dict(name='Group_With_Bots_B', display_name='Room B'),
    dict(name='Group_of_Only_Humans', display_name='Room C'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = '2889755009'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


