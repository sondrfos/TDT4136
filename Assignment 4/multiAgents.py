# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best


        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        oldFood = currentGameState.getFood();
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #stay away from ghosts
        i = 0
        ghostDist = [0 for j in xrange(len(newScaredTimes))]
        for ghostState in newGhostStates:
            ghostDist[i] = manhattanDistance(newPos, ghostState.configuration.pos)
            i+=1

        minGhostDist = min(ghostDist)
        for index in range(len(ghostDist)):
            if ghostDist[index] == minGhostDist:
                minIndices = index    

        if newScaredTimes[minIndices]>0:
            if minGhostDist == 0: 
                ghostScore = 1000
            elif minGhostDist < 3: 
                ghostScore = 1000/minGhostDist
            else: 
                ghostScore = 0
        else:
            if minGhostDist == 0: 
                ghostScore = 0
            elif minGhostDist < 3: 
                ghostScore = 300*minGhostDist
            else: 
                ghostScore = 1000

        #find capsules
        capsuleScore = 0
        for capsule in currentGameState.getCapsules():
            dist=manhattanDistance(capsule,newPos)
            if(dist==0): capsuleScore+=10000
            else: capsuleScore+=1000.0/dist

        #go towards food - always
        foodScore = 0;
        for x in xrange(oldFood.width):
            for y in xrange(oldFood.height):
                if(oldFood[x][y]):
                    dist=manhattanDistance((x,y),newPos)
                    if(dist==0): foodScore+=300
                    else: foodScore+=100.0/(dist*dist)
        return (ghostScore+capsuleScore+foodScore)


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        depth = 0
        
        moves = gameState.getLegalActions(0)
        maxChildValue = -float("inf")
        for move in moves:
            childValue = self.minValue(gameState.generateSuccessor(0, move), depth, 1)
            if maxChildValue < childValue:
                maxChildValue = childValue
                action = move

        return action

        util.raiseNotDefined()


    def maxValue(self, gameState, depth):
        moves = gameState.getLegalActions(0)
        if self.depth == depth or gameState.isWin() or not moves:
            return self.evaluationFunction(gameState)
        i = 0
        childValue = [0 for j in xrange(len(moves))]
        for move in moves:
            childValue[i] = self.minValue(gameState.generateSuccessor(0, move), depth, 1)
            i += 1
        return max(childValue)



    def minValue(self, gameState, depth, enemyIndex):
        moves = gameState.getLegalActions(enemyIndex)
        if gameState.isLose() or not moves:
            return self.evaluationFunction(gameState)
        i = 0
        childValue = [0 for j in xrange(len(moves))]
        if (enemyIndex == gameState.getNumAgents()-1):
            for move in moves:
                childValue[i] = self.maxValue(gameState.generateSuccessor(enemyIndex, move), depth+1)
                i+=1
        else:
            for move in moves:
                childValue[i] = self.minValue(gameState.generateSuccessor(enemyIndex, move), depth, enemyIndex+1)
                i+=1
        return min(childValue)

            



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        depth = 0
        
        moves = gameState.getLegalActions(0)
        alpha = -float("inf")
        v = -float("inf")
        beta = float("inf")
        action = 0
        for move in moves:
            v = max(v, self.minValue(gameState.generateSuccessor(0, move), depth, 1, alpha, beta))
            
            if v > beta:
            	return move
            else:
            	if alpha < v:
            		alpha = v
            		action = move

        return action

        util.raiseNotDefined()


    def maxValue(self, gameState, depth, alpha, beta):
        moves = gameState.getLegalActions(0)
        if self.depth == depth or gameState.isWin() or not moves:
            return self.evaluationFunction(gameState)
        v = -float("inf")

        for move in moves:
            v = max(v, self.minValue(gameState.generateSuccessor(0, move), depth, 1, alpha, beta))
            if v > beta:
            	return v

            alpha = max(v, alpha)

        return v



    def minValue(self, gameState, depth, enemyIndex, alpha, beta):
        moves = gameState.getLegalActions(enemyIndex)
        if gameState.isLose() or not moves:
            return self.evaluationFunction(gameState)
        v = float("inf")

        if (enemyIndex == gameState.getNumAgents()-1):
            for move in moves:
                v = min(v,self.maxValue(gameState.generateSuccessor(enemyIndex, move), depth+1, alpha, beta))
                if alpha > v:
                	return v
                beta = min(v, beta)
        else:
            for move in moves:
                v = min(v,self.minValue(gameState.generateSuccessor(enemyIndex, move), depth, enemyIndex+1, alpha, beta))
                if alpha > v:
                	return v
                beta = min(v, beta)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

