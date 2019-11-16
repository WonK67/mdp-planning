from Transition import Transition
import timeit

class ValueIterationSolver:

    states = {}
    transitions: dict = {}
    actions = []
    last_run_duration = 0
    last_run_v_function = {}
    last_run_policy = {}
    initial_v = None

    def __init__(self, actions_available, states, transitions, initial_v = None):
        self.states = states
        self.transitions = transitions
        self.actions = actions_available
        if initial_v is None:
            self.initial_v = {s: 0 for s in self.transitions.keys()}
        else:
            self.initial_v = initial_v

    def get_transitions(self, state, action):
        state_transitions = []
        for transition in self.transitions[state]:
            if transition.action_name == action:
                state_transitions.append(transition)
        return state_transitions

    def get_actions_available(self):
        actions = []
        for transition in self.transitions:
            if self.transitions[transition].action_name not in actions:
                actions.append(transition.action_name)
        return actions

    def get_actions(self, state):
        actions = []
        for transition in self.transitions[state]:
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
        v1 = self.initial_v
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

    def get_states_from_transitions(self):
        states = []
        for transition in self.transitions:
            if transition.current_state not in states:
                states.append(transition.current_state)
            if transition.next_state not in states:
                states.append(transition.next_state)
        return states
