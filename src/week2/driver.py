'''
Created on Jan 30, 2017

@author: Luca Fontanili
'''
import sys
from abc import abstractmethod
import math
import copy
import Queue as queue
from heapq import heappush,heappop
import time
import resource

strategies = {'bfs': 0, 'dfs': 1, 'ast': 2, 'ida' : 3}
UDLR_moves = ['Up', 'Down', 'Left', 'Right']
id_count = 1

class State:
    
    def __init__(self, state, level = 0, move = '', identifier = 0, previous = None):
        self._state = state
        self._level = level
        self._move = move
        self._id = identifier
        self._previous = previous
        
    def state(self):
        return self._state
    
    def set_state(self,state):
        self._state = state
    
    def level(self):
        return self._level
    
    def set_level(self, level):
        self._level = level
    
    def moves(self):
        return self._move
    
    def set_move(self, move):
        self._move = move
        
    def id(self):
        return self._id
    
    def set_id(self, identifier):
        self._id = identifier
    
    def previous(self):
        return self._previous
    
    def set_previous(self, previous):
        self._previous = previous
    
    def to_string(self):
        return 'state=' + str(self.state()) + ' level=' + str(self.level()) + ' moves=' + str(self.moves()) + ' id=' + str(self.id()) + ' previous=' + str(self.previous().to_string()) if self.previous() is not None else ''
    
    def __eq__(self,other):
        return self.state() == other.state()
    def __hash__(self):
        return hash(tuple(self.state()))
        

class Strategy(object):
    
    @abstractmethod
    def execute(self, state):
        pass
    
    @abstractmethod
    def _generate_child_states(self, state):
        pass
    
    @staticmethod
    @abstractmethod
    def execute_strategy(state):
        pass
    
    def _check_final_state(self, state):
        final_state = []
        for i in range(len(state.state())):
            final_state.append(str(i))
        return final_state == state.state() 
    
    @staticmethod
    def _switch_move(UDLR, child, idx, size, state):
        if UDLR == 'Up':  
            if idx >= size:
                child.state()[idx], child.state()[idx-size] = child.state()[idx-size], '0'
                return child
        elif UDLR == 'Down':
            if idx + size < len(state.state()):
                child.state()[idx], child.state()[idx+size] = child.state()[idx+size], '0'
                return child
        elif UDLR == 'Left':
            if idx % size != 0:
                child.state()[idx], child.state()[idx-1] = child.state()[idx-1], '0'
                return child
        elif UDLR == 'Right':
            if (idx + 1) % size != 0:
                child.state()[idx], child.state()[idx+1] = child.state()[idx+1], '0'
                return child
        else:
            raise ValueError('Invalid move!')
        return state
    
    def _swap(self, state, UDLR):
        global id_count
        size = int(math.sqrt(len(state.state())))
        child = copy.deepcopy(state)
        idx = child.state().index('0')
        child.set_level(state.level()+1)
        child.set_previous(state)
        child.set_id(id_count)
        id_count += 1
        child.set_move(UDLR)
        return self._switch_move(UDLR, child, idx, size, state)
    
    @staticmethod
    def _compute_distance(child_state):
        final_state = []
        for i in range(len(child_state.state())):
            final_state.append(str(i))
        dist = 0
        for i in final_state:
            idx = child_state.state().index(i)
            dist += math.fabs(int(idx/math.sqrt(len(child_state.state()))) - int(final_state.index(i)/math.sqrt(len(child_state.state())))) + math.fabs(final_state.index(i)%math.sqrt(len(child_state.state())) - idx%math.sqrt(len(child_state.state())))
        return dist
    
