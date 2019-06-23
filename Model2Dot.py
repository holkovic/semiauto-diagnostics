import ast

import Files


class Model2Dot:

    def __init__(self):
        self._dot_suffix = ".dot"

    def _get_error_index(self, state_from, state_to):
        """
        Converts error into error index used in error labels table.
        :param state_from: Name of the previous state.
        :param state_to: Name of the next state.
        :return: Index of the error.
        """
        key = self._create_key(state_from, state_to)
        index_beginning_zero = list(self._errors.keys()).index(key)
        index_beginning_one = index_beginning_zero + 1
        return index_beginning_one

    def _create_label_from_state_part(self, part):
        """
        Create user-friendly names.
        :param part: Name.
        :return: User-friendly name.
        """
        if part is None:
            return "Ø"
        else:
            return part

    def _create_label_from_state(self, state):
        """
        Create user-friendly state name.
        :param state: State name.
        :return: User-friendly state name.
        """
        part_1 = self._create_label_from_state_part(state[0])
        part_2 = self._create_label_from_state_part(state[1])
        result = part_1 + ", " + part_2
        return result

    def _generate_dot_state(self, node):
        """
        Generates model states in format for generating image with dot tool.
        :param node: Name of the state.
        :return: String with model data.
        """
        if node == (None, None) or node in self._already_generated_nodes:
            return ""

        label = self._create_label_from_state(node)
        if self.transition_with_error(node, (None, None)):
            color = "red"
            label += "\\n" + "#" + str(self._get_error_index(node, (None, None)))
        else:
            color = "black"

        self._already_generated_nodes.append(node)

        test_key = self._create_key(node, (None, None))
        if test_key in self._transitions:  # finite state
            shape = "doublecircle"
        else:
            shape = "circle"

        index = self._already_generated_nodes.index(node)

        return """
    node [shape = {}, label="{}", color="{}"] {};""".format(shape, label, color, index)

    def _generate_dot_transition(self, previous, actual):
        """
        Generates model transitions in format for generating image with dot tool.
        :param previous: Name of the previous state.
        :param actual: Name of the next state.
        :return: String with model data.
        """
        label = "label=\"" + str(actual)
        if self.transition_with_error(previous, actual):
            color = "red"
            label += "\\n#" + str(self._get_error_index(previous, actual))
        else:
            color = "black"
        label += "\","

        if previous == (None, None):
            result = """
    init -> {};""".format(self._already_generated_nodes.index(actual))
        elif actual == (None, None):
            result = ""
        else:
            result = """
    {} -> {}[{} color="{}"];""".format(self._already_generated_nodes.index(previous), self._already_generated_nodes.index(actual), label, color)
        return result

    def _generate_dot_error_labels(self):
        """
        Generates error descriptions in format for generating image with dot tool.
        :return: String with model data.
        """
        index = 1
        result = ""
        for error in list(self._errors.keys()):
            result += str(index) + ": " + self._errors[error] + """
"""
            index += 1
        return result

    def _generate_dot_states_and_transitions(self):
        """
        Generates model states and transitions in format for generating image with dot tool.
        :return: String with model data.
        """
        result = ""
        self._already_generated_nodes = []
        for transition in self._transitions:
            states = ast.literal_eval(transition)
            result += self._generate_dot_state(states[0])
            result += self._generate_dot_state(states[1])
            result += self._generate_dot_transition(states[0], states[1])
        return result

    def generate_dot_file(self):
        """
        Generates model in format for generating image with dot tool
        :return: String with model data.
        """
        result = """digraph finite_state_machine {
    rankdir=LR;
    labeljust=l;
    label=\""""
        result += self._generate_dot_error_labels()
        result += """\";

    node [shape = point ]; init"""
        result += self._generate_dot_states_and_transitions()
        result += """
}"""
        return result

    def export_dot(self):
        """
        Generates model in format for generating image with dot tool and saves it into file.
        """
        data = self.generate_dot_file()
        dot_file = self._path + self._dot_suffix
        Files.save_file(dot_file, data)
