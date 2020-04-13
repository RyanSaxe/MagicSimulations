import sys
import os
sys.path.append(os.path.abspath('src'))
from modules import Game, Simulation, Deck
import numpy as np

class GyrudaDeck(Deck):
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

class GyrudaGame(Game):
    def __init__(
        self,
        deck,
        on_the_play=True,
    ):
        super().__init__(
            deck,
            on_the_play=True,
        )
        self.clone = self.deck['clone']
        self.win_flag = False
        self.end = False
    
    def turn(self):
        if (self.on_the_play):
            pass
        else:
            self.draw()
        self.win_flag = self.cast_companion()
        #ensure only run one turn
        self.end = True

    def terminate_condition(self):
        return self.end

    def summary(self):
        return 1 if self.win_flag else 0

    def cast_companion(self):
        if self.library.size <= 4:
            return True
        elif self.clone in self.library[:4]:
            self.library.move_to(
                self.graveyard,
                range(4)
            )
            return self.cast_companion()
        else:
            return False

deck = GyrudaDeck(
    {
        'other':26,
        'clone':34,
    },
    mtg_format='legacy',
)

N,processes = map(int,sys.argv[1:])

sim = Simulation(
    deck,
    GyrudaGame,
)

game_summaries = sim(
    N=N,
    processes=processes,
    debug=False
)

result = np.average(game_summaries)
print(f"{result}")
