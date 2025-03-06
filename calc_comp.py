#!/usr/bin/env python

import os
import re
import heapq
from datetime import datetime
from typing import Dict, Tuple

def extract_project_data(line: str) -> Tuple[str, Dict[str, str]]:
    project_id = ""
    project_data = dict()

    # Use regex to extract project information
    matches = re.search(
        r"Project (\d): (Low|High) Cost City Start Date: (\d?\d/\d?\d/\d\d) End Date: (\d?\d/\d?\d/\d\d)",
        line
    )
    if matches is not None:
        project_id = matches.group(1)
        project_data["project_cost"] = matches.group(2)
        project_data["project_start"] = matches.group(3)
        project_data["project_end"] = matches.group(4)

    return project_id, project_data

def process_set_data(set_data: Dict[str, Dict[str, str]]):
    dates = list()
    # Extract date date from dictionary and convert to datetime
    for project_data in set_data.values():
        if (start_data := project_data.get("project_start")) and (end_data := project_data.get("project_end")):
            dates.append(datetime.strptime(start_data, '%m/%d/%y')) # add start date to list
            dates.append(datetime.strptime(end_data,'%m/%d/%y'))    # add end date to list

    # Where the magic happens
    heapq.heapify(dates)

    while len(dates) > 0:
        item = heapq.heappop(dates)
        print(f"{item}")



def process_set(directory_path: str, file_name: str):
    file_path = os.path.join(directory_path, file_name)

    set_data = dict()
    # Open file and get data
    with open(file_path, 'r') as file:
        lines = file.readlines()
        print(f"{file_name}:")
        for line in lines:
            project_id, project_data = extract_project_data(line.strip())

            # This will overwrite existing data at project_id location.
            # This will prevent duplicate project information per set.
            set_data[project_id] = project_data


    # After file is closed,
    process_set_data(set_data)
    #print(f"{file_name}: {set_data}")

def process_all(directory_path: str):
    # Loop through all set files in given directory
    for file_name in os.listdir(directory_path):
        process_set(directory_path, file_name)


def main():


    DIRECTORY = "sets"

    # Define where the set files live relative to where this script gets executed
    DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), DIRECTORY)

    if not os.path.isdir(DIRECTORY_PATH):
        print(f"Directory does not exist.")
        exit()

    process_set(DIRECTORY_PATH, "set_1")
    #process_all(DIRECTORY_PATH)


if __name__ == "__main__":
    main()
