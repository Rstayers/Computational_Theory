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
