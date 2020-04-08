import sys
import os
sys.path.append(os.path.abspath('src'))
from modules import Game, Simulation, Deck
import numpy as np

class YidaroDeck(Deck):
    def __init__(
        self,
        cards,
        mtg_format=None,
    ):
        super().__init__(
            cards, mtg_format=mtg_format
        )

    def mulligan(self, hand):
        #always keep
        return False

class YidaroGame(Game):
    def __init__(
        self,
        deck,
        on_the_play=True,
    ):
        super().__init__(
            deck,
            on_the_play=True,
        )
    
    def allowed_to_play(self, card, from_zone, to_zone):
        pass

    def turn(self):
        pass

    def terminate_condition(self):
        return self.cycle_count >= 4

deck = YidaroDeck(
    {
        'yidaro, wondering monster':4,
        'mountain':56,
    }
    mtg_format='standard',
)

sim = Simulation(
    deck,
    YidaroGame,
)

game_summaries = sim(
    N=10,
    processes=2,
)
print(game_summaries)
