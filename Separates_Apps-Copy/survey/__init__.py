
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass

def creating_session(subsession: Subsession):
    bot_positions = subsession.session.config.get('bot_player_positions') or []
    default_strategy = subsession.session.config.get('bot_strategy', 'majority_cooperate')
    for player in subsession.get_players():
        participant = player.participant
        if player.id_in_subsession in bot_positions:
            participant.bot_strategy = default_strategy
            player.PlayerID = player.id_in_subsession
        else:
            participant.vars.pop('bot_strategy', None)

class Player(BasePlayer):
    PlayerID = models.IntegerField(
    max = 999,
    min = 1
    )
    MajorORFieldOfWork = models.StringField(choices=[['Health and Social Sciences', 'Health and Social Sciences'], ['Business and Economics', 'Business and Economics'], ['Art and Humanities', 'Art and Humanities'], ['STEM', 'STEM']], label='Which of the following options best describes your field of study or work?', widget=widgets.RadioSelect)
    gender = models.StringField(choices=[['Male', 'Male'], ['Female', 'Female'], ['Nonbinary', 'Nonbinary'], ['Other', 'Other']], label='What best describes your gender?', widget=widgets.RadioSelect)
    YearlyPersonalIncome = models.StringField(choices=[['$0 - $12,000', '$0 - $12,000'], ['$12,001 - $40,000', '$12,001 - $40,000'], ['$40,001 - $86,000', '$40,001 - $86,000'], ['$86,001+', '$86,001+']], label='Yearly Personal Income:', widget=widgets.RadioSelect)
    AgeRange = models.StringField(choices=[['18 - 20', '18 - 20'], ['21 - 25', '21 - 25'], ['26 - 34', '26 - 34'], ['35+', '35+']], label='Which age range are you in?', widget=widgets.RadioSelect)
    Self_reported_altruism = models.StringField(choices=[['Often', 'Often'], ['Occasionally', 'Occasionally'], ['Rarely', 'Rarely'], ['Never', 'Never']], label='How often are you willing to go slightly out of your way to help someone?', widget=widgets.RadioSelect)
    Competitiveness = models.StringField(choices=[['Highly', 'Highly'], ['Somewhat', 'Somewhat'], ['Very Little', 'Very Little']], label='How competitive would your friends say you are?', widget=widgets.RadioSelect)
    @property
    def is_bot(self):
        return self.participant.vars.get('bot_strategy') is not None
class Survey(Page):
    form_model = 'player'
    form_fields = ['MajorORFieldOfWork','gender','YearlyPersonalIncome','AgeRange','Self_reported_altruism','Competitiveness']
    @staticmethod
    def get_timeout_seconds(player: Player):
        # Let bots auto-advance without a human submitting for them
        return 1 if player.is_bot else None
class Results(Page):
    form_model = 'player'
    #allow_back_button = True
    #preserve_unsubmitted_form = True
    @staticmethod
    def get_timeout_seconds(player: Player):
        # Let bots auto-advance without a human submitting for them
        return 1 if player.is_bot else None
class Thank_You(Page):
    form_model = 'player'
    @staticmethod
    def get_timeout_seconds(player: Player):
        # Let bots auto-advance without a human submitting for them
        return 1 if player.is_bot else None
page_sequence = [Survey, Results, Thank_You]