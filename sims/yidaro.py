import sys
import os
sys.path.append(os.path.abspath('src'))
from modules import Game
import numpy as np

class YidaroGame(Game):
    def __init__(self):
        super().__init__()
        self.lands = 0
        self.mana = 0
        self.win = 0
        self.ncards = 7

    def build_deck(self):
        deck = np.zeros(60)
        deck[:4] = 1
        return deck

    def mulligan(self):
        return True
    
    def draw(self):
        drawing = self.deck[0]
        self.deck = np.delete(self.deck,0)
        self.hand = np.insert(
            self.hand,
            0,
            drawing,
        )
        self.ncards += 1
    
    def take_turn(self):
        if (self.on_the_play) and (self.lands == 0):
            pass
        else:
            self.draw()       
        self.lands += 1
        self.mana = self.lands
        cyclers = np.where(self.hand == 1)[0]
        for cycler in cyclers:
            if self.mana >= 2:
                out = self.cycle(cycler)
                if out:
                    break

    def cycle(self,hand_index):
        self.win += 1
        if self.win == 4:
            return True
        self.mana -= 2
        self.hand = np.delete(self.hand,hand_index)
        self.deck = np.insert(
            self.deck,
            0,
            1
        )
        self.shuffle()
        self.draw()
        #if you draw it off itself
        if self.hand[0] == 1:
            if self.mana >= 2:
                return self.cycle(0)
        return False
        
    def play(self):
        while self.win < 4:
            self.take_turn()
        return self.lands,self.ncards

import sys
n_sims = int(sys.argv[1])
n_turns = []
n_cards = []
for i in range(n_sims):
    game = YidaroGame()
    turns,cards = game.play()
    n_turns.append(turns)
    n_cards.append(cards)
print("number of turns:",np.average(n_turns))
print("number of cards:",np.average(n_cards))