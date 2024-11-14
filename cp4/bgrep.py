#!/usr/bin/env python3
import sys

from nfa_old import write_nfa
from nfa import match, read
from re_to_nfa import break_down
from helper import read_input


def capture_stdin():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())  # Remove trailing newline character
    return lines


def bgrep(regex, strings):
    # using chiang's match and read functions because mine was not O(n^2) last time
    # need to do some manipulation to change from my nfa interface to chiangs
    nfa = break_down(input_string + '\0')
    write_nfa(nfa, 'n.nfa')
    nfa = read(open('n.nfa'))

    def construct_w(string, clauses):
        output_string = ""

        for key, value in string.items():
            output_string += str(int(string[key]))

        for clause in clauses:
            for literal in clause:
                output_string += str(int(string[abs(literal)]))
        return output_string

    for string in strings:
        result, path = match(nfa, string)
        if result:
            print(string)
        

input_string = read_input()

bgrep(input_string + '\0', capture_stdin())

