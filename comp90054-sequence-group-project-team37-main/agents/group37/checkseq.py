from template import Agent
import sys
import time
import numpy
import random
from Sequence.sequence_utils import *
from scipy.spatial import distance
from collections import defaultdict
sys.path.append('agents/group37/')

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

last_action = []


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.id = _id

    def SelectAction(self, actions, game_state):
        #print("COORDS: ", COORDS)
        #print("game_state.board.empty_coords: ", game_state.board.empty_coords)
        #print("game_state.board.plr_coords: ", game_state.board.plr_coords)
        # print("game_state.board.plr_coords['r']: ",
        #      game_state.board.plr_coords['r'])
        #print("game_state.deck.discards: ", game_state.deck.discards)
        #print("game_state.board.draft: ", game_state.board.draft)
        #print("game_state.board.chips: ", game_state.board.chips)
        #print("id: ", self.id)
        #print("actions[0]: ", actions[0])
        #print("discard: ", game_state.agents[self.id].discard)

        if game_state.board.plr_coords['r'] != []:
            # for agent in game_state.agents:
            # print(agent.colour)
            # print(game_state.agents[0].colour)
            #print("new_seq: ", game_state.board.new_seq)
            #print("last_coords: ", game_state.board.plr_coords['r'][-1])
            r, c = last_action[-1]['coords']
            print(self.checkSeq(game_state.board.chips,
                                game_state.agents[self.id], game_state.board.plr_coords['r'][-1]))

        last_action.append(actions[0])
        return actions[0]

    def checkSeq(self, chips, plr_state, last_coords):
        clr, sclr = plr_state.colour, plr_state.seq_colour
        print('clr: ', clr)
        oc, os = plr_state.opp_colour, plr_state.opp_seq_colour
        seq_type = TRADSEQ
        seq_coords = []
        seq_found = {'vr': 0, 'hz': 0, 'd1': 0, 'd2': 0, 'hb': 0}
        found = False

        def nine_chip(x, clr): return len(
            x) == 9 and len(set(x)) == 1 and clr in x
        lr, lc = last_coords

        # All joker spaces become player chips for the purposes of sequence checking.
        for r, c in COORDS['jk']:
            chips[r][c] = clr

        # First, check "heart of the board" (2h, 3h, 4h, 5h). If possessed by one team, the game is over.
        coord_list = [(4, 4), (4, 5), (5, 4), (5, 5)]
        heart_chips = [chips[y][x] for x, y in coord_list]
        print('heart_chips: ', heart_chips)
        if '_' not in heart_chips and (clr in heart_chips or sclr in heart_chips) and not (oc in heart_chips or os in heart_chips):
            print("CHECK 2")
            seq_type = HOTBSEQ
            seq_found['hb'] += 2
            seq_coords.append(coord_list)

        # Search vertical, horizontal, and both diagonals.
        vr = [(-4, 0), (-3, 0), (-2, 0), (-1, 0),
              (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        hz = [(0, -4), (0, -3), (0, -2), (0, -1),
              (0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        d1 = [(-4, -4), (-3, -3), (-2, -2), (-1, -1),
              (0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
        d2 = [(-4, 4), (-3, 3), (-2, 2), (-1, 1), (0, 0),
              (1, -1), (2, -2), (3, -3), (4, -4)]
        for seq, seq_name in [(vr, 'vr'), (hz, 'hz'), (d1, 'd1'), (d2, 'd2')]:
            print("FOR LOOPPPPPP")
            coord_list = [(r+lr, c+lc) for r, c in seq]
            # Sequences must stay on the board.
            coord_list = [i for i in coord_list if 0 <= min(i) and 9 >= max(i)]
            chip_str = ''.join([chips[r][c] for r, c in coord_list])
            # Check if there exists 4 player chips either side of new chip (counts as forming 2 sequences).
            if nine_chip(chip_str, clr):
                print("CHECK 3")
                seq_found[seq_name] += 2
                seq_coords.append(coord_list)
            # If this potential sequence doesn't overlap an established sequence, do fast check.
            if sclr not in chip_str:
                sequence_len = 0
                start_idx = 0
                for i in range(len(chip_str)):
                    if chip_str[i] == clr:
                        sequence_len += 1
                    else:
                        start_idx = i+1
                        sequence_len = 0
                    if sequence_len >= 5:
                        print("CHECK 4")
                        seq_found[seq_name] += 1
                        seq_coords.append(coord_list[start_idx:start_idx+5])
                        break
            else:  # Check for sequences of 5 player chips, with a max. 1 chip from an existing sequence.
                for pattern in [clr*5, clr*4+sclr, clr*3+sclr+clr, clr*2+sclr+clr*2, clr+sclr+clr*3, sclr+clr*4]:
                    print("--------------1")
                    for start_idx in range(5):
                        print("--------------2")
                        print('chip_str[start_idx:start_idx+5]: ',
                              chip_str[start_idx:start_idx+5])
                        print('pattern: ', pattern)
                        if chip_str[start_idx:start_idx+5] == pattern:
                            seq_found[seq_name] += 1
                            print("CHECK 5")
                            seq_coords.append(
                                coord_list[start_idx:start_idx+5])
                            found = True
                            break
                    if found:
                        break

        for r, c in COORDS['jk']:
            chips[r][c] = JOKER  # Joker spaces reset after sequence checking.

        num_seq = sum(seq_found.values())
        if num_seq > 1 and seq_type != HOTBSEQ:
            seq_type = MULTSEQ
        return ({'num_seq': num_seq, 'orientation': [k for k, v in seq_found.items() if v], 'coords': seq_coords}, seq_type) if num_seq else (None, None)