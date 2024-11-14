
from nfa_old import write_nfa, NFA, read_nfa

"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/27/2024
Purpose: NFA operations single_string, union, concat, and star
"""


def single_string_nfa(string):
    """
    creates an NFA that only accepts one string
    :param string: the string to accept
    :return: a file name for the new NFA
    """
    new_nfa = NFA()
    new_nfa.states.append('q1')
    new_nfa.states.append('q2')
    new_nfa.alphabet.append(string)
    new_nfa.start_state = 'q1'
    new_nfa.accept_states.append('q2')
    new_nfa.transitions.append({"source": 'q1', "symbol": string, "dest": 'q2'})
    return new_nfa

def union_nfa(m1, m2):
    """
    performs the union operation on two NFAs
    :param m1: NFA 1
    :param m2: NFA 2

    :return: file name for the new unioned NFA
    """
    # create new NFA
    new_nfa = NFA()
    m1_state_count = len(m1.states)
    m2_state_count = len(m2.states)
    # make new alphabet
    new_nfa.alphabet = m1.alphabet + m2.alphabet

    # set relevant m1 states and transitions to new NFA
    new_nfa.transitions = m1.transitions

    # copy over relevant states from m1
    for state in m1.states:
        new_nfa.states.append(state)
        if state in m1.accept_states:
            new_nfa.accept_states.append(state)

    # make new states and transitions for m2
    for i, state in enumerate(m2.states):
        new_nfa.states.append(f'q{i + 1 + m1_state_count}')
        if state in m2.accept_states:
            new_nfa.accept_states.append(f'q{i + 1 + m1_state_count}')

    for transition in m2.transitions:
        new_transition = {
            "source": f'q{int(transition["source"][1:]) + m1_state_count}',
            "symbol": transition["symbol"],
            "dest": f'q{int(transition["dest"][1:]) + m1_state_count}'
        }

        new_nfa.transitions.append(new_transition)

    # add new start state
    start = f'q{m1_state_count + m2_state_count + 1}'
    new_nfa.states.append(start)
    new_nfa.start_state = start
    # add new transitions per the union operation
    new_nfa.transitions.append({'source': start, 'symbol': '&', 'dest': m1.start_state})
    new_nfa.transitions.append({'source': start, 'symbol': '&', 'dest': f'q{m1_state_count + 1}'})

    return new_nfa


def concat_nfa(m1, m2):
    """
    performs the concat operation on two NFAs
    :param m1: NFA 1
    :param m2: NFA 2
    :return: file name for the new concatenated NFA
    """
    # create new NFA
    new_nfa = NFA()
    m1_state_count = len(m1.states)

    # make new alphabet
    new_nfa.alphabet = m1.alphabet + m2.alphabet

    # set relevant m1 states and transitions to new NFA
    new_nfa.start_state = m1.start_state
    new_nfa.transitions = m1.transitions

    new_nfa.states = m1.states

    # copy over relevant m2 states with new state values
    for i, state in enumerate(m2.states):
        new_nfa.states.append(f'q{i + 1 + m1_state_count}')
        if state in m2.accept_states:
            new_nfa.accept_states.append(f'q{i + 1 + m1_state_count}')
    # create new transitions with new values
    for transition in m2.transitions:
        new_transition = {
            "source": f'q{int(transition["source"][1:]) + m1_state_count}',
            "symbol": transition["symbol"],
            "dest": f'q{int(transition["dest"][1:]) + m1_state_count}'
        }

        new_nfa.transitions.append(new_transition)
        
    # add transitions between m1 and n2
    for state in m1.accept_states:
        if state not in new_nfa.accept_states:
            new_transition = {
                "source": state,
                "symbol": '&',
                "dest": f'q{int(m2.start_state[1:]) + m1_state_count}'
            }
            new_nfa.transitions.append(new_transition)

    return new_nfa


def star_nfa(m):
    """
    performs a kleene star operation on an NFA
    :param m: NFA object
    :return: file name for new kleene star NFA
    """
    new_nfa = NFA()
    m_state_count = 0

    # copy over relevant info from m
    new_nfa.alphabet = m.alphabet
    new_nfa.accept_states = m.accept_states
    new_nfa.transitions = m.transitions
    for state in m.states:
        new_nfa.states.append(state)
        m_state_count += 1

    # add the new start state and its transitions
    new_state = f'q{m_state_count+1}'
    new_nfa.states.append(new_state)
    new_nfa.start_state = new_state
    new_nfa.accept_states.append(new_state)
    for state in m.accept_states:
        new_nfa.transitions.append({'source': state, 'symbol': '&', 'dest': m.start_state})

    return new_nfa


def backref_nfa(k):
    new_nfa = NFA()
    new_nfa.states.append('q1')
    new_nfa.states.append('q2')
    new_nfa.start_state = 'q1'
    new_nfa.accept_states.append('q2')
    new_nfa.transitions.append({"source": 'q1', "symbol": f'cp{k}', "dest": 'q2'})
    return new_nfa


def group_nfa(m, i):
    """
    performs a group operation on an NFA
    :param m: NFA object
    :return: file name for new kleene star NFA
    """
    new_nfa = NFA()
    m_state_count = 0

    # copy over relevant info from m
    new_nfa.alphabet = m.alphabet
    new_nfa.transitions = m.transitions
    for state in m.states:
        new_nfa.states.append(state)
        m_state_count += 1

    # add the new start state and its transitions
    new_start = f'q{m_state_count + 1}'
    new_nfa.states.append(new_start)
    new_nfa.start_state = new_start
    new_nfa.transitions.append({'source': new_start, 'symbol': f'o{i}', 'dest': m.start_state})
    # add new accept state and transitions
    new_accept = f'q{m_state_count + 2}'
    new_nfa.states.append(new_accept)

    new_nfa.accept_states.append(new_accept)
    # close k transitions
    for state in m.accept_states:
        new_nfa.transitions.append({'source': state, 'symbol': f'c{i}', 'dest': new_accept})

    # create file

    return new_nfa