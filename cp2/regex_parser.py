"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/27/2024
Purpose: Parses a regular expression to output a regex tree
"""


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def dfs_traversal(self):
        """
        traverse regex graph for NFA operation execution
        :return: dfs order of operations
        """
        printed_values = []

        for child in self.children:
            printed_values.extend(child.dfs_traversal())  # Recursive call for children

            printed_values.append(child.value)  # Append the current node's value
        return printed_values


expression_ops = ('(', ')', '*', '|', "\\")


def parse(exp):
    exp = list(exp)
    stack = ['$']
    state_accept = False
    tree_string = []
    tree = []

    while exp:

        read = exp[0]
        read_1, read_2 = ('$', '(', '|', 'T'), ('$', '(', '|')
        non_term = ('E', 'M', 'T', 'F', 'P')
        _next_1 = {'|', ')', '\x00'}
        if (read not in expression_ops and read != '\0' and read not in non_term) and stack[-1] in read_1:
            stack.append(read)
            exp.pop(0)
        elif read == '(' and stack[-1] in read_1:
            stack.append('(')
            exp.pop(0)
        elif read == ')' and stack[-1] == 'E':
            stack.append(')')
            exp.pop(0)
        elif read == '|' and stack[-1] == 'E':
            stack.append('|')
            exp.pop(0)
        elif read == '*' and stack[-1] == 'P':
            stack.append('*')
            exp.pop(0)
        elif stack[-1] == 'M' and stack[-2] == '|' and stack[-3] == 'E':
            stack.pop()
            stack.pop()
            e = stack.pop()
            beta = tree_string.pop()
            gamma = tree_string.pop()
            beta_tree = tree.pop()
            gamma_tree = tree.pop()
            stack.append(e)  # E(union(gamma, beta))
            tree_string.append(f'union({gamma},{beta})')
            node = TreeNode("union")
            node.add_child(gamma_tree)
            node.add_child(beta_tree)
            tree.append(node)

        elif stack[-1] == 'M' and stack[-2] in ('$', '('):
            stack.pop()
            gamma = tree_string.pop()
            gamma_tree = tree.pop()
            stack.append('E')  # E(gamma)
            tree_string.append(gamma)
            tree.append(gamma_tree)
        elif stack[-1] in read_2 and read in _next_1:
            stack.append('M')  # M(epsilon())
            tree_string.append('epsilon()')

            tree.append(TreeNode('epsilon'))
        elif stack[-1] == 'T' and read in _next_1:
            stack.pop()
            gamma = tree_string.pop()
            gamma_tree = tree.pop()
            stack.append('M')  # M(gamma)
            tree_string.append(gamma)
            tree.append(gamma_tree)
        elif stack[-1] == 'F' and stack[-2] == 'T':
            stack.pop()
            stack.pop()
            beta = tree_string.pop()
            gamma = tree_string.pop()
            beta_tree = tree.pop()
            gamma_tree = tree.pop()
            stack.append('T')  # T(concat(gamma, beta)
            tree_string.append(f'concat({gamma},{beta})')
            node = TreeNode("concat")
            node.add_child(gamma_tree)
            node.add_child(beta_tree)
            tree.append(node)
        elif stack[-1] == 'F' and stack[-2] in read_2:
            stack.pop()
            gamma = tree_string.pop()
            gamma_tree = tree.pop()
            stack.append('T')  # T(gamma)
            tree_string.append(gamma)
            tree.append(gamma_tree)
        elif stack[-1] == '*' and stack[-2] == 'P':
            stack.pop()
            stack.pop()
            gamma = tree_string.pop()
            gamma_tree = tree.pop()
            stack.append('F')  # F(star(gamma))
            tree_string.append(f'star({gamma})')
            node = TreeNode("star")
            node.add_child(gamma_tree)
            tree.append(node)
        elif stack[-1] == 'P' and read != '*':
            stack.pop()
            gamma = tree_string.pop()
            gamma_tree = tree.pop()
            stack.append('F')  # F(star(gamma))
            tree_string.append(gamma)
            tree.append(gamma_tree)

        elif stack[-1] not in expression_ops and stack[-1] != '\0' and stack[-1] not in non_term:
            a = stack.pop()
            stack.append('P')  # P(symbol(a))
            tree_string.append(f"symbol(\"{a}\")")
            node = TreeNode("symbol")
            node.add_child(TreeNode(a))
            tree.append(node)
        elif stack[-1] == ')' and stack[-2] == 'E' and stack[-3] == '(':
            stack.pop()
            stack.pop()
            stack.pop()
            gamma = tree_string.pop()
            gamma_tree = tree.pop()
            stack.append('P')  # P(gamma)
            tree_string.append(gamma)
            tree.append(gamma_tree)
        elif read == '\0' and stack[-1] == 'E' and stack[-2] == '$':
            stack.pop()
            stack.pop()
            exp.pop(0)
            state_accept = True
        else:
            print("error, not path found")
            quit()

    return tree_string[0], tree[0] if state_accept else None