class BFS(Strategy):
    
    def execute(self, state):
        return self.execute_strategy(state)
    
    def execute_strategy(self, initial_state):
        all_states = set()
        q = queue.Queue()
        state = State(initial_state, 0, '')
        all_states.add(state)
        q._put(state)
        end = False
        expanded_nodes = 0
        max_queue_size = 0
        max_depth = 0
        final_state = None
        while end is False:
            final_state = q._get()
            (end,max_d) = self._step(final_state, all_states, q)
            if q.qsize() > max_queue_size:
                max_queue_size = q.qsize()
            if end is False:
                expanded_nodes += 1
                if max_d > max_depth:
                    max_depth = max_d
        
        moves = []
        current = copy.deepcopy(final_state)
        while current.previous() is not None:
            moves.append(current.moves())
            current = current.previous()
        return final_state, expanded_nodes, q.qsize(), max_queue_size, max_depth, moves[::-1]
        
    def _generate_child_states(self, state):
        children = []
        [children.append(self._swap(state, move)) for move in UDLR_moves if self._swap(state, move) is not state]
        return children
    
    
    
    def _step(self, state, all_states, q):        
        if(self._check_final_state(state)):
            return True, None
        else:
            max_depth = 0
            children = self._generate_child_states(state)
            [q._put(child_state) for child_state in children if State(child_state.state()) not in all_states]
            [all_states.add(State(child_state.state())) for child_state in children if State(child_state.state()) not in all_states]
            for child in children:
                if child.level() > max_depth:
                    max_depth = child.level()
            return False, max_depth
    
class DFS(Strategy):
    
    def execute(self, state):
        return self.execute_strategy(state)
    
    def execute_strategy(self, initial_state):
        all_states = set()
        state = State(initial_state)
        all_states.add(state)
        explored = []
        mo = []
        explored.append(state)
        expanded_nodes = 0
        max_size = 0
        max_depth = 0
        current_level = 0
        final_state = None
        end = False
        while end is False:
            final_state = explored.pop()
            if final_state.level() > current_level:
                mo.append(final_state.moves())
                current_level = final_state.level()
            elif current_level > 0:
                mo = mo[0:final_state.level() -1]
                mo.append(final_state.moves())
            (end,max_d) = self._step(final_state, all_states, explored)
            if len(explored) > max_size:
                max_size = len(explored)
            if end is False:
                expanded_nodes += 1
                if max_d > max_depth:
                    max_depth = max_d
                            
        return final_state, expanded_nodes, len(explored), max_size, max_depth, mo        
        
    def _generate_child_states(self, state):
        children = []
        [children.append(self._swap(state, move)) for move in UDLR_moves[::-1] if self._swap(state, move) is not state]
        return children
    
    def _step(self, state, all_states, explored):        
        if(self._check_final_state(state)):
            return True, None
        else:
            max_depth = 0
            excluded = []
            children = self._generate_child_states(state)
            [explored.append(child_state) for child_state in children if State(child_state.state()) not in all_states]
            [excluded.append(child_state) for child_state in children if State(child_state.state()) in all_states]
            [all_states.add(State(child_state.state())) for child_state in children if State(child_state.state()) not in all_states]
            for child in children:
                if child not in excluded and child.level() > max_depth:
                    max_depth = child.level()
            return False, max_depth
        
    def _swap(self, state, UDLR):
        size = int(math.sqrt(len(state.state())))
        child = copy.deepcopy(state)
        idx = child.state().index('0')
        child.set_level(state.level()+1)
        child.set_move(UDLR)
        return self._switch_move(UDLR, child, idx, size, state)
    
class AST(Strategy):
    
    def execute(self, state):
        return self.execute_strategy(state)
    
    def execute_strategy(self, initial_state):
        all_states = set()
        h = []
        state = State(initial_state, 0, '')
        all_states.add(state)
        heappush(h, (0, state))
        end = False
        expanded_nodes = 0
        max_queue_size = 0
        max_depth = 0
        final_state = None
        while end is False:
            ord, final_state = heappop(h)
            (end,max_d) = self._step(final_state, all_states, h)
            if len(h) > max_queue_size:
                max_queue_size = len(h)
            if end is False:
                expanded_nodes += 1
                if max_d > max_depth:
                    max_depth = max_d
                    
        moves = []
        current = copy.deepcopy(final_state)
        while current.previous() is not None:
            moves.append(current.moves())
            current = current.previous()
        return final_state, expanded_nodes, len(h), max_queue_size, max_depth, moves[::-1]
        
    def _generate_child_states(self, state):
        children = []
        [children.append(self._swap(state, move)) for move in UDLR_moves if self._swap(state, move) is not state]
        return children
    
    def _step(self, state, all_states, h):        
        if(self._check_final_state(state)):
            return True, None
        else:
            max_depth = 0
            children = self._generate_child_states(state)
            [heappush(h, (self._compute_distance(child_state),child_state)) for child_state in children if State(child_state.state()) not in all_states]
            [all_states.add(State(child_state.state())) for child_state in children if State(child_state.state()) not in all_states]
            for child in children:
                if child.level() > max_depth:
                    max_depth = child.level()
            return False, max_depth
    
