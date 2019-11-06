from ProblemParser import ProblemParser
from ValueIterationSolver import ValueIterationSolver

problem = ProblemParser("resources/RandomGoalState/navigation_1.net")
ValueIterationSolver(problem.states, problem.transitions)