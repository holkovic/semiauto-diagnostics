import ast
from Model2Dot import Model2Dot
import Files
import json


class Model(Model2Dot):

    def __init__(self, path):
        super().__init__()
        self._transitions = {}
        self._errors = {}
        self._path = path
        self._already_generated_nodes = []
        self.load_json()

    def __str__(self):
        result = "OK: " + str(self._transitions) + "\n"
        result += "ERROR: " + str(self._errors) + "\n"
        return result

    def _count_state(self, state):
        """
        Checks whether the state was already counted and if not, increase the counter of unique states.
        :param state: Name of the state.
        """
        if state not in self.counted_states:
            self.counted_states.append(state)
            self.state_count += 1

    def _count_states(self):
        """
        Calculate amount of unique states.
        :return: Number of states.
        """
        self.counted_states = []
        self.state_count = 0
        for transition in self._transitions:
            states = ast.literal_eval(transition)
            self._count_state(states[0])
            self._count_state(states[1])
        return self.state_count

    def print_stats(self):
        """
        Print size statistics of the model (states, transitions).
        """
        states_count = self._count_states()
        transitions_count = len(self._transitions)
        print(str(states_count)+","+str(transitions_count))

    def load_json(self):
        """
        Load model from the JSON file.
        """
        try:
            serialized_data = Files.load_file(self._path)
            data = json.loads(serialized_data)
            self._transitions = data[0]
            self._errors = data[1]
        except:
            self._transitions = {}
            self._errors = {}

    def export_json(self):
        """
        Save model into JSON file.
        """
        data = (self._transitions, self._errors)
        json_data = json.dumps(data)
        Files.save_file(self._path, json_data)

    def save(self):
        """
        Export the model into JSON and dot format.
        """
        self.export_dot()
        self.export_json()

    def _create_key(self, state_from, state_to):
        """
        Creates a string key from previous and next state.
        :param state_from: Name of the previous state.
        :param state_to: Name of the next state.
        :return: String representing the key.
        """
        key = (state_from, state_to)
        return str(key)

    def add_transition(self, state_from, state_to):
        """
        Create correct transition between two states.
        :param state_from: Name of the previous state.
        :param state_to: Name of the next state.
        """
        key = self._create_key(state_from, state_to)
        self._transitions[key] = "ok"

    def transition_exists(self, state_from, state_to):
        """
        Checks where a transition exists between two states.
        :param state_from: Name of the previous state.
        :param state_to: Name of the next state.
        :return: Boolean, exists or not.
        """
        key = self._create_key(state_from, state_to)
        return key in self._transitions

    def transition_with_error(self, state_from, state_to):
        """
        Checks whether a error transition exists between two states.
        :param state_from: Name of the previous state.
        :param state_to: Name of the next state.
        :return: Boolean, exists with error or not.
        """
        key = self._create_key(state_from, state_to)
        if key in self._transitions and self._transitions[key] == "error":
            result = True
        else:
            result = False
        return result

    def create_error(self, state_from, state_to, description):
        """
        Mark correct transition with error and save error description.
        :param state_from: Name of the previous state.
        :param state_to: Name of the next state.
        :param description: Error description.
        """
        key = self._create_key(state_from, state_to)
        self._transitions[key] = "error"
        self._errors[key] = description

    def update_error_description(self, state_from, state_to, description):
        """
        If the error description is new, adds it into the error transition.
        :param state_from: Name of the previous state.
        :param state_to: Name of the next state.
        :param description: Error description.
        """
        key = self._create_key(state_from, state_to)
        old_description = self._errors[key]
        if ";" + description + ";" not in ";" + old_description + ";":
            new_description = old_description + "; " + description
            self._errors[key] = new_description

    def get_error(self, state_from, state_to):
        """
        Finds and returns saved error description on the transition.
        :param state_from: Name of the previous state.
        :param state_to: Name of the next state.
        :return: Error description.
        """
        key = self._create_key(state_from, state_to)
        return self._errors[key]
