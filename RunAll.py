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
    execution_time_fields
    execution_time_rows = []
    for dir in os.listdir(resources):
        for file in sorted_aphanumeric(os.listdir(resources + "/" + dir)):
            problem_file = resources + "/" + dir + "/" + file
            problem = ProblemParser(problem_file)
            print("------------------Parsing problem ", problem_file, "------------------")
            print("------------------Running Value Function (VI) ------------------")
            value_iteration_solver = ValueIterationSolver(problem.actions_available, problem.states, problem.transitions_by_current)
            value_iteration_solver.run()
            value_iteration_solver.last_run_v_function
            print("------------------Saving Value Function (VI) ------------------")
            print("------------------Saving Policy (VI) ------------------")
            value_iteration_solver.last_run_policy
            print("Execution time (in s): ", value_iteration_solver.last_run_duration)
            print("------------------Saving Value Function (LAO*) ------------------")
            lao_star_solver = LAOStarSolver(problem.actions_available, problem.states, problem.transitions_by_current, problem.transitions_by_next, problem.initial_state, problem.goal_state)
            lao_star_solver.run()
            lao_star_solver.last_run_v_function
            print("------------------Saving Policy (LAO*) ------------------")
            lao_star_solver.last_run_policy
            print("Execution time (in s): ", lao_star_solver.last_run_duration)
            execution_time_rows.append([value_iteration_solver.last_run_duration, lao_star_solver.last_run_duration])
            




