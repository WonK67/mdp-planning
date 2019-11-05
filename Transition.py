class Transition:

    action_name = None
    cost = None
    current_state = None
    next_state = None
    probability = None

    def __init__(self, action_name, current_state, next_state, probability, cost):
        self.action_name = action_name
        self.current_state = current_state
        self.next_state = next_state
        self.probability = probability
        self.cost = cost