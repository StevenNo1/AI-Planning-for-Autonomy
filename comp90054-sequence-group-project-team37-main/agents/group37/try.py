from template import Agent

#import sys
#sys.path.append(’agents/group37/’)
import time
import random
import math
#from time import time

class myAgent(Agent):
    def __init__(self,_id):
        super().__init__(_id)
    
    def SelectAction(self,actions,game_state):
        #print('actions:',actions[0])
        #time.sleep(0.9)
        
        #return actions[0]
        #return random.choice(actions)
        #start = time()
        
        #method 1:
        a=0
        
        max_length = float('inf')
        all_coor=set()
        
        #print("actions",actions)
        for action1 in actions:
            all_coor.add(action1['coords'])
            cor = action1['coords']
            #choose_action = {}
            if cor == None and action1['type'] == 'trade':
            #if type(cor) != int or float:
                continue
                #return action1
            #if action1['type'] == 'trade':
            #    continue
            c,r = cor
            a+=1
            #if action1['type'] == 'trade':
            #    return action1
            if abs(c-5.5) + abs(r-5.5) < max_length:
                max_length = abs(c-5.5) + abs(r-5.5)
                choose_action = action1
                #print(choose_action)
            #elif action1 == actions[len(actions)]:
            elif a == len(actions):
                #if choose_action == {}:
                #    return random.choice(actions)
                #else:
                return choose_action
                #print(choose_action)
            else:
                pass
        if all_coor == {None}:
            return random.choice(actions)
        #end = time()
        #print('running time is :%s seconds'%(end - start))
        #calScore(self, game_state,agent_id=0)
        #self.current_game_state.board.draft
        #method 2:(SaSa)
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
        