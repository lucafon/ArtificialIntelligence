from random import randint,random
from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):
    
    _INFINITY = 100000
    _max_depth = 8
    _alpha = -_INFINITY
    _beta = _INFINITY
    possibleNewTiles = [2, 4]
    probability = 0.9
    
    def getMove(self, grid):
        return self.decide(grid)
    
    def decide(self, grid):
        move,l = self.maximize(grid, 0)
        return move
        
    def maximize(self, grid, level):
        level += 1
        if level == self._max_depth or len(grid.getAvailableMoves()) == 0:
            return None, self._eval_state(grid)
        
        max_child = None
        max_utility = -self._INFINITY
        for child in grid.getAvailableMoves():
            g = grid.clone()
            g.move(child)
            l, utility = self.minimize(g, child, level)
            if utility > max_utility:
                max_child = child
                max_utility = utility
            if max_utility >= self._beta:
                break
            if max_utility >  self._alpha:
                self._alpha = max_utility
        return max_child, max_utility
            
            
    
    def minimize(self, grid, child, level):
        level += 1
        if level == self._max_depth or len(grid.getAvailableMoves()) == 0:
            return None, self._eval_state(grid)
        
        min_child = None
        min_utility = self._INFINITY
        for child in grid.getAvailableMoves():
            cells = grid.getAvailableCells()
            move = cells[randint(0, len(cells) - 1)] if cells else None
            if move and grid.canInsert(move):
                grid.setCellValue(move, self.getNewTileValue())
            l,utility = self.maximize(grid, level)
            if utility < min_utility:
                min_child = child
                min_utility = utility
            if min_utility <= self._alpha:
                break
            if min_utility <  self._beta:
                self._beta = min_utility
        return min_child, min_utility
    
    def getNewTileValue(self):
        if randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1];
        
    def _eval_state(self, grid):
        if len(grid.getAvailableMoves()) == 0:
            return 0
        value = 3 * grid.getMaxTile() / 2048 + 6 * len(grid.getAvailableCells()) / 16
        monotonic_row = 0
        monotonic_col = 0
        for row in grid.map:
            for col in range(len(row) -1):
                if row[col] > row[col+1]:
                    monotonic_row += 1
            if row[0] > row[3]:
                monotonic_row += 1
            if row[0] > row[2]:
                monotonic_row += 1
        
        for col in range(len(grid.map[0])-1):
            for row in range(len(grid.map[0])):
                if grid.map[col][row] > grid.map[col + 1][row]:
                    monotonic_col += 1
                    
        final_value =  2 * value + 3 *(monotonic_row/20 + monotonic_col/12)
        if grid.getMaxTile() >= 256 and grid.getMaxTile() == grid.map[0][0]:
            final_value += 1
        
        return final_value