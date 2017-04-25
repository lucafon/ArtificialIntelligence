'''
Created on Mar 18, 2017

@author: Luca Fontanili
'''

import sys
import queue
import copy

rows = ['1','2','3','4','5','6','7','8','9']
cols = ['A','B','C','D','E','F','G','H','I']
default = ['1','2','3','4','5','6','7','8','9']

def create_board(arg):
    board = dict()
    count = 0
    for c in cols:
        for r in rows:
            board[c+r] = [arg[count]] if arg[count] != '0' else default
            count +=1
    return board

def initialize_constraints():
    constraints = []
    for c in cols:
        constraint = []
        for r in rows:
            constraint.append(c+r)
        constraints.append(constraint)
    for r in rows:     
        constraint = []   
        for c in cols:
            constraint.append(c+r)
        constraints.append(constraint)
    constraints.append(['A1','A2','A3','B1','B2','B3','C1','C2','C3'])
    constraints.append(['A4','A5','A6','B4','B5','B6','C4','C5','C6'])
    constraints.append(['A7','A8','A9','B7','B8','B9','C7','C8','C9'])
    constraints.append(['D1','D2','D3','E1','E2','E3','F1','F2','F3'])
    constraints.append(['D4','D5','D6','E4','E5','E6','F4','F5','F6'])
    constraints.append(['D7','D8','D9','E7','E8','E9','F7','F8','F9'])
    constraints.append(['G1','G2','G3','H1','H2','H3','I1','I2','I3'])
    constraints.append(['G4','G5','G6','H4','H5','H6','I4','I5','I6'])
    constraints.append(['G7','G8','G9','H7','H8','H9','I7','I8','I9'])
    return constraints
    
def check(arc, board, constraints):
    
    arc0 = copy.deepcopy(board[arc[0]])
    arc1 = copy.deepcopy(board[arc[1]])
    revised = False
    if len(arc1) == 1:
        if arc1[0] in arc0:
            revised = True
            arc0.remove(arc1[0])
            board[arc[0]] = arc0
    return revised

def forward_checking(board, constraints):
    q = queue.Queue()
    [q._put((k1,k2)) for k1 in board.keys() for k2 in board.keys() for c in constraints if k1 != k2 and k1 in c and k2 in c]
    while q.qsize() > 0:
        arc = q.get()
        revised = check(arc, board, constraints)
        if revised:
            if len(board[arc[0]]) == 0:
                return False
            [q._put((k,arc[0])) for k in board.keys() for c in constraints if arc[0] != k and arc[1] != k and arc[0] in c and k in c]
    return True
        
def print_results(board):
    out = ''
    solved = True
    for c in cols:
        for r in rows:
            if len(board[c+r]) == 1:
                out += str(board[c+r][0])
            else: 
                out += '0'
                solved = False
    if solved:
        print('SUDOKU SOLVED', out)
    return solved

def pr_res(board):
    out = ''
    for c in cols:
        for r in rows:
            if len(board[c+r]) == 1:
                out += str(board[c+r][0])
            else: 
                out += '0'
    return out

def backtrack(board, constraints):
    if print_results(board):
        return True, board
    remaining_values = [] 
    [remaining_values.append((k, board[k])) for k in sorted(board, key=lambda k: len(board[k]), reverse=False) if len(board[k]) > 1]
    var = remaining_values[0]
    for value in var[1]:
        b = copy.deepcopy(board)
        b[var[0]] = [value]
        fc = forward_checking(b, constraints)    
        if fc:
            result, b = backtrack(b, constraints)
            if result:
                return result, b
            b = copy.deepcopy(board)
    
    return False, b

def main(args):
    o = open('output.txt', 'w')
    if len(args) != 2:
        raise('Correct execution of the program: python3 driver.py <input_string>')
    board = create_board(args[1])
    constraints = initialize_constraints()
    if not forward_checking(board, constraints):
        raise
    result, b = backtrack(board, constraints)
    if not result:
        print('UNSOLVABLE SUDOKU')
    else:
        o.write(pr_res(b))


if __name__ == '__main__':
    main(sys.argv)