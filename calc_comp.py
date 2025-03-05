#!/usr/bin/env python

import os

def import_and_process_files(directory: str):
    # Loop through all set files in given directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Open file for reading
        with open(file_path, 'r') as file:
            lines = file.readlines()
            print(f'{filename}:') # Print file's name
            for index in range(len(lines)):
                print(f'Line {index}: {lines[index].strip()}') # Print each individual line


def main():

    # Define where the sets of projects live relative
    # to where this script gets executed
    # example: /home/username/Projects/python/calc-comp/ as starting point
    PROJECT_SETS_DIRECTORY = "sets"
    PROJECT_SETS_PATH = os.path.join(os.path.dirname(__file__), PROJECT_SETS_DIRECTORY)

    import_and_process_files(PROJECT_SETS_PATH)

    #print("Tis just the beginning")

if __name__ == "__main__":
    main()
