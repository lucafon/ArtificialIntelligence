from random import randint,random
from BaseAI_3 import BaseAI


max_depth = 2
vecIndex = {0: 'UP', 1: 'DOWN', 2: 'LEFT', 3: 'RIGHT'}

class PlayerAI(BaseAI):
    
    possibleNewTiles = [2, 4]
    probability = 0.9
    
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        
#         tileValue = self.getNewTileValue()
#         cells = grid.getAvailableCells()
#         cell = cells[randint(0, len(cells) - 1)]
#         cl.insertTile(cell, tileValue)
#         print(cl.move(1))
#         print(cl.getAvailableMoves())
        print()
        heuristic_move = self.maximize(moves, grid.clone())
        if heuristic_move is not None:
            return heuristic_move
        if 1 in moves:
            return 1
        if 3 in moves:
            return 3
        return moves[randint(0, len(moves) - 1)] if moves else None
#     
#     def getNewTileValue(self):
#         if randint(0,99) < 100 * 0.9:
#             return possibleNewTiles[0]
#         else:
#             return possibleNewTiles[1];

#         {level: {(p,a,t,h):[state1, state2]}}
        
    def maximize(self, moves, grid):
        g = grid.clone()
        children = {}
        level = 0
        for i in moves:
            g.move(i)
            children[level] = children.get(level,[])
            children[level].append(State(g, i, level, None))
            g = grid.clone()
        level += 1
        while level < max_depth:
            for c in children.get(level -1, []):
                current_grid = c._grid.clone()
                cells = current_grid.getAvailableCells()
                
                move = cells[randint(0, len(cells) - 1)] if cells else None
                if move and current_grid.canInsert(move):
                    current_grid.setCellValue(move, self.getNewTileValue())
                
                moves = current_grid.getAvailableMoves()
                for i in moves:
                    current_grid.move(i)
                    children[level] = children.get(level,[])
                    children[level].append(State(current_grid, i, level, c._move))
                    current_grid = c._grid.clone()
            level += 1
        for l,ch in children.items():
            for c in ch:
                print(c.to_string())
                
    def getNewTileValue(self):
        if randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1];

class State:
    
    def _compute_value(self):
        if self._grid.getAvailableMoves() is []:
            return 0
        return self._grid.getMaxTile()
        
    
    def __init__(self, grid, move, level, previous_move):
        self._grid = grid
        self._move = vecIndex[move]
        self._level = level
        self._value = self._compute_value()
        self._previous = previous_move
        
    def to_string(self):
        return 'move: ' + str(self._move) + ' level: ' + str(self._level) + ' map: ' + str(self._grid.map) + ' maxTile: ' + str(self._grid.getMaxTile()) + ' previous: ' + str(self._previous) + ' value: ' + str(self._value)