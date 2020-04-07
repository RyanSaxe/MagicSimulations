import numpy as np

class Game:
    def __init__(self):
        self.make_deck()
        self.draw_hand()
        self.lands = 0
        self.mana = 0
        self.win = 0

    def make_deck(self):
        self.deck = np.zeros(60)
        self.deck[:4] = 1
        self.shuffle()
    
    def shuffle(self):
        np.random.shuffle(self.deck)
    
    def draw_hand(self):
        self.hand = self.deck[:7]
        self.deck = self.deck[7:]
    
    def draw(self):
        self.hand = np.insert(
            self.hand,
            0,
            self.deck[0],
        )
        self.deck = self.deck[1:]
    
    def take_turn(self):
        self.lands += 1
        self.mana = self.lands
        cyclers = np.where(self.hand == 1)
        for cycler in cyclers:
            if self.mana >= 2:
                self.cycle(cyclers)

    def cycle(self,hand_index):
        self.hand = np.delete(self.hand,hand_index)
        self.deck = np.insert(
            self.deck,
            0,
            1
        )
        self.shuffle()
        if self.deck[0] == 1:
            self.win += 1
        self.draw()
        self.mana -= 2
        
    def play(self):
        while self.win < 4:
            self.take_turn()
        return self.lands

import sys
n_sims = int(sys.argv[1])
n_turns = []
for i in range(n_sims):
    game = Game()
    n_turns.append(game.play())
print(np.average(n_turns))


