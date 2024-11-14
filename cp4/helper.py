import sys
import hashlib
"""
Author: Rex Stayer-Suprick
Course: Theory of Computing
Date: 02/27/2024
Purpose: helper functions for CP2
"""


def read_input():
    """
    reads from command-line arguments to output string input
    """
    try:
        # Check if enough arguments are provided
        if len(sys.argv) < 2:
            raise ValueError("Insufficient arguments provided. Need both NFA file and string input.")

        # Extract string input from command-line arguments
        string_input = sys.argv[1]
    except ValueError as e:
        print(e)
        sys.exit(1)

    return string_input


def read_input_sat_to_re():
    """
    reads from command-line arguments to output string input
    """
    try:
        # Check if enough arguments are provided
        if len(sys.argv) < 3:
        
            raise ValueError("Insufficient arguments provided.")

        # Extract string input from command-line arguments
        cnf_file, regexp_file, string_file = sys.argv[1], sys.argv[2], sys.argv[3]
    except ValueError as e:
        print(e)
        sys.exit(1)

    return cnf_file, regexp_file, string_file

def read_input_msed():
    """
    reads from command-line arguments for msed
    """
    try:
        args = sys.argv[1:]

        commands = []
        files = []
        read_from_stdin = True

        # Flags to track the state
        expecting_command = False
        expecting_file = False

        for arg in args:
            
            if arg == '-f':
                expecting_file = True
            elif arg == '-e':
                expecting_command = True
            elif expecting_file:
                # Read commands from the specified file
                fp = open(arg)
                lines = fp.readlines()
                commands.extend(read_cmd_file(lines))
                expecting_file = False
            elif expecting_command:
                # Directly add the command
                commands.append(read_cmd_file([arg]))
                expecting_command = False
            else:
                # All remaining arguments are treated as files
                files.append(arg)
                read_from_stdin = False
        
        return commands, files, read_from_stdin

    except ValueError as e:
        print(e)
        sys.exit(1)


def read_cmd_file(lines):
    """
    reads a file and organizes commands
    :param file: file lines for each command
    :return: list of dictionaries that correspond to commands
    """

    commands = []

    for i, line in enumerate(lines):

        if line[0] == 's':  # replacement command
            parts = line.split('/')
            if len(parts) < 3:
                return "Invalid command format."
            regexp = parts[1]
            replacement = parts[2]
            backreferences = []
            i = 0
            replace = ''
            while i < len(replacement):

                if replacement[i] == '\\' and (i + 1 < len(replacement) and replacement[i + 1].isdigit()):

                    # Simple backreference \k
                    j = i + 1
                    k_content = ''
                    while j < len(replacement) and replacement[j].isdigit():
                        k_content += replacement[j]
                        j += 1
                    if k_content.isdigit():
                        backreferences.append(replace + '\\' + k_content)

                    i = j
                    replace = ''
                elif replacement[i] == '\\' and (
                        i + 2 < len(replacement) and replacement[i + 1] == 'g' and replacement[i + 2] == '<'):
                    # Extended backreference \g<k>
                    j = i + 3
                    k_content = ''
                    while j < len(replacement) and replacement[j] != '>':
                        k_content += replacement[j]
                        j += 1
                    if k_content.isdigit():
                        backref = replace + '\\g<' + k_content + '>'
                     
                        backreferences.append(backref)
                    i = j + 1
                    replace = ''
                else:
                    replace += replacement[i]
                    if i == len(replacement) -1:
                        backreferences[-1] += replacement[i]
                    i += 1
                
            commands.append({
                'type': 'replace',
                'regexp': regexp,
                'replacement': replacement,
                'backreferences': backreferences,
                'line': i
            })
        elif line[0] == '/':  # branch cmd
            parts = line.split('/')
            commands.append({
                'type': 'branch',
                'regexp': parts[1],
                'label': parts[2][1:].replace('\n', ''),
                'line': i
            })
        elif line[0] == ':':  # label
            commands.append({
                'type': 'label',
                'line': i,
                'label': line[1:].replace('\n', '')
            })
        else:
            print('invalid cmd')

    return commands


def read_input_union():
    """
    reads from command-line arguments to output string input
    """
    try:
        # Check if enough arguments are provided
        if len(sys.argv) < 3:
            raise ValueError("Insufficient arguments provided. Need both NFA file and string input.")

        # Extract string input from command-line arguments
        m1 = sys.argv[1]
        m2 = sys.argv[2]
    except ValueError as e:
        print(e)
        sys.exit(1)

    return m1, m2


def hash_string(string):
    # Encode the string to bytes before hashing
    string_bytes = string.encode('utf-8')

    # Create a hashlib object for SHA-256 hashing
    hasher = hashlib.sha256()

    # Update the hasher with the bytes of the string
    hasher.update(string_bytes)

    # Get the hexadecimal digest of the hash
    hashed_string = hasher.hexdigest()

    return hashed_string + '.nfa'


def get_matches(path):
    open_groups = {}  # To keep track of where each group starts
    group_contents = {}  # To store the contents of each group
    return_groups = []
    
    for i, step in enumerate(path):

        if 'o' in step.a and step.a != 'o':
            # Mark the start of a group, extracting the group number from the transition
            group_number = int(step.a[1:])
            open_groups[group_number] = i  # Store the position where the group opens
        elif 'c' in step.a and step.a != 'c' and 'cp' not in step.a:
            # Mark the end of a group, reconstruct and print the group's content
            group_number = int(step.a[1:])
            start_index = open_groups[group_number]
            # Extract the substring from the path that belongs to the group
            group_content = ''.join(
                step.a for j, step in enumerate(path[start_index:i + 1]) if step.a != '&' and len(step.a) == 1)
            group_contents[group_number] = group_content
    # Print the groups in order
    for group_number in sorted(group_contents):
        return_groups.append([group_number, group_contents[group_number]])
    return return_groups
