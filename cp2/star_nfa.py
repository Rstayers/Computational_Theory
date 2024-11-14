#!/usr/bin/env python3
from helper import read_input
from nfa_operations import star_nfa
from nfa_old import read_nfa
"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/27/2024
Purpose: runs star_nfa on input string
"""


input_string = read_input()
n1 = read_nfa(input_string)
m1 = star_nfa(n1, input_string)

# Open the file in read mode
with open(m1, 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Print the line
        print(line, end='')


