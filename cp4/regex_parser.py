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

    def dfs_traversal(self, counter=None):
        """
        Traverse regex graph for NFA operation execution.
        When a '#' is encountered, replace it with a consecutive number.
        :return: dfs order of operations with '#' replaced by consecutive numbers
        """
        if counter is None:  # Initialize the counter at 1 for the first call
            counter = [1]  # Use a list to hold the counter so it can be updated within the function

        printed_values = []
        for child in self.children:
            printed_values.extend(child.dfs_traversal(counter))  # Recursive call for children

            # Check if the value is '#' and replace it with the counter, then increment the counter
            if child.value == '~':
                printed_values.append(str(counter[0]))
                counter[0] += 1
            else:
                printed_values.append(child.value)  # Append the current node's value
        return printed_values

expression_ops = ('(', ')', '*', '|', "\\")


def parse(exp):
    stack = ['$']
    state_accept = False
    tree_string = []
    tree = []
    read_1, read_2 = ('$', '(', '|', 'T'), ('$', '(', '|')
    non_term = ('E', 'M', 'T', 'F', 'P')
    _next_1 = {'|', ')', '\x00'}
    exp_list = []
    i = 0
    while i < len(exp):
        char = exp[i]

        # Check for the backslash that might start an escape sequence
        if char == '\\':
            # Check if next character is a digit, implying \k
            if i + 1 < len(exp) and exp[i + 1].isdigit():
                sequence = char + exp[i + 1]
                i += 2

                # Continue to add digits to the sequence if more follow
                while i < len(exp) and exp[i].isdigit():
                    sequence += exp[i]
                    i += 1

                if sequence[1] == '0':
                    print("Error invalid backreference")
                    return None
                # Add the whole sequence to the list
                exp_list.append(sequence)
            elif i + 1 < len(exp) and exp[i + 1] == 'g':
                # Check for \g<k> sequence
                if i + 2 < len(exp) and exp[i + 2] == '<':
                    sequence = exp[i:i + 3]  # Start with '\g<'
                    i += 3
                    while i < len(exp) and exp[i].isdigit():
                        sequence += exp[i]
                        i += 1
                    if i < len(exp) and exp[i] == '>':
                        sequence += '>'
                        i += 1
                    if sequence[3] == '0':
                        print("Error invalid backreference")
                        return None
                    exp_list.append(sequence)
                else:
                    # If it's just '\g' without '<', treat it normally
                    exp_list.append(exp[i])
                    i += 1
            else:
                # It's not a digit or 'g' following the backslash, so treat it normally
                exp_list.append(exp[i:i + 2])
                i += 2
        else:
            exp_list.append(char)
            i += 1

    # Begin your original parsing logic here, replacing exp with exp_list
    exp = exp_list
    while exp:

        read = exp[0]
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
            if a.startswith('\\'):  # backref
                if '<' in a or '>' in a:
                    k = a[3:-1]
                else:
                    k = a[1:]
                
                tree_string.append(f"backref({k})")
                node = TreeNode("backref")
                node.add_child(TreeNode(int(k)))
                tree.append(node)
            else:
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
            tree_string.append(f"group(~,{gamma})")
            node = TreeNode("group")
            node.add_child(TreeNode("~"))
            node.add_child(gamma_tree)
            tree.append(node)
        elif read == '\0' and stack[-1] == 'E' and stack[-2] == '$':
            stack.pop()
            stack.pop()
            exp.pop(0)
            state_accept = True
        else:
            print("error, not path found")
            quit()

    new_string = ''
    i = 1
    for x, char in enumerate(tree_string[0]):
        if char == "~":
            new_string += str(i)
            i += 1
        else:
            new_string += char


    # Replace the original string in the list with the new string
    return new_string, tree[0] if state_accept else None

