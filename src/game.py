import numpy as np

class Game:
    def __init__(
        self,
        on_the_play=True,
        max_mull=4,
    ):
        self.on_the_play = True
        self.max_mull = max_mull
        self.initialize()

    def initialize(self):
        self.build_deck()
        self.shuffle_deck()
        handsize = 7
        self.hand = self.deck[:handsize]
        while self.mulligan() and (handsize > self.max_mull):
            handsize -= 1
            self.shuffle_deck()
            self.hand = self.deck[:handsize]
        self.deck = self.deck[handsize:]

    def build_deck(self, shuffle=True):
        """
        override to define a deck
        """
        raise NotImplementedError

    def shuffle_deck(self):
        np.random.shuffle(self.deck)

    def mulligan(self):
        """
        override with mulligan strategy
        """
        raise NotImplementedError

    