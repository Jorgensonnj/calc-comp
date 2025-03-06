#!/usr/bin/env python

import os
import re
import heapq
from datetime import datetime
from typing import Dict, Tuple, List

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
        project_data["project_id"] = project_id
        project_data["project_cost"] = matches.group(2)
        project_data["project_start"] = matches.group(3)
        project_data["project_end"] = matches.group(4)

    return project_id, project_data

def process_set_data(set_data: Dict[str, Dict[str, str]]) -> List[Tuple[datetime, str, Dict[str, str]]]:
    dates = list()
    # Extract date date from dictionary and convert to datetime
    for project_data in set_data.values():
        dates.append((
            datetime.strptime(project_data["project_start"], '%m/%d/%y'),
            project_data["project_id"],
            project_data
        )) # add start date to list
        dates.append((
            datetime.strptime(project_data["project_end"], '%m/%d/%y'),
            project_data["project_id"],
            project_data
        )) # add start date to list

    # Where the magic happens
    heapq.heapify(dates)

    return dates

def calculate(date_heap: List[Tuple[datetime, str, Dict[str, str]]]):

    # Hardcoded costs
    city_cost = {"High": (85, 55), "Low": (75,45)}

    total_compensation = 0

    # Start pointer
    start = heapq.heappop(date_heap)
    start_date, start_data = start[0], start[2]

    while len(date_heap) > 0:

        # End pointer
        end = heapq.heappop(date_heap)
        end_date = end[0]

        delta_days = (end_date - start_date).days + 1  # number of full days inbetween

        start_cost = city_cost[start_data["project_cost"]]
        total_compensation += ((delta_days - 2) * start_cost[0]) + (2 * start_cost[1])

    return total_compensation

def process_set(directory_path: str, file_name: str):
    file_path = os.path.join(directory_path, file_name)

    set_data = dict()
    # Open file and get data
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            project_id, project_data = extract_project_data(line.strip())

            # This will overwrite existing data at project_id location.
            # This will prevent duplicate project information per set.
            set_data[project_id] = project_data

    # After file is closed, process the set data
    date_heap = process_set_data(set_data)
    # Finally, calculate the compensation
    total_compensation = calculate(date_heap)

    print(f"Set: {file_name} Total: {total_compensation}")

def process_all(directory_path: str):
    # Loop through all set files in given directory
    for file_name in os.listdir(directory_path):
        process_set(directory_path, file_name)

def main():

    DIRECTORY = "sets"

    # Define where the set files live relative to where this script gets executed
    DIRECTORY_PATH = os.path.join(os.path.dirname(__file__), DIRECTORY)

    # Check if directory exists
    if not os.path.isdir(DIRECTORY_PATH):
        print(f"Directory does not exist.")
        exit()

    process_set(DIRECTORY_PATH, "set_2")


if __name__ == "__main__":
    main()
