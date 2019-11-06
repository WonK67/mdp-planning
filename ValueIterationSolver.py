from Transition import Transition


class ValueIterationSolver:

    states = []
    transitions = []
    actions = []

    def __init__(self, states, transitions):
        self.states = states
        self.transitions = transitions
        self.actions = self.get_actions_available()
        v = self.value_iteration()
        pi = self.best_policy(v)
        print(v)
        print(pi)

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

    def value_iteration(self):
        states = self.states
        v1 = {s: 0 for s in states}
        while True:
            v = v1.copy()
            delta = 0
            for s in states:
                #Bellman update, update the utility values
                v1[s] = min([sum([t.probability * (t.cost + v[t.next_state]) for t in self.get_transitions(s, a)]) for a in self.get_actions(s)])
                delta = max(delta, abs(v1[s] - v[s]))
                print(delta)
            if delta < 0.1:
                return v

    def best_policy(self, v):
        states =  self.states
        actions = self.actions
        pi = {}
        for s in states:
            pi[s] = max(self.get_actions(s), key=lambda a: self.expected_utility(a, s, v))
        return pi

    def expected_utility(self, a, s, v):
        return sum([t.probability * v[t.next_state] for t in self.get_transitions(s, a)])