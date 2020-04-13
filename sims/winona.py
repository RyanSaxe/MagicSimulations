import sys
import os
sys.path.append(os.path.abspath('src'))
from modules import Game, Simulation, Deck
import mtg_globals
import numpy as np
import pdb
class WinotaDeck(Deck):
    def __init__(
        self,
        cards,
        mtg_format=None,
    ):
        super().__init__(
            cards, mtg_format=mtg_format
        )

    def mulligan(self, obj, handsize):
        """
        Description of mulligan strategy:

        1 - Do not mulligan below 5 cards
        2 - Keep 2-4 land hands
        3 - When placing cards on the bottom for the london mulligan,
                aim for 3-land hands with non-human creatures.
        """
        hand = obj.hand
        lands = hand.find(self['land'])
        n_lands = len(lands)
        if handsize == 5:
            self.sculpt_hand(
                hand,
                obj.library,
                cuts=mtg_globals.HANDSIZE - handsize
            )
            return False
        elif (n_lands < 2) or (n_lands > 4):
            return True
        else:
            if handsize != mtg_globals.HANDSIZE:
                self.sculpt_hand(
                    hand,
                    obj.library,
                    cuts=mtg_globals.HANDSIZE - handsize
                )
            return False
    
    def sculpt_hand(self, hand, library, cuts=0):
        self.move_card_type(hand, library, cuts, 'other')
        cuts_left = (mtg_globals.HANDSIZE - cuts) - hand.size
        self.move_card_type(hand, library, cuts_left, 'human')
        cuts_left = (mtg_globals.HANDSIZE - cuts) - hand.size
        if cuts_left > 0:
            lands = hand.find(self['land'])
            land_ideal = 3
            if lands <= land_ideal:
                self.move_card_type(hand, library, cuts_left, 'nonhuman')
            else:
                to_cut = (len(lands) - land_ideal)
                to_cut = to_cut if to_cut <= cuts_left else cuts_left
                self.move_card_type(hand, library, to_cut, 'land')
            cuts_left = (mtg_globals.HANDSIZE - cuts) - hand.size
            if cuts_left > 0:
                self.move_card_type(hand, library, cuts_left, 'nonhuman')

    def move_card_type(self, hand, library, cuts, card):
        if cuts > 0:
            bad = hand.find(self[card])
            amount = cuts if len(bad) >= cuts else len(bad)
            going_to = list(range(library.size - amount,library.size))
            cutting = bad[:cuts]
            hand.move_to(
                library,
                cutting,
                going_to
            )
        
class WinotaGame(Game):
    def __init__(
        self,
        deck,
        on_the_play=True,
    ):
        super().__init__(
            deck,
            on_the_play=True,
        )
        self.cast_winota = False
        self.lands = 0
        self.hit_from_winota = 0
        self.turn_n = 0
        self.land = self.deck['land']
        self.human = self.deck['human']
        self.nonhuman = self.deck['nonhuman']
    
    def turn(self):
        if (self.on_the_play):
            if self.turn_n != 0:
                self.draw()
        else:
            self.draw()
        self.turn_n += 1
        lands = self.hand.find(self.land)
        if len(lands) != 0:
            self.play_card(lands[0])
        num_lands = len(self.battlefield.find(self.land))
        if num_lands >= 4:
            self.cast_winota = True
            non_humans = self.battlefield.find(self.nonhuman)
            for i in range(len(non_humans)):
                look_at = self.library[i * 6:(i+1) * 6]
                if self.human in look_at:
                    self.hit_from_winota += 1
        else:
            non_humans = self.hand.find(self.nonhuman)
            if len(non_humans) > 0:
                self.play_card(non_humans[0])
            else:
                humans = self.hand.find(self.human)
                if len(humans) > 0:
                    self.play_card(humans[0])

    def terminate_condition(self):
        return self.cast_winota

    def summary(self):
        return [self.hit_from_winota,self.turn_n]

    def allowed_to_play(self, card, from_zone, to_zone):
        return card,0

deck = WinotaDeck(
    {
        'land':16,
        'human':10,
        'nonhuman':8,
        'other':6,
    },
    mtg_format='legacy',
)
g = WinotaGame(deck)
N,processes = map(int,sys.argv[1:])

sim = Simulation(
    deck,
    WinotaGame,
)

game_summaries = sim(
    N=N,
    processes=processes,
    debug=True
)
turns = [x[1] for x in game_summaries]
hits = [x[0] for x in game_summaries]

print("average turn winota is cast:",np.average(turns))
print("average humans hit off triggers:",np.average(hits))
percent_misses = len(np.where(np.array(hits) == 0)[0]) / len(hits)
print("Percent games where winota misses:",percent_misses)

