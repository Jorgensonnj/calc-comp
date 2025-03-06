#!/usr/bin/env python

import os
import re
from typing import Dict

def process_set_line(line: str) -> Dict[str, Dict[str, str]]:
    set_data = dict()

    # Use regex to extract project information
    matches = re.search(
        r"Project (\d): (Low|High) Cost City Start Date: (\d?\d/\d?\d/\d\d) End Date: (\d?\d/\d?\d/\d\d)",
        line
    )
    if matches is not None:

        product_id = matches.group(1)

        # Duplicate project rows will result in the last entry
        # overwriting existing project data in dictionary.
        # This prevents double calculations of compensation
        if not product_id in set_data:
            set_data[product_id] = dict()

        set_data[product_id]["project_cost"] = matches.group(2)
        set_data[product_id]["project_start"] = matches.group(3)
        set_data[product_id]["project_end"] = matches.group(4)

    return set_data

def process_set(directory: str, file_name: str):
    # Open file for reading

    file_path = os.path.join(os.path.dirname(__file__), directory, file_name)
    print(file_path)
    set_data = dict()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            set_data = process_set_line(line.strip())

        print(f"{file_name}: {set_data}")

def process_all(directory: str):

    # Define where the sets live relative
    # to where this script gets executed
    # example: /home/username/Projects/python/calc-comp/ as starting point
    directory_path = os.path.join(os.path.dirname(__file__), directory)

    # Loop through all set files in given directory
    for file_name in os.listdir(directory_path):
        process_set(directory, file_name)


def main():


    DIRECTORY = "sets"

    if not os.path.isdir(DIRECTORY):
        print(f"Directory does not exist.")
        exit()

    process_set(DIRECTORY, "set_1")
    #process_all(DIRECTORY)


if __name__ == "__main__":
    main()
