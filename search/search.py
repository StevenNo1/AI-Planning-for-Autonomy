# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    mystack = util.Stack()
    startNode = (problem.getStartState(), '', 0, [])
    mystack.push(startNode)
    visited = set()
    while mystack :
        node = mystack.pop()
        state, action, cost, path = node
        if state not in visited :
            visited.add(state)
            if problem.isGoalState(state) :
                path = path + [(state, action)]
                break;
                #continue
                #return
            succNodes = problem.expand(state)
            for succNode in succNodes :
                succState, succAction, succCost = succNode
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                mystack.push(newNode)
    actions = [action[1] for action in path]
    del actions[0]
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    
    #method 2:
    myQueue = util.Queue()
    #visited = []
    visited = set()
    startNode = (problem.getStartState(), '', 0, [])
    myQueue.push(startNode)
    while not myQueue.isEmpty():
        node = myQueue.pop()
        state, action, cost, path = node
        if state not in visited :
            visited.add(state)
            if problem.isGoalState(state) :
                path = path + [(state, action)]
                break
            succNodes = problem.expand(state)
            for succNode in succNodes :
                succState, succAction, succCost = succNode
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                myQueue.push(newNode)
    actions = [action[1] for action in path]
    del actions[0]
    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    #COMP90054 Task 1, Implement your A Star search algorithm here
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    
    myQueue = util.PriorityQueue()
    actions = []
    myQueue.push((problem.getStartState(),actions),0)
    #myQueue.push((problem.getStartState(),actions))
    visited = []
    succActions = []
    while myQueue:
        state,actions = myQueue.pop()
        if problem.isGoalState(state):
            break
        if state not in visited:
            visited.append(state)
            #print(state)
            successors = problem.expand(state)
            for successor, action, cost in successors:
                succActions = actions + [action]
                succCost = problem.getCostOfActionSequence(succActions) + heuristic(successor,problem)
                if successor not in visited and heuristic(successor,problem) < float("inf"):
                    myQueue.push((successor,succActions),succCost)
    print(actions)
    return actions
    
        

import searchAgents
def recursivebfs(problem, heuristic=nullHeuristic) :
#def recursivebfs(problem, heuristic = manhattanHeuristic):
    #COMP90054 Task 2, Implement your Recursive Best First Search algorithm here
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    
    a = RBFS(problem, (problem.getStartState(), [], 0,0), float("inf"), heuristic)
    return a[0]

    
    #method 7:
def RBFS(problem, node, f_limit, heuristic):
    state, actions, cost, n_f = node
    if problem.isGoalState(state):
        return actions,0
    successors = []
    
    for successor in problem.expand(state):
        succState, action, succCost = successor
        succActions = actions + [action]
        succCost = problem.getCostOfActionSequence(succActions)
        #succCost = max(s_g + heuristic(succState, problem), cost)
        newNode = [succState, succActions, succCost]
        successors.append(newNode)
    if successors == []:
        return "failure", float("inf"),f_limit
    for successor in successors:
        succState, action, succCost = successor
        #s_f = max(succCost + heuristic(succState, problem), cost)
        s_f = max(succCost + heuristic(succState, problem), n_f)
        successor.append(s_f)
    #print("successors:{}".format(successors))
    while True:
        successors.sort(key=lambda x: x[3])
        #print("successors2:{}".format(successors))
        best = successors[0]
        #print("best:{}".format(best))
        #alternative = successors[1][3]
        if best[3]> f_limit:
            #f_limit = best[2]
            return "failure", best[3]
        #print("f_limit:{}".format(f_limit))
        alternative = successors[1][3]
        #print("alt:{}".format(alternative))
        result, best[3] = RBFS(problem, best, min(f_limit, alternative), heuristic)
        
        
        if result != "failure":
            
            return result,0
        #break
    
    #print(succNodes)
    #print(problem.expand(problem.getStartState()))
    #print(problem.getStartState())
    #print(heuristic(problem.getStartState()))

    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
rebfs = recursivebfs
