from importlib import import_module
import Arguments, Files, Model


def import_action_method(action):
    """
    Dynamically imports action module from string.
    :param action: Name of the action.
    :return: Module method object.
    """
    module_name = "Action_" + action
    module = import_module(module_name)
    method = getattr(module, "main")
    return method


def get_data_based_on_arguments(arguments):
    """
    Reads the arguments, loads the data and returns it.
    :return: dictionary containing all the required data for main process
    """
    data = {}
    data["action_method"] = import_action_method(arguments["action"])
    data["model"] = Model.Model(arguments["model"])
    data["input_files"] = Files.get_list_of_files(arguments["input"], ".pcapng")
    return data


def main():
    """
    Parses the program arguments, loads action module and executes specified action on all input data.
    """
    arguments = Arguments.parse()
    data = get_data_based_on_arguments(arguments)

    for input_file in data["input_files"]:
        data["action_method"](input_file, data["model"])

    data["model"].save()


if __name__ == '__main__':
    main()
