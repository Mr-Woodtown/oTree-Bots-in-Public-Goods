from otree.api import *

# shortens a currency field to a lowercase c
c = cu

doc = ''


class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10
    ENDOWMENT = cu(1)
    MULTIPLIER = 1.6
    # Defines how high the average player contribution in the last round must be for the bot to contribute.
    BOT_FORGIVENESS_THRESHOLD = c(0.5)


class Subsession(BaseSubsession):
    pool = models.CurrencyField()


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
    group_ID = models.StringField()
    round_contribution = models.CurrencyField(initial=0)
    individual_share = models.CurrencyField(initial=0)


def round_payoff(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.round_contribution = sum(contributions)
    group.individual_share = group.round_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    for player in players:
        player.payoff = C.ENDOWMENT - player.contribution + group.individual_share


class Player(BasePlayer):
    PlayerID = models.IntegerField(
    max = 999,
    min = 1
    )
    contribution = models.CurrencyField(
        label='How much will you contribute',
        max=C.ENDOWMENT,
        min=0,
        initial=c(0),
    )

    @property
    def is_bot(self):
        return self.participant.vars.get('bot_strategy') is not None


def tit_for_tat_contribution(player: Player):
    if player.round_number == 1:
        return C.ENDOWMENT

    previous_group = player.group.in_round(player.round_number - 1)
    previous_opponents = [
        opponent.contribution
        for opponent in previous_group.get_players()
        if opponent.id_in_subsession != player.id_in_subsession
    ]
    if not previous_opponents:
        return C.ENDOWMENT

    cooperators = sum(1 for contribution in previous_opponents if contribution >= C.ENDOWMENT)
    if cooperators >= len(previous_opponents) / 2:
        return C.ENDOWMENT
    return c(0)


def majority_cooperate_contribution(player: Player):
    # Round 1: bots contribute 1 by default.
    if player.round_number == 1:
        return C.ENDOWMENT

    # From round 2 onward: base on previous round.
    # If the average contribution of Player 1 and Player 2 in the previous
    # round is < 0.5, bots defect (0). Otherwise they contribute 1.
    previous_group = player.group.in_round(player.round_number - 1)
    values = []
    for gid in (1, 2):
        # The parenthetical above is the players' group IDs that are human. 
        try:
            p = previous_group.get_player_by_id(gid)
        except Exception:
            p = None
        if p and p.contribution is not None:
            values.append(p.contribution)

    if not values:
        return C.ENDOWMENT

    avg = sum(values) / len(values)
    if avg < C.BOT_FORGIVENESS_THRESHOLD:
        return c(0)
    return C.ENDOWMENT


BOT_STRATEGIES = {
    'tit_for_tat': tit_for_tat_contribution,
    'majority_cooperate': majority_cooperate_contribution,
}


def get_bot_contribution(player: Player):
    strategy_name = player.participant.vars.get('bot_strategy')
    if not strategy_name:
        return None
    strategy = BOT_STRATEGIES.get(strategy_name)
    if strategy is None:
        return None
    return strategy(player)


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def get_timeout_seconds(player: Player):
        # Let bots auto-advance without a human submitting for them
        return 1 if player.is_bot else None

    @staticmethod
    def get_form_fields(player: Player):
        if player.is_bot:
            return []
        return ['contribution']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.is_bot:
            bot_move = get_bot_contribution(player)
            player.contribution = bot_move if bot_move is not None else c(0)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = round_payoff


class Results(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return not player.is_bot


page_sequence = [Contribute, ResultsWaitPage, Results]
