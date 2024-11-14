from helper import hash_string
from nfa_old import write_nfa, NFA

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
    nfa_file_name = string + ".nfa"
    # Define states
    states = ""
    # Define input symbols
    symbols = set()
    i = 1
    # add states and alphabet
    for char in string:
        states += f'q{i}' + " "
        symbols.add(char)
        i += 1

    states += f'q{i}' + " "
    states = states.strip()
    symbols = " ".join(symbols)

    # Define start state
    start_state = "q1"

    # Define accept state
    accept_state = states[-2:]

    # Write to the NFA file
    with open(nfa_file_name, "w") as nfa_file:
        # Write header
        nfa_file.write(states + "\n")
        nfa_file.write(symbols + "\n")
        nfa_file.write(start_state + "\n")
        nfa_file.write(accept_state + "\n")

        # Write transitions
        for i, char in enumerate(string):
            transition_line = f"q{i+1} {char} q{i+2}\n"
            nfa_file.write(transition_line)
        transition = f'{accept_state} & {accept_state}\n'
        nfa_file.write(transition)
        return nfa_file_name


def union_nfa(m1, m2, n1, n2):
    """
    performs the union operation on two NFAs
    :param m1: NFA 1
    :param m2: NFA 2
    :param n1: file_name for NFA 1
    :param n2: file_name for NFA 1
    :return: file name for the new unioned NFA
    """
    # create new NFA
    new_nfa = NFA()
    m1_state_count = len(m1.states)
    m2_state_count = len(m2.states)
    # make new alphabet
    new_nfa.alphabet = set(m1.alphabet + m2.alphabet)

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

    # create new file
    last_slash_index = n1.rfind('/')
    n1 = n1[last_slash_index + 1:]
    last_slash_index_2 = n2.rfind('/')
    n2 = n2[last_slash_index_2 + 1:]
    f_name = hash_string(f"{n1}_{n2}")
    write_nfa(new_nfa, f_name)
    return f_name


def concat_nfa(m1, m2, n1, n2):
    """
    performs the concat operation on two NFAs
    :param m1: NFA 1
    :param m2: NFA 2
    :param n1: file_name for NFA 1
    :param n2: file_name for NFA 1
    :return: file name for the new concatenated NFA
    """
    # create new NFA
    new_nfa = NFA()
    m1_state_count = len(m1.states)

    # make new alphabet
    new_nfa.alphabet = set(m1.alphabet + m2.alphabet)

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

    # create file
    last_slash_index = n1.rfind('/')
    n1 = n1[last_slash_index + 1:]
    last_slash_index_2 = n2.rfind('/')
    n2 = n2[last_slash_index_2 + 1:]
    f_name = hash_string(f"{n1}{n2}")
    write_nfa(new_nfa, f_name)
    return f_name


def star_nfa(m, n1):
    """
    performs a kleene star operation on an NFA
    :param m: NFA object
    :param n1: name of file
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

    # create file
    f_name = hash_string(f"{n1.removesuffix('.nfa')}_star.nfa")
    write_nfa(new_nfa, f_name)
    return f_name