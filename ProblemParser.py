import re
import string

from Transition import Transition


class ProblemParser:
    states = {}
    transitions_by_current = {}
    transitions_by_next = {}
    initial_state = None
    goal_state = None
    actions_available = []

    def __init__(self, file_path):
        file = open(file_path)
        text = file.read()
        self.states = self.get_items_from_until(text, "states", "endstates")
        self.initial_state = self.get_items_from_until(text, "initialstate", "endinitialstate")[0]
        self.goal_state = self.get_items_from_until(text, "goalstate", "endgoalstate")[0]
        self.fill_transitions(text, "action", "endaction")
        self.fill_costs(self.transitions_by_current, text, "cost", "endcost")

    @staticmethod
    def get_items_from_until(text, start, end):
        text = text.translate({ord(c): None for c in string.whitespace})
        text_between = re.search(start + '(.*)' + end, text).group(1)
        items = text_between.split(",")
        return items

    # action test
    # current_state next_state probability
    # endaction
    def fill_transitions(self, text, start, end):
        self.transitions_by_next = {}
        self.transitions_by_current = {}
        action_groups = re.findall(start + '(.+?)' + end, text, flags=re.DOTALL)
        for action_group in action_groups:
            action_lines = list(filter(None, action_group.splitlines()))
            # first line is the action name
            first_line = action_lines[0]
            action_name = first_line.strip()
            self.actions_available = action_name
            action_lines.remove(first_line)
            # next lines are the transitions
            for line in action_lines:
                line_items = line.split(" ")
                current_state = str(line_items[0]).strip()
                next_state = str(line_items[1]).strip()
                probability = float(str(line_items[2]).strip())
                transition = Transition(action_name, current_state, next_state, probability, 0)
                if transition.current_state in self.transitions_by_current:
                    self.transitions_by_current[transition.current_state].append(transition)
                else:
                    self.transitions_by_current[transition.current_state] = [transition]
                if transition.next_state in self.transitions_by_next:
                    self.transitions_by_next[transition.next_state].append(transition)
                else:
                    self.transitions_by_next[transition.next_state] = [transition]

    @staticmethod
    def fill_costs(transitions, text, start, end):
        cost_group = re.search(start + '(.+?)' + end, text, flags=re.DOTALL).group(1)
        cost_lines = list(filter(None, cost_group.splitlines()))
        for line in cost_lines:
            line_items = line.split(" ")
            current_state = str(line_items[0]).strip()
            action_name = str(line_items[1]).strip()
            cost = float(str(line_items[2]).strip())
            for transition in transitions[current_state]:
                if transition.action_name == action_name:
                    transition.cost = cost
