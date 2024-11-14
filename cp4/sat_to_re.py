#!/usr/bin/env python3
from helper import read_input_sat_to_re


def parse_cnf(cnf_file):
    clauses = []
    variables = set()
    with open(cnf_file, 'r') as file:
        for line in file:
            clause = []
            for literal in line.strip().split():
                var = abs(int(literal))
                variables.add(var)
                clause.append(int(literal))
            clauses.append(clause)
    return clauses, variables


def to_regexp(clauses, variables):

    # capture literal values x1, ~x1, x2 ~x2, .... xn, ~xn
    patterns = []
    for i in range(1, variables + 1):
        # (1)? for positive literal xi, (0)? for negative literal -xi
        patterns.append(f"((1)|(1))")

    # Join all variable patterns
    variable_pattern = ''.join(patterns)

    # construct the rest of the regex clauses
    all_clauses = []
    for i, clause in enumerate(clauses):
        clause_regexp = []
        # construct one clause
        for literal in clause:
            if literal > 0:
                group_num = 2 + 3*(literal-1)
            else:
                group_num = 3 + 3 * (abs(literal) - 1)
            clause_regexp.append(f"\\{group_num}")
        all_clauses.append(f"({'|'.join(clause_regexp)})")

    # merge capture groups and clause regexps
    regex = variable_pattern + ''.join(all_clauses)
    return regex


if __name__ == '__main__':
    cnf_file, regexp_file, w_file = read_input_sat_to_re()

    try:
        clauses, lits = parse_cnf(cnf_file)
    except FileNotFoundError:
        clauses, lits = parse_cnf("../" + cnf_file)

    string_w = '1' * (len(clauses) + len(lits))  # constructs a string of all 1s
    regexp = to_regexp(clauses, len(lits))

    fp_regexp = open(regexp_file, "w")
    fp_regexp.write(regexp)

    fp_w = open(w_file, "w")
    fp_w.write(string_w)

    fp_w.close()
    fp_regexp.close()

