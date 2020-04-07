import numpy as np
import mtg_globals

class Deck:
    """
    class to hold a Magic deck. 

    cards =  {
        card_name: card_count,
        . . .
    }

    format: name of Magic format 
    """
    def __init__(
        self,
        cards,
        format=None,
    ):
        self.buid_deck(cards)

    def build(self,cards):
        pass

    def shuffle(self):
        pass

    def draw(self, N=1):
        pass

    def mulligan(self):
        """
        override with mulligan strategy
        """
        raise NotImplementedError

    def play(self):
        """
        override with simulation logic
        """
        raise NotImplementedError

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
        self.deck = self.build_deck()
        self.shuffle()
        handsize = mtg_globals.HANDSIZE
        self.hand = self.deck[:handsize]
        while self.mulligan() and (handsize > self.max_mull):
            handsize -= 1
            self.shuffle()
            self.hand = self.deck[:handsize]
        self.deck = self.deck[handsize:]

    def draw(self):
        drawing = self.deck[0]
        self.deck = np.delete(self.deck,0)
        self.hand = np.insert(
            self.hand,
            0,
            drawing,
        )
        #return drawing

    def shuffle(self):
        np.random.shuffle(self.deck)

    def build_deck(self, shuffle=True):
        """
        override to define a deck
        """
        raise NotImplementedError

    def mulligan(self):
        """
        override with mulligan strategy
        """
        raise NotImplementedError

    def play(self):
        """
        override with simulation logic
        """
        raise NotImplementedError

    