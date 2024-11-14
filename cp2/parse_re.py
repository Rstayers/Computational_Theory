#!/usr/bin/env python3
from helper import read_input
from regex_parser import parse

"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/27/2024
Purpose: runs regex testing on input string
"""


input_string = read_input()

result, tree = parse(input_string + '\0')

if result:
    print(result)
else:
    print("reject")

