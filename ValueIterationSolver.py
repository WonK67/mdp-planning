from Transition import Transition
import timeit

class ValueIterationSolver:

    states = {}
    transitions = []
    actions = []
    last_run_duration = 0
    last_run_v_function = {}
    last_run_policy = {}

    def __init__(self, states, transitions):
        self.states = states
        self.transitions = transitions
        self.actions = self.get_actions_available()

    def get_transitions(self, state, action):
        state_transitions = []
        for transition in self.transitions:
            if transition.current_state == state and transition.action_name == action:
                state_transitions.append(transition)
        return state_transitions

    def get_actions_available(self):
        actions = []
        for transition in self.transitions:
            if transition.action_name not in actions:
                actions.append(transition.action_name)
        return actions

    def get_actions(self, state):
        actions = []
        for transition in self.transitions:
            if transition.current_state == state:
                if transition.action_name not in actions:
                    actions.append(transition.action_name)
        return actions

    def run(self):
        start = timeit.default_timer()
        self.last_run_v_function = self.value_iteration()
        self.last_run_policy = self.best_policy(self.last_run_v_function)
        stop = timeit.default_timer()
        self.last_run_duration = stop - start

    def value_iteration(self):
        v1 = {s: 0 for s in self.states}
        while True:
            v = v1.copy()
            delta = 0
            for s in self.states:
                #Bellman update, update the utility values
                v1[s] = min(self.expected_utility(a, s, v) for a in self.get_actions(s))
                delta = max(delta, abs(v1[s] - v[s]))
            if delta < 0.01:
                return v

    def best_policy(self, v):
        states = self.states
        pi = {}
        for s in states:
            pi[s] = min(self.get_actions(s), key=lambda a: self.expected_utility(a, s, v))
        return pi

    def expected_utility(self, a, s, v):
        return sum([t.probability * (t.cost + v[t.next_state]) for t in self.get_transitions(s, a)])