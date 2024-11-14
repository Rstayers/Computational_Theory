import collections
import copy

EPSILON = '&'
SPECIAL_C = [f'c{i}' for i in range(1, 100)]
SPECIAL_O = [f'o{i}' for i in range(1, 100)]
SPECIAL_CP = [f'cp{i}' for i in range(1, 100)]
class Transition(object):
    def __init__(self, q, a, r):
        self.q = q
        self.a = a
        self.r = r

def convert_dict_to_tuple(d):
    return tuple((key, tuple(value) if isinstance(value, list) else value) for key, value in sorted(d.items()))
class NFA(object):
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.start = None
        self.accept = set()
        self.transitions = {}

    def add_state(self, q):
        self.states.add(q)

    def add_symbol(self, a):
        self.alphabet.add(a)

    def set_start(self, q):
        self.add_state(q)
        self.start = q

    def add_accept(self, q):
        self.add_state(q)
        self.accept.add(q)

    def add_transition(self, t):
        self.add_state(t.q)
        if t.a != EPSILON and t.a not in SPECIAL_O and t.a not in SPECIAL_C and t.a not in SPECIAL_CP:
            self.add_symbol(t.a)
        self.add_state(t.r)
        self.transitions.setdefault(t.q, {}).setdefault(t.a, []).append(t)


def read(file):
    """Read a NFA from a file."""
    m = NFA()
    for q in next(file).split():
        m.add_state(q)
    for a in next(file).split():
        m.add_symbol(a)
    m.set_start(next(file).rstrip())
    for q in next(file).split():
        m.add_accept(q)
    for line in file:
        q, a, r = line.split()
        m.add_transition(Transition(q, a, r))
    return m


def write(m, file):
    """Write a NFA to a file."""
    file.write(' '.join(map(str, m.states)) + '\n')
    file.write(' '.join(map(str, m.alphabet)) + '\n')
    file.write(str(m.start) + '\n')
    file.write(' '.join(map(str, m.accept)) + '\n')
    for q in m.transitions:
        for a in m.transitions[q]:
            for t in m.transitions[q][a]:
                file.write("{} {} {}\n".format(t.q, t.a, t.r))


def _transitions(m, w, q, i, groups):
    """Helper function for match_dfs and match_bfs.

    If NFA m is in state q and reading string w at position i,
    iterates over possible transitions and new positions."""

    for t in m.transitions.get(q, {}).get(EPSILON, []):
        n_g = copy.deepcopy(groups)
        yield t, i, n_g
    # Handle special operations that act like epsilon transitions
    for special_op in SPECIAL_O + SPECIAL_C:

        group_num = special_op[1:]
        for t in m.transitions.get(q, {}).get(special_op, []):
            new_g = copy.deepcopy(groups)
            if special_op in SPECIAL_O:
                new_g[group_num] = [i, '_']
            elif special_op in SPECIAL_C:
                old = new_g[group_num]
                new_g[group_num] = [old[0], i]

            yield t, i, new_g
    for op in SPECIAL_CP:  # Handles backreferences
        group_num = op[2:]

        for t in m.transitions.get(q, {}).get(op, []):

            n_g = copy.deepcopy(groups)
            try:
                group_start, group_end = n_g[group_num][0], n_g[group_num][1]
            except KeyError:
                continue
            if group_start == '_' or group_end == '_':
                continue
            len_gk = (group_end - group_start)
            gk = w[group_start: group_end]

            if w[i:i+len_gk] == gk and i+len_gk <= len(w):

                yield t, i + len_gk, n_g
            else:
                continue

    if i < len(w):

        for t in m.transitions.get(q, {}).get(w[i], []):


            n_g = copy.deepcopy(groups)
            yield t, i + 1, n_g



def match(m, w):
    """Test whether a NFA accepts a string, using a breadth-first search.

    m: NFA
    w: list of symbols
    Returns:
      - if m accepts w, then (True, path), where path is a list of Transitions
      - otherwise, (False, None)
    """

    if m.start in m.accept and len(w) == 0:
        return True, []
    groups = {}
    start = (m.start, 0, groups)
    frontier = collections.deque([start])  # Queue of configurations to explore
    visited = {}  # Mapping from each visited configuration to one of its incoming transitions

    while len(frontier) > 0:

        q, i, groups = frontier.popleft()

        for t, j, group in _transitions(m, w, q, i, groups):

            group_tuple = convert_dict_to_tuple(group)
            # Don't allow duplicates in frontier.
            # If we do this later, it will be exponential.

            if (t.r, j, group_tuple) in visited: continue
            visited[t.r, j, group_tuple] = t

            if t.r in m.accept and j == len(w):

                # Reconstruct the path in reverse
                path = []

                return True, path
            frontier.append((t.r, j, group))
    return False, None
