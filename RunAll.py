from ProblemParser import ProblemParser
from ValueIterationSolver import ValueIterationSolver
import os
import csv
import re

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

if __name__ == '__main__':
    resources = "./resources"
    execution_time = []
    for dir in os.listdir(resources):
        for file in sorted_aphanumeric(os.listdir(resources + "/" + dir)):
            problem = ProblemParser(problem_file)




