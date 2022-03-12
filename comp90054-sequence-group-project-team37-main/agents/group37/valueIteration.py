from template import Agent
import sys
import time
import numpy as np
import random
from random import randrange
from scipy.spatial import distance
from collections import defaultdict
sys.path.append('agents/team37/')


### GLOBAL VARIABLES ###
BOARD = [['jk', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'jk'],
         ['6c', '5c', '4c', '3c', '2c', 'ah', 'kh', 'qh', 'th', 'ts'],
         ['7c', 'as', '2d', '3d', '4d', '5d', '6d', '7d', '9h', 'qs'],
         ['8c', 'ks', '6c', '5c', '4c', '3c', '2c', '8d', '8h', 'ks'],
         ['9c', 'qs', '7c', '6h', '5h', '4h', 'ah', '9d', '7h', 'as'],
         ['tc', 'ts', '8c', '7h', '2h', '3h', 'kh', 'td', '6h', '2d'],
         ['qc', '9s', '9c', '8h', '9h', 'th', 'qh', 'qd', '5h', '3d'],
         ['kc', '8s', 'tc', 'qc', 'kc', 'ac', 'ad', 'kd', '4h', '4d'],
         ['ac', '7s', '6s', '5s', '4s', '3s', '2s', '2h', '3h', '5d'],
         ['jk', 'ad', 'kd', 'qd', 'td', '9d', '8d', '7d', '6d', 'jk']]

# ex. {'jk': [(0, 0), (0, 9), (9, 0), (9, 9)], '2s': [(0, 1), (8, 6)],...}
COORDS = defaultdict(list)
for row in range(10):
    for col in range(10):
        COORDS[BOARD[row][col]].append((row, col))
# print("COORDS: ", COORDS)

# actions = {'play_card': '3d', 'draft_card': '2h', 'type': 'place', 'coords': (2, 3)}

