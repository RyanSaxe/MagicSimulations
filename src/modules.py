import numpy as np
import mtg_globals
import warnings
from itertools import chain
import multiprocessing

class Zone:

    def __init__(self,init_zone=None):
        self.init_zone = init_zone
        self.reset()

    @property
    def size(self):
        return len(self.zone)

    def __getitem__(self,indexer):
        return self.zone[indexer]

    def reset(self):
        if self.init_zone is None:
            self.zone = np.array([],dtype=np.int8)
        else:
            self.zone = self.init_zone
    
    def move_to(self, new_zone, cur_locations, new_locations=None):
        if isinstance(cur_locations,(np.integer,int)):
            cur_locations = [cur_locations]
        if new_locations is None:
            #if no location specified, add to the front
            new_locations = [0] * len(cur_locations) 
        cards = self.zone[cur_locations]
        self.zone = np.delete(self.zone,cur_locations)
        new_zone.zone = np.insert(
            new_zone.zone,
            new_locations,
            cards,
        )

    def shuffle(self):
        np.random.shuffle(self.zone)

    def find(self, card_id):
        return np.where(self.zone == card_id)[0]

class Deck:

    def __init__(
        self,
        cards,
        mtg_format=None,
    ):
        self.format = mtg_format
        self.cards = cards
        if not self.is_legal:
            warnings.warn(f'This deck is not {self.format} legal.')
        self.map = {
            card_name:i for i,card_name in enumerate(self.cards.keys())
        }

    @property
    def is_legal(self):
        #need to implement format legality
        return True

    def __getitem__(self,key):
        return self.map[key]

    def build_library(self):
        deck = []
        for name,count in self.cards.items():
            idx = self.map[name]
            deck.append([idx] * count)
        deck = list(chain.from_iterable(deck))
        return Zone(init_zone=np.array(deck,dtype=np.int8))


    def mulligan(self, hand):
        """
        override with mulligan strategy
        """
        raise NotImplementedError

class Game:

    def __init__(
        self,
        deck,
        on_the_play=True,
    ):
        self.deck = deck
        self.on_the_play = True
        self.create_zones(deck)

    def __call__(self):
        self.start()
        while not self.terminate_condition():
            self.turn()
        return self.summary()

    def create_zones(self, deck):
        self.hand = Zone()
        self.battlefield = Zone()
        self.graveyard = Zone()
        self.exile = Zone()
        self.library = deck.build_library()

    def draw(self,N=1):
        self.library.move_to(
            self.hand,
            range(N),
        )

    def play_card(self, card, from_zone=None):
        #default zone to play from is hand
        if from_zone is None:
            from_zone = self.hand
        #check if allowed to play
        location_from,location_to = self.allowed_to_play(
            card,
            from_zone = from_zone,
            to_zone = self.battlefield,
        )
        if location_from is not None:
            self.hand.move_to(
                self.battlefield,
                location_from,
                location_to,
            )
            
    def start(self):
        self.library.shuffle()
        handsize = mtg_globals.HANDSIZE
        self.draw(handsize)
        while self.deck.mulligan(self.hand):
            handsize -= 1
            self.library.reset()
            self.hand.reset()
            self.library.shuffle()
            self.draw(handsize)

    def allowed_to_play(self, card, from_zone, to_zone):
        """
        override with logic to check if cards can be played
        """
        raise NotImplementedError

    def turn(self):
        """
        override with logic for how to play turns of the game
        """
        raise NotImplementedError

    def terminate_condition(self):
        """
        override with logic for how to play turns of the game
        """
        raise NotImplementedError

    def summary(self):
        """
        override with logic for summarizing game result
        """
        raise NotImplementedError

class Simulation:

    def __init__(
        self,
        deck_instance,
        game_class,
        **game_kwargs,
    ):
        self.deck = deck_instance
        self.game_class = game_class
        self.game_kwargs = game_kwargs

    def __call__(self,N=100,processes=4,debug=False):
        if debug:
            #don't parallelize for debugging
            return [
                self.simulate(i) for i in range(N)
            ]
        with multiprocessing.Pool(processes) as pool:
            out = pool.map(
                self.simulate,
                range(N),
            )
        return out
    
    def simulate(self,sim_number):
        game = self.game_class(self.deck,**self.game_kwargs)
        return game()

