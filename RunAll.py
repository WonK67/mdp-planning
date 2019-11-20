from ProblemParser import ProblemParser
from ValueIterationSolver import ValueIterationSolver
from LAOStarSolver import LAOStarSolver

import os
import csv
import re

def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def save_v_function(file_name, v_function):
    fields = ["state", "v_function"]
    list = [[k, v] for k, v in v_function.items()]
    with open(file_name, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(list)

def save_policy(file_name, policy):
    fields = ["state", "policy"]
    list = [[k, v] for k, v in policy.items()]
    with open(file_name, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(list)

if __name__ == '__main__':
    resources = "./resources"
    fields = ["VI", "LAO*"]
    execution_time_rows = []
    policy_size_rows = []
    for dir in os.listdir(resources):
        for i,file in enumerate(sorted_aphanumeric(os.listdir(resources + "/" + dir))):
            problem_file = resources + "/" + dir + "/" + file
            problem = ProblemParser(problem_file)
            print("------------------Parsing problem ", problem_file, "------------------")
            print("------------------Running Value Function (VI) ------------------")
            value_iteration_solver = ValueIterationSolver(problem.actions_available, problem.states, problem.transitions_by_current)
            value_iteration_solver.run()
            print("------------------Saving Value Function (VI) ------------------")
            save_v_function(dir + "_" + str(i+1) + "_" + "function_vi.csv",value_iteration_solver.last_run_v_function)
            print("------------------Saving Policy (VI) ------------------")
            save_v_function(dir + "_" + str(i+1) + "_" + "policy_vi.csv", value_iteration_solver.last_run_policy)
            print("Execution time (in s): ", value_iteration_solver.last_run_duration)
            print("------------------Saving Value Function (LAO*) ------------------")
            lao_star_solver = LAOStarSolver(problem.actions_available, problem.states, problem.transitions_by_current, problem.transitions_by_next, problem.initial_state, problem.goal_state)
            lao_star_solver.run()
            save_v_function(dir + "_" + str(i+1) + "_" + "function_lao.csv", lao_star_solver.last_run_v_function)
            print("------------------Saving Policy (LAO*) ------------------")
            save_v_function(dir + "_" + str(i+1) + "_" + "policy_lao.csv", lao_star_solver.last_run_policy)
            print("Execution time (in s): ", lao_star_solver.last_run_duration)
            execution_time_rows.append([value_iteration_solver.last_run_duration, lao_star_solver.last_run_duration])
            policy_size_rows.append([len(value_iteration_solver.last_run_policy), len(lao_star_solver.last_run_policy)])
    with open("execution_time.csv", 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(execution_time_rows)
            