class IDA(Strategy):
    
    def execute(self, state):
        return self.execute_strategy(state)
    
    def execute_strategy(self, initial_state):
        current_max_depth = 1
        end = False
        while end is False:
            expanded_nodes = 0
            max_queue_size = 0
            all_states = set()
            h = []
            state = State(initial_state, 0, '')
            all_states.add(State(state.state()))
            heappush(h, (0, state))
            final_state = None
            while end is False:
                if len(h) == 0:
                    current_max_depth += 1
                    break
                ord, final_state = heappop(h)
                end = self._step(final_state, all_states, h, current_max_depth)
                if len(h) > max_queue_size:
                    max_queue_size = len(h)
                if end is False:
                    expanded_nodes += 1
        moves = []
        current = copy.deepcopy(final_state)
        while current.previous() is not None:
            moves.append(current.moves())
            current = current.previous()
        return final_state, expanded_nodes, len(h), max_queue_size, current_max_depth, moves[::-1]  
        
    def _generate_child_states(self, state):
        children = []
        [children.append(self._swap(state, move)) for move in UDLR_moves if self._swap(state, move) is not state]
        return children
    
    
    def _step(self, state, all_states, h, current_max_depth):      
        if(state.level() > current_max_depth):
            return False  
        if(self._check_final_state(state)):
            return True
        else:
            children = self._generate_child_states(state)
            [heappush(h, (self._compute_distance(child_state),child_state)) for child_state in children if State(child_state.state()) not in all_states and child_state.level() <= current_max_depth]
            [all_states.add(State(child_state.state())) for child_state in children if State(child_state.state()) not in all_states and child_state.level() <= current_max_depth]
            return False     

class StrategyClass:
    _strategy_map = {}
    
    def __init__(self):
        self.__init_map()
        
    def __init_map(self):
        self._strategy_map[strategies['bfs']] = BFS()
        self._strategy_map[strategies['dfs']] = DFS()
        self._strategy_map[strategies['ast']] = AST()
        self._strategy_map[strategies['ida']] = IDA()
        
    def execute(self, state, strategy):
        return self._strategy_map[strategies[strategy]].execute(state.split(','))

def _print_stats(final_state, expanded_nodes, fringe_size, max_queue_size, running_time, max_depth, moves):
   
    f = open('output.txt', 'w')
    f.write('path_to_goal: ' + str(moves) + "\n")
    f.write('cost_of_path: ' + str(len(moves)) + "\n")
    f.write('nodes_expanded: ' + str(expanded_nodes) + "\n")
    f.write('fringe_size: ' + str(fringe_size) + "\n")
    f.write('max_fringe_size: ' + str(max_queue_size) + "\n")
    f.write('search_depth: ' + str(final_state.level()) + "\n")
    f.write('max_search_depth: ' + str(max_depth) + "\n")
    f.write('running_time: ' + str(running_time) + "\n")
    f.write('max_ram_usage: ' + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000))

def run(args):
    if len(args) != 3:
        raise ValueError('Bad argument list')
    start_time = time.time()
    strategy = StrategyClass()
    (final_state, expanded_nodes, fringe_size, max_size, max_depth, moves) = strategy.execute(args[2], args[1])
    end_time = time.time()
    _print_stats(final_state, expanded_nodes, fringe_size, max_size, end_time - start_time, max_depth, moves)
    

if __name__ == '__main__':
    run(sys.argv)