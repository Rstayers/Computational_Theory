from nfa_old import read_nfa
from regex_parser import parse
from nfa_operations import single_string_nfa, concat_nfa, union_nfa, star_nfa
"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/27/2024
Purpose: breaks down a regex into a corresponding NFA
"""


def break_down(regex):
    result, tree = parse(regex)
    # returns order to perform operations
    ops = tree.dfs_traversal()
    ops.append(tree.value)
    curr = []
    # use curr as a stack to perform NFA operations in the correct order
    while ops:
        next_op = ops.pop(0)
        if next_op == 'concat':
            val_2 = curr.pop()
            val_1 = curr.pop()
            curr.append(concat_nfa(read_nfa(val_1), read_nfa(val_2), val_1, val_2))
        elif next_op == 'star':
            val_1 = curr.pop()
            curr.append(star_nfa(read_nfa(val_1), val_1))
        elif next_op == 'epsilon':
            curr.append(single_string_nfa(""))
        elif next_op == 'symbol':
            val_1 = curr.pop()
            curr.append(single_string_nfa(val_1))
        elif next_op == 'union':
            val_2 = curr.pop()
            val_1 = curr.pop()
            curr.append(union_nfa(read_nfa(val_1), read_nfa(val_2), val_1, val_2))
        else:
            # variable given
            curr.append(next_op)
        
    return curr[0]


