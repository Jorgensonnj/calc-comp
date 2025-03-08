## About

This is a small cli application that calculates the reimbursement amount for a given set of projects.

Here's why:
* Allows the user calculate their reimbursement amount quickly
* Allows for multiple concurrent projects to occur in tandem

## Getting Started

To try it for your self follow these simple example steps.

### Prerequisites

Install dependencies using the following methods.
* Git
* Python 3.10.7 or greater

### Installation

1. Clone the repo
   ```sh
   git clone git@github.com:Jorgensonnj/calc-comp.git
   ```

## Usage

The cli works right out of the box.

All you need to do is enter the git repo folder
```sh
cd calc-comp/
```

Then run the command
```sh
./calc_comp.py
```

*note: the cli will run all sample sets in the* `set/` *directory. If you want to change this, please edit the calc_comp.py file and uncomment individual test sets.  (e.g. process_set(DIRECTORY_PATH, "set_1"))*

## Assumptions

* The user is familiar with the command line and is able to execute the program
* The project set files are in the set directory
* Valid project set lines are formatted correctly and are in their respective project set file
