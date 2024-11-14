import collections

EPSILON = '&'
SPECIAL_C = [f'c{i}' for i in range(1, 1000)]
SPECIAL_O = [f'o{i}' for i in range(1, 1000)]

class Transition(object):
    def __init__(self, q, a, r):
        self.q = q
        self.a = a
        self.r = r


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
        if t.a != EPSILON and t.a not in SPECIAL_O and t.a not in SPECIAL_C:
            self.add_symbol(t.a)
        self.add_state(t.r)
        self.transitions.setdefault(t.q, {}).setdefault(t.a, []).append(t)


def read(file):
    """Read a NFA from a file."""
    m = NFA()
    print('here')
    for q in next(file).split():
        m.add_state(q)
    for a in next(file).split():
        m.add_symbol(a)
    m.set_start(next(file).rstrip())
    for q in next(file).split():
        m.add_accept(q)
    for line in file:
        q, a, r = line.split()
        print(a)
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


def _transitions(m, w, q, i):
    """Helper function for match_dfs and match_bfs.

    If NFA m is in state q and reading string w at position i,
    iterates over possible transitions and new positions."""

    for t in m.transitions.get(q, {}).get(EPSILON, []):
        yield t, i
    # Handle special operations that act like epsilon transitions
    for special_op in [SPECIAL_O, SPECIAL_C]:
        for t in m.transitions.get(q, {}).get(special_op, []):
            yield t, i
    if i < len(w):
        for t in m.transitions.get(q, {}).get(w[i], []):
            yield t, i + 1


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
    start = (m.start, 0)
    frontier = collections.deque([start])  # Queue of configurations to explore
    visited = {}  # Mapping from each visited configuration to one of its incoming transitions

    while len(frontier) > 0:
        q, i = frontier.popleft()
        for t, j in _transitions(m, w, q, i):
            # Don't allow duplicates in frontier.
            # If we do this later, it will be exponential.
            if (t.r, j) in visited: continue
            visited[t.r, j] = t
            if t.r in m.accept and j == len(w):
                # Reconstruct the path in reverse
                path = []
                r = t.r
                while (r, j) != start:
                    t = visited[r, j]
                    path.append(t)
                    r = t.q
                    if t.a != EPSILON and t.a not in SPECIAL_O and t.a not in SPECIAL_C: j -= 1
                path.reverse()
                return True, path
            frontier.append((t.r, j))
    return False, None
