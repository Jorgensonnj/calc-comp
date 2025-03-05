#!/usr/bin/env python

import os
import re
from typing import Dict, List

def process_set_line(line: str) -> Dict[str, str]:
    project_data = dict()

    # Use regex to extract project information
    matches = re.search(
        r"Project (\d): (Low|High) Cost City Start Date: (\d?\d/\d?\d/\d\d) End Date: (\d?\d/\d?\d/\d\d)",
        line
    )
    if matches is not None:
        project_data["project_number"] = matches.group(1)
        project_data["project_cost"] = matches.group(2)
        project_data["project_start"] = matches.group(3)
        project_data["project_end"] = matches.group(4)

    return project_data

def process_set_file(file_path: str) -> List[Dict[str, str]]:
    # Open file for reading
    projects = list()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Extract the line's data and add it to the array
            projects.append(
                process_set_line(line.strip())
            )

    return projects

def import_and_process_files(directory: str):
    # Loop through all set files in given directory
    for filename in os.listdir(directory):
        # Let's just focus on the first set for now
        if filename != "set_1":
            continue

        file_path = os.path.join(directory, filename)

        print(f"{filename}: {process_set_file(file_path)}")


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
