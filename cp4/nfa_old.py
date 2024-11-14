#!/usr/bin/env python3
import sys

"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/07/2024
Purpose: All NFA logic for CP1
"""
SPECIAL_C = [f'c{i}' for i in range(1, 100)]
SPECIAL_O = [f'o{i}' for i in range(1, 100)]
SPECIAL_CP = [f'cp{i}' for i in range(1, 100)]

class NFA:
    """
    class to contain all needed NFA information
    """
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.start_state = None
        self.accept_states = []
        self.transitions = []


def construct_graph(NFA):
    """
    constructs graph given an NFA object
    :param NFA: NFA class
    :return: a transition graph
    """

    graph = {}
    for transition in NFA.transitions:
        if transition['source'] not in graph:
            graph[transition['source']] = []
        graph[transition['source']].append(transition)
    return graph


def read_input():
    """
    reads from command-line arguments to output nfa file and string input
    """
    try:
        # Check if enough arguments are provided
        if len(sys.argv) < 3:
            raise ValueError("Insufficient arguments provided. Need both NFA file and string input.")

        # Extract nfa file and string input from command-line arguments
        nfa_file = sys.argv[1]
        string_input = sys.argv[2]
    except ValueError as e:
        print(e)
        sys.exit(1)

    return nfa_file, string_input


def read_nfa(file):
    """
    reads a file and creates a corresponding NFA
    :param file: file with NFA info
    :return: NFA object
    """
    # open file and get lines
    M = NFA()
    fp = open(file)
    lines = fp.readlines()
    # input NFA class info depending on line number
    for i, line in enumerate(lines):
        line = line.split()
        if i == 0:  # Q
            for state in line:
                M.states.append(state)
        elif i == 1:  # Alphabet
            for symbol in line:
                M.alphabet.append(symbol)
        elif i == 2:  # start state
            M.start_state = line[0]
        elif i == 3:  # accept states
            for state in line:
                M.accept_states.append(state)
        else:  # transitions
            transition = {"source": line[0], "symbol": line[1], "dest": line[2]}
            M.transitions.append(transition)

    return M


def write_nfa(M, file):
    """
    uses an NFA object and writes a corresponding file
    :param M: NFA object
    :param file: file to write to
    :return: None
    """
    fp = open(file, "w")
    # write states
    fp.write(" ".join(M.states))
    fp.write("\n")
    # write alphabet
    fp.write(" ".join(M.alphabet))
    fp.write("\n")
    # write start state
    fp.write(M.start_state)
    fp.write("\n")
    # accept states
    fp.write(" ".join(M.accept_states))
    fp.write("\n")
    # transitions
    for transition in M.transitions:
        fp.write(" ".join(transition.values()))
        fp.write("\n")
    fp.close()


def match(M, w):
    """
    returns whether NFA M accepts string w
    :param M: NFA object
    :param w: string to test
    :return: tuple (accept/reject, path)
    """

    nfa_graph = construct_graph(M)

    queue = [(M.start_state, 0, [])]

    visited = set()

    # traversal graph BFS
    while queue:

        source, index, path = queue.pop(0)

        # gauntlet conditions
        if (source, index) in visited:
            continue
        if index == len(w) and source in M.accept_states:
            return True, path
        visited.add((source, index))

        # try/except is to ignore states w/o outgoing transitions
        try:
            for transition in nfa_graph[source]:
                if transition['source'] == source:
                    # get transition info
                    dest = transition['dest']
                    symbol = transition['symbol']
                    # try/except is to treat index out of bounds
                    try:
                        # add paths to queue if there is a valid outgoing condition or epsilon transition
                        if symbol == w[index] or symbol == '&':
                            # increment index only if it is not an epsilon transition
                            queue.append((dest, index + (symbol != '&'), path + [transition]))

                    except IndexError:
                        # here to test epsilon transitions if index out of bounds
                        if symbol == '&':
                            queue.append((dest, index, path + [transition]))

        except KeyError:
            pass
    return False, []


def main():
    """
    runs match on command line args
    :return: None
    """
    nfa_file, input_string = read_input()
    M = read_nfa(nfa_file)
    return match(M, input_string)
