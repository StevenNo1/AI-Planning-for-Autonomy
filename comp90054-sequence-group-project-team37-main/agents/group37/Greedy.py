from template import Agent
import sys
import time
import numpy
import random
from scipy.spatial import distance
sys.path.append('agents/team37/')

last_action = []


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        #self.last_action = []

    def SelectAction(self, actions, game_state):
        # the availble action with minimal distance to the last action
        currentSelect = actions[0]
        min_distance = 1000
        print('action',actions)

        if last_action != []:  # make the first action be randomly selected
            for last in last_action:
                idx = 0
                for action in actions:  # calculate each action from all available actions with Euclidean
                    if action['coords'] != None:
                        dst = distance.euclidean(
                            last['coords'], action['coords'])
                        if dst < min_distance:
                            min_distance = dst
                            currentSelect = actions[idx]
                        idx += 1
                    else:
                        return random.choice(actions)
                #print("last_corrds: ", game_state.board.plr_coords['r'][-1])
        last_action.append(currentSelect)
        #print("last_coords: ", last_action[-1]['coords'])

        return currentSelect