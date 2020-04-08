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
        self.mana = 0
        self.turns = 0
        self.cycle_count = 0
    
    def turn(self):
        if (self.on_the_play) and (self.turns == 0):
            pass
        else:
            self.draw()
        self.turns += 1
        self.mana = self.turns
        cyclers = self.hand.find(self.deck['yidaro'])
        for cycler in cyclers:
            if self.mana >= 2:
                out = self.cycle(cycler)
                if out:
                    break

    def terminate_condition(self):
        return self.cycle_count >= 4

    def summary(self):
        return self.turns + 6 + 3

    def cycle(self,hand_index):
        self.cycle_count += 1
        if self.cycle_count == 4:
            return True
        self.mana -= 2
        self.hand.move_to(
            self.library,
            hand_index
        )
        self.library.shuffle()
        self.draw()
        #if you draw it off itself
        if self.hand[0] == 1:
            if self.mana >= 2:
                return self.cycle(0)
        return False

deck = YidaroDeck(
    {
        'yidaro':4,
        'mountain':56,
    },
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
