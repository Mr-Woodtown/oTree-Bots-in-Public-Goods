from otree.api import *

# shortens a currency field to a lowercase c
c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'public_goods_Intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
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


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    PlayerID = models.IntegerField(
        max = 999,
        min = 1
    )
    Question1Ans = models.CurrencyField(
        initial=c(0)
    )

    @property
    def is_bot(self):
        return self.participant.vars.get('bot_strategy') is not None

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

class Welcome(Page):
    form_model = 'player'
    form_fields = ['PlayerID']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not player.is_bot
    
    def before_next_page(self, timeout_happened):
        if not self.is_bot:
            self.participant.label = str(self.PlayerID)
            print(f"Set partcipant label to: {self.participant.label}") # Console debug statemnet


class Instruction(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not player.is_bot    


class UnderstandingCheck(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not player.is_bot

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            poolCalculation=4
        )


page_sequence = [Welcome, Instruction, UnderstandingCheck]
