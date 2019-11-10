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
        fringe_states = [self.start_state]
        g_line = {self.start_state: self.manhattan_heuristic(self.start_state)}
        g_line_policy = {}
        z = []
        while self.end_state not in z:
            bestChild = self.getBestChild(fringe_states, g_line)
            z.append(bestChild)
            for state in z:
                if state not in expanded_states:
                    tip_state = state
                    break
            self.expandGLine(tip_state, g_line, expanded_states, fringe_states)

            z_transitions = self.filterAvailableTransitions(g_line, self.transitions)
            z_values = g_line
            value_iteration_solver = ValueIterationSolver(z, z_transitions, z_values)
            value_iteration_solver.run()
            g_line = value_iteration_solver.last_run_v_function
            g_line_policy = value_iteration_solver.last_run_policy

            print(g_line)
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

    def getChildren (self, state, g_line):
        children = {}
        for transition in self.transitions:
            if transition.current_state == state and transition.next_state not in children and transition.next_state != state and transition.next_state not in list(g_line.keys()):
                children[transition.next_state] = self.manhattan_heuristic(transition.next_state)
        return children

    def expandGLine(self, tip_state, g_line, expanded_states, fringe_states):
        children = self.getChildren(tip_state, g_line)
        g_line.update(children)
        expanded_states.append(tip_state)
        fringe_states += list(children.keys())
        fringe_states.remove(tip_state)

    @staticmethod
    def filterAvailableTransitions(states, transitions):
        available_transitions = []
        for transition in transitions:
            if transition.current_state in states and transition.next_state in states:
                available_transitions.append(transition)
        return available_transitions

    @staticmethod
    def filterAvailableValues(states, v):
        available_values = {}
        for state in states:
            if state in list(v.keys()):
                available_values[state] = v[state]
        return available_values

    def getBestChild (self, fringe_states, g_line):
        fringe_v1 = {s: g_line[s] for s in fringe_states}
        bestChild = min(fringe_states, key = lambda s: fringe_v1[s])
        print(bestChild)
        return bestChild