# to decide at which point we feel comfortable stopping the algorithm
SMALL_ENOUGH = 20
# discount
GAMMA = 0.3  # 0.9
# the probability of doing a random action rather than the one intended
NOISE = 0.1


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.id = _id
        # V table to store the optimal Q-value[Q*(s, a)] for eachc state Q(s, a)
        # Q*(s, a) = V*(s) = best possible (immediate reward + discounted future reward)
        # {(coords, possible action): 1, ...}  s = current state, a = next possible action
        self.V = {}
        # from taking action a0 in state S0 (immediate reward)
        self.R = {}
        # Q table, Q-value = value when taking that action in that state
        self.Q = {}

    def SelectAction(self, actions, game_state):

        ### CALL valueIetration function ###
        # will get the value table with optimal Q-values
        if actions[0]['type'] == 'trade':
            highest_action = random.choice(actions)
        else:
            self.valueIteration(game_state, actions)
            print("SUCCESS V_I FUNCTION")  # TESTING
            ### CHOOSE the best action to take given a state is the one with highest Q-value ###
            highest_action = actions[0]
            for idx in range(len(actions)-1):
                if self.V[actions[idx]['coords']] < self.V[actions[idx+1]['coords']]:
                    highest_action = actions[idx]

        # currentSelect = self.callFunction(actions, game_state, currentSelect) # TESTING

        return highest_action

    def valueIteration(self, game_state, actions):
        # OUTPUT is the value table, the table that maps state-action pairs to the optimal Q-values(Q*(s, a))

        # ex. [(0, 3), (4, 3), (2, 6), (3, 0)]
        # current_state = game_state.board.plr_coords['r']
        our_color = 'r'
        their_color = 'b'
        if self.id == 1 or self.id == 3:
            our_color = 'b'
            their_color = 'r'

        ### ------ Define an initial V function, V(s) ------ ###
        # search space = current_state to all the possible taken-action state ???
        # because we need't to consider the empty_coords ???
        # or for all states ???
        '''
        for state in current_state:
            self.V[state, action] = randrange(10)
        print("V = ", self.V)
        '''
        for k, v in COORDS.items():
            for idx in range(len(v)):
                self.V[v[idx]] = randrange(10)
        # print("V = ", self.V)  # TESTING
        # print("-------------------------")

        ### ------ Define R for all states (coords) ------ ###
        # HOW TO DEFINE REWARDS ???
        # ex. k = 'js', v = (0,0)
        for k, v in COORDS.items():
            for idx in range(len(v)):
                if v[idx] in [(5, 5), (4, 5), (5, 6), (3, 5), (5, 4), (5, 3), (6, 5), (7, 5), (4, 6), (6, 4), (4, 4)]:
                    self.R[v[idx]] = 10
                elif v[idx] in [(0, 0), (0, 9), (9, 9), (9, 0)]:
                    self.R[v[idx]] = 0
                else:
                    self.R[v[idx]] = 4
        # print("R = ", self.R) # TESTING
        # print("-------------------------")

        ### ------ Define Q-value for all states, Q(s, a) ------ ###
        '''
        for k, v in COORDS.items():
            for idx in range(len(v)):
                for action in actions:
                    self.Q[v[idx], action['coords']] = randrange(10)
        '''
        # for action in actions:
        #    self.Q[action['coords']] = randrange(10)
        # print("Q = ", self.Q) # TESTING
        # print("-------------------------")

        ### ------ ITERATION ------ ###
        # 1. states = COORDS
        # 2. possible states = game_state.board.empty_coords
        # 3. possible actions = actions
        while True:
            change = 0  # Δ

            # for all possible STATES of the enviroment -> empty_coords or ???
            # for state in game_state.board.empty_coords: ???
            idx = 0
            for action in actions:
                # print("INSIDE LOOP - STATES") # TESTING
                # print("state: ", state)  # TESTING
                # v := V(s) extract and store the most recent value of the state
                # old_v = self.V[state]
                old_v = self.V[action['coords']]
                new_v = 0

                # append the success or of action into actions
                for action['draft_card'] in game_state.agents[self.id].hand:
                    if action['draft_card'] in ['jh', 'js']:  # one-eyed jacks
                        print("GET A JJJJJJJ")  # TESTING
                        for r in range(10):
                            for c in range(10):
                                if game_state.board.chips[r][c] == game_state.agents[self.id].opp_colour:
                                    for draft in game_state.board.draft:
                                        actions.append(
                                            {'play_card': action['draft_card'], 'draft_card': draft, 'type': 'remove', 'coords': (r, c)})
                    elif action['draft_card'] in ['jd', 'jc']:  # two-eyed jacks
                        print("GET A JJJJJJJ2222222")  # TESTING
                        for r in range(10):
                            for c in range(10):
                                if game_state.board.chips[r][c] == '_':
                                    for draft in game_state.board.draft:
                                        actions.append(
                                            {'play_card': action['draft_card'], 'draft_card': draft, 'type': 'place', 'coords': (r, c)})
                    else:
                        for c1 in COORDS[action['draft_card']]:
                            # print("CHECK 0: ", c1)  # TESTING
                            # for r, c in c1:
                            # print("CHECK 1: ", c1)  # TESTING
                            # for r, c in c1:
                            r = c1[0]
                            c = c1[1]
                            # print("CHECK 2: ", r, ", ", c)  # TESTING
                            if game_state.board.chips[r][c] == '_':
                                # print("CHECK 3: ",game_state.board.chips[r][c])
                                for draft in game_state.board.draft:
                                    actions.append(
                                        {'play_card': action['draft_card'], 'draft_card': draft, 'type': 'place', 'coords': (r, c)})
                                    print("GET NEW APPEND !!!!")  # TESTING
                del actions[idx]
                # for all possible ACTIONS, based on all possible states
                # for s in current_state: ???
                # print("TO SECOND LOOPPPPPP")  # TESTING
                for sub_action in actions[idx:]:
                    # print("SUB ACTIONNNNN !!!!!!!!")  # TESTING
                    # Q(s, a) = (expected immediate R given the state s and an action a)
                    # + (discount rate) * [summation_over_all_new_states(probability of ending up
                    # in a new state s’given a state s and action a * value of the new state s’)]
                    # v = self.R[s] + (GAMMA * (1 - NOISE) * self.V[action['coords']] + (NOISE * self.V[s])) ???
                    v = self.R[action['coords']] + (GAMMA * ((1 - NOISE) *
                                                             self.V[sub_action['coords']] + (NOISE*self.V[action['coords']])))
                    if v > new_v:
                        new_v = v

                # V(s) := maximum value of Q(s, a) across all the different actions taking from state s
                self.V[action['coords']] = new_v
                # print("new V(s): ", self.V[state])  # TESTING
                # Δ := maximum(Δ, |v - V(s)|)
                change = max(change, np.abs(old_v - self.V[action['coords']]))
                print("CHANGE: ", change)  # TESTING

                # !!!!! in order to solve TIMEOUT !!!!! #
                if change < 10:
                    print("BREAK000000")  # TESTING
                    print("#######change: ", change)  # TESTING
                    break

                #idx += 1

            # when Δ gets below the error threshold Ɵ
            if change < SMALL_ENOUGH:
                print("BREAK11111")  # TESTING
                break

    ### TESTING ###
    def callFunction(self, actions, game_state, currentSelect):
        next_act = random.choice(actions)
        print("radom - next_act: ", next_act)
        return next_act