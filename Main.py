from ProblemParser import ProblemParser
from ValueIterationSolver import ValueIterationSolver
from LAOStarSolver import LAOStarSolver

problem_file = "resources/RandomGoalState/navigation_1.net"
print("------------------Parsing problem ", problem_file, "------------------")
problem = ProblemParser(problem_file)
print("Successfully parsed!")
# print("------------------Value Function (VI) ------------------")
# value_iteration_solver = ValueIterationSolver(problem.actions_available, problem.states, problem.transitions_by_current)
# value_iteration_solver.run()
# print(value_iteration_solver.last_run_v_function)
# print("------------------Policy (VI) ------------------")
# print(value_iteration_solver.last_run_policy)
# print("Execution time (in s): ", value_iteration_solver.last_run_duration)
print("------------------Value Function (LAO*) ------------------")
lao_star_solver = LAOStarSolver(problem.actions_available, problem.states, problem.transitions_by_current, problem.transitions_by_next, problem.initial_state, problem.goal_state)
lao_star_solver.run()
print(lao_star_solver.last_run_v_function)
print("------------------Policy (LAO*) ------------------")
print(lao_star_solver.last_run_policy)
print("Execution time (in s): ", lao_star_solver.last_run_duration)


