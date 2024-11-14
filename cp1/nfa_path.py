#!/usr/bin/env python3


from nfa import main
"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/07/2024
Purpose: runs nfa testing on input string
"""
flag, path = main()
if flag:
    print("accept")
else:
    print("reject")
for step in path:
    for i, item in enumerate(step.values()):
        if i == len(step) - 1:
            print(item, end='')
        else:
            print(item, end=' ')
    print()
