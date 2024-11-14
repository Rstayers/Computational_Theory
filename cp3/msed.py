#!/usr/bin/env python3
import sys

from helper import read_input_msed, get_matches, read_cmd_file
from re_to_nfa import break_down
from nfa import match, read 

"""
Author: Rex Stayer-Suprick
Course: Theory of Computing CP3
Date: 02/27/2024
Purpose: runs msed
"""


def extract_k(s):
    # function that gets group number k and any characters after for /g<k>
    index_k = 2
    group = ''
    after = ''
    # Make sure index_k is within the string bounds
    while s[index_k] != '>':
        group += s[index_k]
        index_k += 1
    index_k += 1
    while index_k < len(s):

        after += s[index_k]
        index_k += 1
    return group, after


def capture_stdin():
    lines = []
    for line in sys.stdin:
         
        yield line.strip() # Remove trailing newline character


# gets the list of commands and strings to test them on
cmds, strings, read_from_stdin = read_input_msed()

if read_from_stdin:
    strings = capture_stdin()

i = 0
labels = {} # keep track of labels
cmds = sum(cmds, []) if any(isinstance(i, list) for i in cmds) else cmds # flattens it if its 2D
accepted = False

# loop through all strings and execute the commands
for string in strings:
    string = string
    i = 0  # line tracker
    for command in cmds:
        if command['type'] == 'label':
            labels[command['label']] = command['line']
    # using TM instead of expression
    try:
        labels['qaccept']
        string = '[q1]' + string + '_______________________'
    except KeyError:
        pass

    while i < len(cmds):
        command = cmds[i]
        # get command type and line number
        _type, line = command['type'], command['line']
        if _type == 'replace':
            # if s/ command, see if it passes and replace accordingly

            nfa = read(open(break_down(command['regexp'] + '\0')))
            result,path = match(nfa, string)

            if result:

                if len(command['backreferences']) == 0: # case of pure replacement
                    string = command['replacement']
                else:
                    new_string = ''

                    matches = get_matches(path)
                    matches_dict = {str(match[0]): match[1] for match in matches}
                    # Process each backreference
                    for backref in command['backreferences']:
                        before, group_num = backref.split('\\', 1)
                        if group_num.startswith('g<'):
                            k, after = extract_k(group_num)
                            new_string += before + matches_dict.get(k, '')
                            new_string += after
                        else:
                            new_string += before + matches_dict.get(group_num, '')

                    string = new_string

        elif _type == 'branch':  # branch command
            
            nfa = read(open(break_down(command['regexp'] + '\0'))) # test if string passes and branch if it does
            result, path = match(nfa, string)

            if result:
                i = labels[command['label']]
        i += 1

    # print depend on whether we are simulating a TM
    try:
        is_tm = labels['qaccept']
        if string.startswith('reject') or '[qreject]' in string:
            print("reject")
        else:
            print(f"accept:{string}")
    except KeyError:
        print(string)
