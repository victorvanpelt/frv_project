from os import environ


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

mturk_hit_settings = {
    'keywords': ['decision-making', 'study', 'academic', 'research', 'problem-solving', 'iq'],
    'title': 'Decision-making study (earn up to $4.10 for +-10 minutes)',
    'description': 'Decision-making study that pays up to $4.10 for approximately 10 minutes.',
    'frame_height': 500,
    'template': 'global/mturk_template.html',
    'minutes_allotted_per_assignment': 45,
    'expiration_hours': 7*24, # 7 days

    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        # No-retakers
        {
            'QualificationTypeId': "384V06JTUF5J61HYJOI99955LXK4CR",
            'Comparator': "DoesNotExist",
        },
        # # Masters
        # {
        #         'QualificationTypeId': "2F1QJWKUDD8XADTFD2Q0G6UTO95ALH",
        #         'Comparator': "Exists",
        # },
        # Only US
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },
        # At least x HITs approved
        {
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [100]
        },
        # At least x% of HITs approved
        {
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [95]
        },
        ]
}
SESSION_CONFIGS = [
    dict(
        name='raven_test_inc_rpi',
        display_name="FVR full incentives rpi",
        num_demo_participants=4,
        app_sequence=['raven', 'coll_dishonest','payment_info'],
        participation_fee=0.50,
        incentives=1,
        rpi=1,
        mturk_hit_settings=mturk_hit_settings
    ),
    dict(
        name='raven_test',
        display_name="FVR full no incentives no rpi",
        num_demo_participants=4,
        app_sequence=['raven', 'coll_dishonest', 'payment_info'],
        participation_fee=0.50,
        incentives=0,
        rpi=0,
        mturk_hit_settings=mturk_hit_settings
    ),
    dict(
        name='raven_test_inc',
        display_name="FVR full incentives no rpi",
        num_demo_participants=4,
        app_sequence=['raven', 'coll_dishonest', 'payment_info'],
        participation_fee=0.50,
        incentives=1,
        rpi=0,
        mturk_hit_settings=mturk_hit_settings
    ),
    dict(
        name='raven_test_rpi',
        display_name="FVR full no incentives rpi",
        num_demo_participants=4,
        app_sequence=['raven', 'coll_dishonest', 'payment_info'],
        participation_fee=0.50,
        incentives=0,
        rpi=1,
        mturk_hit_settings=mturk_hit_settings
    )
]


SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.00,
    doc="",
    #mturk_hit_settings=mturk_hit_settings_cd,
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
POINTS_DECIMAL_PLACES = 2

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Test page for FRV experiments
"""

SECRET_KEY = '3458208590179'

INSTALLED_APPS = ['otree']

PARTICIPANT_FIELDS = [
    'is_dropout',
    'is_dropout_mate',
    'no_time_left',
    'expiry',
    'answers',
    'number_correct',
    'time_left',
    'wait_page_arrival',
    'no_partner'
]