from template import Agent

#import sys
#sys.path.append(’agents/group37/’)
import time
import random
import math
from collections import defaultdict
#from time import time

class myAgent(Agent):
    def __init__(self,_id):
        super().__init__(_id)
        """
        BOARD = [['jk','2s','3s','4s','5s','6s','7s','8s','9s','jk'],
         ['6c','5c','4c','3c','2c','ah','kh','qh','th','ts'],
         ['7c','as','2d','3d','4d','5d','6d','7d','9h','qs'],
         ['8c','ks','6c','5c','4c','3c','2c','8d','8h','ks'],
         ['9c','qs','7c','6h','5h','4h','ah','9d','7h','as'],
         ['tc','ts','8c','7h','2h','3h','kh','td','6h','2d'],
         ['qc','9s','9c','8h','9h','th','qh','qd','5h','3d'],
         ['kc','8s','tc','qc','kc','ac','ad','kd','4h','4d'],
         ['ac','7s','6s','5s','4s','3s','2s','2h','3h','5d'],
         ['jk','ad','kd','qd','td','9d','8d','7d','6d','jk']]

        #Store dict of cards and their coordinates for fast lookup.
        COORDS = defaultdict(list)
        for row in range(10):
            for col in range(10):
                COORDS[BOARD[row][col]].append((row,col))
        
        COORDS = {'jk': [(0, 0), (0, 9), (9, 0), (9, 9)], '2s': [(0, 1), (8, 6)], '3s': [(0, 2), (8, 5)], '4s': [(0, 3), (8, 4)], '5s': [(0, 4), (8, 3)], '6s': [(0, 5), (8, 2)], '7s': [(0, 6), (8, 1)], '8s': [(0, 7), (7, 1)], '9s': [(0, 8), (6, 1)], '6c': [(1, 0), (3, 2)], '5c': [(1, 1), (3, 3)], '4c': [(1, 2), (3, 4)], '3c': [(1, 3), (3, 5)], '2c': [(1, 4), (3, 6)], 'ah': [(1, 5), (4, 6)], 'kh': [(1, 6), (5, 6)], 'qh': [(1, 7), (6, 6)], 'th': [(1, 8), (6, 5)], 'ts': [(1, 9), (5, 1)], '7c': [(2, 0), (4, 2)], 'as': [(2, 1), (4, 9)], '2d': [(2, 2), (5, 9)], '3d': [(2, 3), (6, 9)], '4d': [(2, 4), (7, 9)], '5d': [(2, 5), (8, 9)], '6d': [(2, 6), (9, 8)], '7d': [(2, 7), (9, 7)], '9h': [(2, 8), (6, 4)], 'qs': [(2, 9), (4, 1)], '8c': [(3, 0), (5, 2)], 'ks': [(3, 1), (3, 9)], '8d': [(3, 7), (9, 6)], '8h': [(3, 8), (6, 3)], '9c': [(4, 0), (6, 2)], '6h': [(4, 3), (5, 8)], '5h': [(4, 4), (6, 8)], '4h': [(4, 5), (7, 8)], '9d': [(4, 7), (9, 5)], '7h': [(4, 8), (5, 3)], 'tc': [(5, 0), (7, 2)], '2h': [(5, 4), (8, 7)], '3h': [(5, 5), (8, 8)], 'td': [(5, 7), (9, 4)], 'qc': [(6, 0), (7, 3)], 'qd': [(6, 7), (9, 3)], 'kc': [(7, 0), (7, 4)], 'ac': [(7, 5), (8, 0)], 'ad': [(7, 6), (9, 1)], 'kd': [(7, 7), (9, 2)]}
        """
    
    def SelectAction(self,actions,game_state):

        """
        BOARD = [['jk','2s','3s','4s','5s','6s','7s','8s','9s','jk'],
         ['6c','5c','4c','3c','2c','ah','kh','qh','th','ts'],
         ['7c','as','2d','3d','4d','5d','6d','7d','9h','qs'],
         ['8c','ks','6c','5c','4c','3c','2c','8d','8h','ks'],
         ['9c','qs','7c','6h','5h','4h','ah','9d','7h','as'],
         ['tc','ts','8c','7h','2h','3h','kh','td','6h','2d'],
         ['qc','9s','9c','8h','9h','th','qh','qd','5h','3d'],
         ['kc','8s','tc','qc','kc','ac','ad','kd','4h','4d'],
         ['ac','7s','6s','5s','4s','3s','2s','2h','3h','5d'],
         ['jk','ad','kd','qd','td','9d','8d','7d','6d','jk']]
        #Store dict of cards and their coordinates for fast lookup.
        COORDS = defaultdict(list)
        for row in range(10):
            for col in range(10):
                COORDS[BOARD[row][col]].append((row,col))
        """
        COORDS = {'jk': [(0, 0), (0, 9), (9, 0), (9, 9)], '2s': [(0, 1), (8, 6)], '3s': [(0, 2), (8, 5)], '4s': [(0, 3), (8, 4)], '5s': [(0, 4), (8, 3)], '6s': [(0, 5), (8, 2)], '7s': [(0, 6), (8, 1)], '8s': [(0, 7), (7, 1)], '9s': [(0, 8), (6, 1)], '6c': [(1, 0), (3, 2)], '5c': [(1, 1), (3, 3)], '4c': [(1, 2), (3, 4)], '3c': [(1, 3), (3, 5)], '2c': [(1, 4), (3, 6)], 'ah': [(1, 5), (4, 6)], 'kh': [(1, 6), (5, 6)], 'qh': [(1, 7), (6, 6)], 'th': [(1, 8), (6, 5)], 'ts': [(1, 9), (5, 1)], '7c': [(2, 0), (4, 2)], 'as': [(2, 1), (4, 9)], '2d': [(2, 2), (5, 9)], '3d': [(2, 3), (6, 9)], '4d': [(2, 4), (7, 9)], '5d': [(2, 5), (8, 9)], '6d': [(2, 6), (9, 8)], '7d': [(2, 7), (9, 7)], '9h': [(2, 8), (6, 4)], 'qs': [(2, 9), (4, 1)], '8c': [(3, 0), (5, 2)], 'ks': [(3, 1), (3, 9)], '8d': [(3, 7), (9, 6)], '8h': [(3, 8), (6, 3)], '9c': [(4, 0), (6, 2)], '6h': [(4, 3), (5, 8)], '5h': [(4, 4), (6, 8)], '4h': [(4, 5), (7, 8)], '9d': [(4, 7), (9, 5)], '7h': [(4, 8), (5, 3)], 'tc': [(5, 0), (7, 2)], '2h': [(5, 4), (8, 7)], '3h': [(5, 5), (8, 8)], 'td': [(5, 7), (9, 4)], 'qc': [(6, 0), (7, 3)], 'qd': [(6, 7), (9, 3)], 'kc': [(7, 0), (7, 4)], 'ac': [(7, 5), (8, 0)], 'ad': [(7, 6), (9, 1)], 'kd': [(7, 7), (9, 2)]}
        #select all the draft and card
        cards_cor = set()
        #cards_cor = []
        drafts = set()
        #print("actions:",actions)
        for action in actions:
            if action['coords'] == None:
                continue
            if action['draft_card'] == 'jd' or 'jc' or 'js' or 'jh':
                return action
            cards_cor.add(action['coords'])
            #cards_cor.append(action['coords'])
            drafts.add(action['draft_card'])
        if len(cards_cor) == 0:
            return random.choice(actions)
        #print(drafts)
        #print(cards)
        #print('cards_cor:',cards_cor)
        drafts_cor = []
        for draft in drafts:
            drafts_cor.append(COORDS[str(draft)])
        #card_length={}
        #print('drafts_cor:',drafts_cor)
        card_length = []
        for card_cor in list(cards_cor):
            #print('card_cor:',card_cor)
            #card_length[str(card_cor)] = calculate_distance(card_cor, drafts_cor)
            #card_length.append([card_cor,calculate_distance(card_cor, drafts_cor)])
            cc,cr = card_cor
            length = 0
            for a in drafts_cor:
                for b in a:
                    dc,dr = b
                    length = length + abs(cc-dc) + abs(cr-dr)
            #card_length.append([card_cor,(length+abs(cc-5.5)+abs(cr-5.5))])
            card_length.append([card_cor,length])
        #print('cards_cor:',cards_cor)
        #print('card_length:',card_length)
        card_length.sort(key=lambda x: x[1])
        shortest_length_cor = card_length[0][0]
        #not sure whether we need to consider next draft, I did not
        for action in actions:
            if shortest_length_cor == action['coords']:
                #print("action:",action)
                return action
                
    """
    def calculate_distance(card,drafts):
        cc,cr = card
        length = 0
        for a in drafts:
            for b in a:
                dc,dr = b
                length = length + abs(cc-dc) + abs(cr-dr)
        return length
    """
    