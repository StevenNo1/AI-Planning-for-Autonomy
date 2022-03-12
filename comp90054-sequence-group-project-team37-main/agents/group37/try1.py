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
        #print(game_state.id)
        print('id:',self.id)
        print('chips:',self.board.chips)
        return actions[0]