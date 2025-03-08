#!/usr/bin/env python

import os
import re
from datetime import datetime, timedelta
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

def process_set_data(set_data: Dict[str, Project]) -> List[List[Project]]:
    sequences: List[List[Project]] = list()

    # Guarantee that the projects are in order of their start date
    sorted_projects = [ item for item in sorted(set_data.values(), key=lambda project : project.start_date) ]

    previous = sorted_projects.pop(0)
    is_contiguous = False

    while len(sorted_projects) > 0:
        project = sorted_projects.pop(0)

        # Is there an overlap?
        if project.start_date <= previous.end_date:
            if previous.end_date < project.end_date:
                # Adjust the overlapping items
                if previous.rate == "High":
                    project.start_date = previous.end_date + timedelta(days=1)
                    sequences.append([previous])
                else:
                    previous.end_date = project.start_date - timedelta(days=1)
                    sequences.append([previous])
                is_contiguous = True

            elif previous.end_date == project.end_date:
                pass # just drop the previous project
            else:
                # if previous item is larger, but the over lapping section as precedence
                if previous.rate == "Low" and project.rate == "High":
                    temp = previous.end_date
                    previous.end_date = project.start_date - timedelta(days=1)
                    sequences.append([previous])
                    sequences[-1].append(project)
                    new_project = Project(
                        previous.id,
                        previous.rate,
                        project.end_date + timedelta(days=1),
                        temp
                    )
                    sequences[-1].append(new_project)
                is_contiguous = True

        else:
            if is_contiguous and len(sorted_projects) > 0:
                sequences[-1].append(previous)
                is_contiguous = False
            else:
                sequences.append([previous])

        previous = project

    if is_contiguous:
        sequences[-1].append(previous)
    else:
        sequences.append([previous])

    return sequences

def calculate(sequences: List[List[Project]]):
    # Hard coded
    city_cost = {"High": (85, 55), "Low": (75,45)} # (full day rate, travel day rate)
    total_compensation = 0

    for sequence in sequences:

        first_project = sequence[0]
        last_project = sequence[-1]

        # remove the first and the last days and add the compensation at the right rate
        # The two projects are not the same
        if first_project != last_project:

            first_project.start_date += timedelta(days=1)
            last_project.end_date -= timedelta(days=1)

            total_compensation += city_cost[first_project.rate][1]
            total_compensation += city_cost[last_project.rate][1]

        else:
            # last and first are the same project
            if last_project.start_date != last_project.end_date:

                last_project.start_date += timedelta(days=1)
                last_project.end_date -= timedelta(days=1)

                total_compensation += city_cost[last_project.rate][1]
                total_compensation += city_cost[last_project.rate][1]
            else:
                sequence.pop()

                total_compensation += city_cost[last_project.rate][1]

        # Add up all of the full work days
        for project in sequence:
            days = (project.end_date - project.start_date).days + 1
            total_compensation += days * city_cost[project.rate][0]

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
    total_compensation = calculate(projects)

    print(f"Set: {file_name} Total: {total_compensation}")

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

    #process_set(DIRECTORY_PATH, "set_1")
    #process_set(DIRECTORY_PATH, "set_2")
    #process_set(DIRECTORY_PATH, "set_3")
    #process_set(DIRECTORY_PATH, "set_4")
    process_all(DIRECTORY_PATH)


if __name__ == "__main__":
    main()
