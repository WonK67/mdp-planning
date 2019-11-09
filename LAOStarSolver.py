from ValueIterationSolver import ValueIterationSolver
import timeit

class LAOStarSolver:

    states = []
    transitions = []
    start_state = None
    end_state = None
    last_run_duration = 0
    last_run_v_function = {}
    last_run_policy = {}

    def __init__(self, states, transitions, start_state, end_state):
        self.states = states
        self.transitions = transitions
        self.start_state = start_state
        self.end_state = end_state

    def run(self):
        start = timeit.default_timer()
        self.last_run_v_function = self.lao_star()
        stop = timeit.default_timer()
        self.last_run_duration = stop - start

    def lao_star(self):
        expanded_states = []
        v1 = {s: self.manhattan_heuristic(s) for s in self.states}
        g_line = {self.start_state: v1[self.start_state]}
        g_line_line = g_line.copy()
        while self.end_state not in g_line_line:
            for state in g_line_line:
                if state not in expanded_states:
                    tip_state = state
                    break
            self.expandGLine(tip_state, g_line, v1)
            expanded_states.append(tip_state)
            z = list(g_line_line.keys())
            value_iteration_solver = ValueIterationSolver(z, self.transitions)
            value_iteration_solver.run()
            v1 = value_iteration_solver.last_run_v_function
            print(v1)
            break


    def manhattan_heuristic(self, state:str):
        coordinate_start = state.split("x")[1].split("y")
        x_start = int(coordinate_start[0])
        y_start = int(coordinate_start[1])
        coordinate_end = self.end_state.split("x")[1].split("y")
        x_end = int(coordinate_end[0])
        y_end = int(coordinate_end[1])
        return self.manhattan_distance(x_start, x_end, y_start, y_end)

    @staticmethod
    def manhattan_distance(x_start, x_end, y_start, y_end):
        return abs(x_end - x_start) + abs(y_end - y_start)

    def getChildren (self, state, v1):
        children = {}
        for transition in self.transitions:
            if transition.current_state == state and transition.next_state not in children:
                children[transition.next_state] = v1[transition.next_state]
        return children


    def expandGLine(self, tip_state, g_line, v1):
        children = self.getChildren(tip_state, v1)
        g_line.update(children)

