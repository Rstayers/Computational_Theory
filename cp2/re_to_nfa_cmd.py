#!/usr/bin/env python3
from helper import read_input
from re_to_nfa import break_down
"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/27/2024
Purpose: runs re_groups a regular expression
"""

input_string = read_input()

nfa = break_down(input_string + '\0')

# Open the file in read mode
with open(nfa, 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Print the line
        print(line, end='')
