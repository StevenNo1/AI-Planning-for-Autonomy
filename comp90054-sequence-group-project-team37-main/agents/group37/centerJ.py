import random
from collections import defaultdict


from template import Agent
import sys
import math


sys.path.append('agents/team37/')

COORDS = {'jk': [(0, 0), (0, 9), (9, 0), (9, 9)], '2s': [(0, 1), (8, 6)], '3s': [(0, 2), (8, 5)],
          '4s': [(0, 3), (8, 4)], '5s': [(0, 4), (8, 3)], '6s': [(0, 5), (8, 2)], '7s': [(0, 6), (8, 1)],
          '8s': [(0, 7), (7, 1)], '9s': [(0, 8), (6, 1)], '6c': [(1, 0), (3, 2)], '5c': [(1, 1), (3, 3)],
          '4c': [(1, 2), (3, 4)], '3c': [(1, 3), (3, 5)], '2c': [(1, 4), (3, 6)], 'ah': [(1, 5), (4, 6)],
          'kh': [(1, 6), (5, 6)], 'qh': [(1, 7), (6, 6)], 'th': [(1, 8), (6, 5)], 'ts': [(1, 9), (5, 1)],
          '7c': [(2, 0), (4, 2)], 'as': [(2, 1), (4, 9)], '2d': [(2, 2), (5, 9)], '3d': [(2, 3), (6, 9)],
          '4d': [(2, 4), (7, 9)], '5d': [(2, 5), (8, 9)], '6d': [(2, 6), (9, 8)], '7d': [(2, 7), (9, 7)],
          '9h': [(2, 8), (6, 4)], 'qs': [(2, 9), (4, 1)], '8c': [(3, 0), (5, 2)], 'ks': [(3, 1), (3, 9)],
          '8d': [(3, 7), (9, 6)], '8h': [(3, 8), (6, 3)], '9c': [(4, 0), (6, 2)], '6h': [(4, 3), (5, 8)],
          '5h': [(4, 4), (6, 8)], '4h': [(4, 5), (7, 8)], '9d': [(4, 7), (9, 5)], '7h': [(4, 8), (5, 3)],
          'tc': [(5, 0), (7, 2)], '2h': [(5, 4), (8, 7)], '3h': [(5, 5), (8, 8)], 'td': [(5, 7), (9, 4)],
          'qc': [(6, 0), (7, 3)], 'qd': [(6, 7), (9, 3)], 'kc': [(7, 0), (7, 4)], 'ac': [(7, 5), (8, 0)],
          'ad': [(7, 6), (9, 1)], 'kd': [(7, 7), (9, 2)]}

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


class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.colour = self.find_colour()
        self.opponent_colour = self.find_opponent_colour()
        self.hand = []

    def SelectAction(self, actions, game_state):
        global COORDS
        print('actions : ', actions)
        self.hand = self.find_hands(game_state)

        random_draft = random.choice(game_state.board.draft)
        # print("random:", random_draft)

        if actions[0]['type'] == 'trade':
            action = random.choice(actions)
            return action

        cores = [(5, 4), (5, 5), (4, 4), (4, 5)]
        # 搶中心
        for core in cores:
            if core in game_state.board.empty_coords:
                for card in self.hand:
                    if card in ['jc', 'jd']:
                        return {'play_card': card, 'draft_card': random_draft, 'type': 'place', 'coords': core}
        # 去中心
        for core in cores:
            if core in game_state.board.plr_coords[self.opponent_colour]:
                for card in self.hand:
                    if card in ['js', 'jh']:
                        return {'play_card': card, 'draft_card': random_draft, 'type': 'remove',
                                'coords': core}  # 是remove吧？

        # 手上有雙眼J 但 中心都滿了 或
        # 手上沒雙眼J 且 手上沒單眼J 或
        # 手上只有單眼J但中心剛好也沒人 就會往下進行
        # 先把J 扣在手上，留著以後用 -> 決定除了J牌要出哪張
        filter_hand = []
        j_in_hand = []
        has_J = False
        for card in self.hand:
            if card not in ['jc', 'jd', 'js', 'jh']:
                filter_hand.append(card)
            else:
                j_in_hand.append(card)
                has_J = True

        # 檢查這回合可能的最多12個座標，是否通通被佔據 -> dead card
        # candidate_coords = []
        # for card in filter_hand:
        #     for r, c in COORDS[card]:
        #         candidate_coords.append((r, c))  # 每次加兩個座標

        # live, dead, is_dead = self.check_dead_card(candidate_coords, game_state.board.empty_coords)


        # if is_dead:
        #     if has_J:
        #         card = j_in_hand[0]
        #         if card['type'] == 'place':  # 雙眼J
        #             # print("---use J with 2 eye")
        #             empty_coords = game_state.board.empty_coords
        #             action = {'play_card': card, 'draft_card': random_draft, 'type': 'place',
        #                       'coords': empty_coords[len(empty_coords) / 2]}
        #             return action
        #         else:  # 單眼J
        #             # print("---use J with 1 eye")
        #             opp_coords = game_state.board.plr_coords[self.opponent_colour]
        #             action = {'play_card': card, 'draft_card': random_draft, 'type': 'remove',
        #                       'coords': opp_coords[len(opp_coords) / 2]}
        #             return action
        #     else:
        #         # print("---dead and have to trade")
        #         card = filter_hand[0]
        #         action = {'play_card': card, 'draft_card': random_draft, 'type': 'trade',
        #                   'coords': COORDS[random_draft][0]}  # 應該是這樣？

                # return action
        else:  # 扣住J 打其他牌
            action = self.closest_heart_action(actions)
            return action

    def find_colour(self):
        if self.id == 0 or self.id == 2:
            return 'r'
        else:
            return 'b'

    def find_opponent_colour(self):
        if self.colour == 'r':
            return 'b'
        else:
            return 'r'

    def find_hands(self, game_state):
        for agent in game_state.agents:
            if agent.id == self.id:
                return agent.hand

    def check_dead_card(self, candidate_coords, empty_board):
        live_coords = []
        dead_coords = []
        is_dead = False
        for coord in candidate_coords:
            if coord in empty_board:
                live_coords.append(coord)
            else:
                dead_coords.append(coord)

        if len(dead_coords) == len(candidate_coords):
            is_dead = True

        return live_coords, dead_coords, is_dead

    def closest_heart_action(self, actions):
        min_dist = 150
        closest_action = {}
        for action in actions:
            dist = math.dist(list(action['coords']), [4.5, 4.5])
            if dist < min_dist:
                min_dist = dist
                closest_action = action
                print("update closet", action)
                print("update closet", dist)
        return closest_action