#!/usr/bin/env python

import os
import re
import heapq
from datetime import datetime
from typing import Dict, Tuple, List

class Project:
    def __init__(self, id: str, rate: str, start_date: datetime, end_date: datetime):
        self.id = id
        self.rate = rate
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"[id: {self.id}, rate: {self.rate}, start: {self.start_date}, end: {self.end_date}]"

    def __str__(self):
        return f"[id: {self.id}, rate: {self.rate}, start: {self.start_date}, end: {self.end_date}]"


def extract_project_data(line: str) -> Tuple[str, Project] | None:
    # Use regex to extract project information
    matches = re.search(
        r"Project (\d): (Low|High) Cost City Start Date: (\d?\d/\d?\d/\d\d) End Date: (\d?\d/\d?\d/\d\d)",
        line
    )
    if matches is not None:
        project = Project(
            matches.group(1),
            matches.group(2),
            datetime.strptime(matches.group(3), '%m/%d/%y'),
            datetime.strptime(matches.group(4), '%m/%d/%y'),
        )

        return project.id, project

    return None

def process_set_data(set_data: Dict[str, Project]) -> List[Project]:
    projects = list()

    # Garrentee that the projects are in order of their start date
    sorted_projects = [ item for item in sorted(set_data.values(), key=lambda project : project.start_date) ]

    previous = sorted_projects[0]
    for project in sorted_projects[1:]:

        # merge projects into on larg
        if project.start_date <= previous.end_date:
            previous.end_date = max(previous.end_date, project.end_date)
        else:
            projects.append(previous)
            previous = project

    projects.append(previous)

    return projects

def calculate(projects: List[Project]):
    # Hardcoded costs
    #city_cost = {"High": (85, 55), "Low": (75,45)} # (full_day, travel_day)

    total_compensation = 0

    return total_compensation

def process_set(directory_path: str, file_name: str):
    file_path = os.path.join(directory_path, file_name)

    set_data: Dict[str, Project] = dict()
    # Open file and get data
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            result = extract_project_data(line.strip())
            if result:
                project_id, project = result[0], result[1]
                # This will overwrite existing data at project_id location.
                # This will prevent duplicate project information per set.
                set_data[project_id] = project

    # After file is closed, process the set data
    projects = process_set_data(set_data)

    # Finally, calculate the compensation
    #total_compensation = calculate(date_heap)

    #print(f"Set: {file_name} Total: {total_compensation}")

def process_all(directory_path: str):
    # Loop through all set files in given directory
    for file_name in sorted(os.listdir(directory_path)):
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
    #process_all(DIRECTORY_PATH)


if __name__ == "__main__":
    main()
