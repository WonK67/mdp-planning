from ValueIterationSolver import ValueIterationSolver
import timeit
import sys

class LAOStarSolver:
    states = []
    transitions_by_current = {}
    transitions_by_next = {}
    start_state = None
    end_state = None
    last_run_duration = 0
    last_run_v_function = {}
    last_run_policy = {}
    visited_states = []
    actions_available = []

    def __init__(self, actions_available, states, transitions_by_current, transitions_by_next, start_state, end_state):
        self.states = states
        self.transitions_by_current = transitions_by_current
        self.transitions_by_next = transitions_by_next
        self.start_state = start_state
        self.end_state = end_state
        self.actions_available = actions_available

    def run(self):
        start = timeit.default_timer()
        self.last_run_v_function = self.new_lao_star()
        stop = timeit.default_timer()
        self.last_run_duration = stop - start

    def new_lao_star(self):
        tip_states = [self.start_state]
        g_line = {self.start_state: self.manhattan_heuristic(self.start_state)}
        g_line_line = {}
        greedy_policy = {}
        g_line_line = self.explore_tip_states(g_line, greedy_policy, tip_states)
        return g_line_line

    def explore_tip_states(self, outer_graph, policy, tip_states):
        while tip_states != [self.end_state] and len(tip_states) != 0:
            tip_state = self.select_tip_state(tip_states)
            self.expand(tip_state, outer_graph)
            z = self.get_this_and_previous_states_using_policy(tip_state, policy)
            g_line_line = self.generate_best_partial_solution(z, policy, outer_graph)
            tip_states = self.get_states_without_action(g_line_line.keys(), policy)
        convergence_test_solution = self.generate_best_partial_solution(g_line_line, policy, outer_graph)
        tip_states = self.get_states_without_action(convergence_test_solution.keys(), policy)
        if tip_states != [self.end_state] and len(tip_states) != 0:
            return self.explore_tip_states(outer_graph, policy, tip_states)
        else:
            print("g_line (", len(outer_graph), ") ")
            print("g_line (", len(convergence_test_solution), ") ")
            self.fill_final_policy(convergence_test_solution, policy)
            return convergence_test_solution

    def fill_final_policy(self, solution_graph, solution_policy):
        self.last_run_policy = {}
        for state in solution_graph:
            self.last_run_policy[state] = solution_policy[state]

    def generate_best_partial_solution(self, graph_to_run_iv, policy, graph_to_use_policy):
        transitions = self.getAvailableTransitions(graph_to_run_iv)
        value_iteration_solver = ValueIterationSolver(self.actions_available, graph_to_run_iv, transitions, graph_to_use_policy)
        value_iteration_solver.run()
        g_line = value_iteration_solver.last_run_v_function
        best_partial_solution_policy = value_iteration_solver.last_run_policy
        self.mergePolicy(best_partial_solution_policy, policy)
        self.visited_states = []
        policy_states = self.get_this_and_next_states_using_policy(self.start_state, policy)
        return {s: g_line[s] for s in policy_states}

    #the tip states
    def get_states_without_action(self, states, policy):
        states_without_action = []
        for state in states:
            if state not in policy:
                states_without_action.append(state)
        return states_without_action

    def get_this_and_next_states_using_policy(self, state, policy):
        self.visited_states = []
        next_states = self.get_next_states_using_policy(state, policy)
        if state not in next_states:
            next_states.append(state)
        self.visited_states = []
        return next_states

    def get_next_states_using_policy(self, start_state, policy):
        if start_state in policy:
            next_states = self.get_next_states_by_action_ignoring_self(policy, start_state)
        else:
            next_states = []
        self.visited_states.extend(next_states)
        for state in next_states:
            next_states.extend(self.get_next_states_using_policy(state, policy))
        return next_states

    def get_next_states_by_action_ignoring_self(self, policy, state):
        direct_next_states = []
        transitions = self.transitions_by_current[state]
        action = policy[state]
        for transition in transitions:
            if action == transition.action_name and transition.next_state not in self.visited_states and state in policy:
                    direct_next_states.append(transition.next_state)
        return direct_next_states

    def mergePolicy(self, inner_policy, policy):
        for state in inner_policy:
            policy[state] = inner_policy[state]

    def getAvailableTransitions(self, states):
        available_transitions = {}
        for state in states:
            available_transitions[state] = self.transitions_by_current[state]
        return available_transitions

    def get_this_and_previous_states_using_policy(self, state, policy):
        self.visited_states = []
        previous_states = self.get_previous_states_using_policy(state, policy)
        if state not in previous_states:
            previous_states.append(state)
        self.visited_states = []
        return previous_states

    def get_previous_states_using_policy(self, state, policy):
        direct_previous_states = []
        transitions_reaching = self.transitions_by_next[state]
        for transition in transitions_reaching:
            if transition.current_state in policy and \
                    policy[transition.current_state] == transition.action_name and \
                    transition.current_state not in self.visited_states:
                direct_previous_states.append(transition.current_state)
        self.visited_states.extend(direct_previous_states)
        for state in direct_previous_states:
            direct_previous_states.extend(self.get_previous_states_using_policy(state, policy))
        return direct_previous_states

    def select_tip_state(self, tip_states):
        for state in tip_states:
            if state != self.end_state:
                tip_states.remove(state)
                return state
        return None

    def expand(self, tip_state, g_line):
        for child_transition in self.transitions_by_current[tip_state]:
            if child_transition.next_state not in g_line:
                g_line[child_transition.next_state] = self.manhattan_heuristic(child_transition.next_state)

    def manhattan_heuristic(self, state: str):
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

    def getChildren(self, state, g_line):
        children = {}
        for transition in self.transitions_by_current:
            if transition.current_state == state and transition.next_state not in children and transition.next_state != state and transition.next_state not in list(
                    g_line.keys()):
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

    def getBestChild(self, fringe_states, g_line):
        fringe_v1 = {s: g_line[s] for s in fringe_states}
        bestChild = min(fringe_states, key=lambda s: fringe_v1[s])
        return bestChild
