from ProblemParser import ProblemParser
from ValueIterationSolver import ValueIterationSolver

problem_file = "resources/RandomGoalState/navigation_1.net"
print("------------------Parsing problem ", problem_file, "------------------")
problem = ProblemParser(problem_file)
print("Successfully parsed!")
print("------------------Value Function------------------")
value_iteration_solver = ValueIterationSolver(problem.states, problem.transitions)
value_iteration_solver.run()
print(value_iteration_solver.last_run_v_function)
print("------------------Policy------------------")
print(value_iteration_solver.last_run_policy)
print("Execution time (in s): ", value_iteration_solver.last_run_duration)