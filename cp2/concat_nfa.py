#!/usr/bin/env python3
from helper import read_input_union
from nfa_old import read_nfa
from nfa_operations import concat_nfa

"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/27/2024
Purpose: runs concat_nfa on two nfa's
"""

n1, n2 = read_input_union()

m1 = read_nfa(n1)
m2 = read_nfa(n2)

n3 = concat_nfa(m1, m2, n1, n2)

# Open the file in read mode
with open(n3, 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Print the line
        print(line, end='')


