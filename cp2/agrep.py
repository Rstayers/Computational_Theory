#!/usr/bin/env python3
import sys

from nfa import match, read
from re_to_nfa import break_down
from helper import read_input


def capture_stdin():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())  # Remove trailing newline character
    return lines


def agrep(regex, strings):
    # using chiang's match and read functions because mine was not O(n^2) last time
    nfa = read(open(break_down(regex)))
    for string in strings:
        result, path = match(nfa, string)
        if result:
            print(string)


input_string = read_input()

agrep(input_string + '\0',  capture_stdin())

