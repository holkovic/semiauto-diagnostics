import pkgutil
import InputDataProcessing
from pcapng import FileScanner


def get_pcap_description(input_file, default="<not provided>"):
    """
    Extracts the error description from the PCAPng file (comment section).
    :param input_file: Path to the PCAP file.
    :param default: When no comment is found, this value is returned.
    :return: Comment section from the PCAP or default.
    """
    description = default
    with open(input_file, "rb") as fp:
        scanner = FileScanner(fp)
        for block in scanner:
            description = block.options.get("opt_comment")
            if description is not None:
                return description
    return description


def main(input_file, model):
    pairs = InputDataProcessing.process(input_file)
    description = get_pcap_description(input_file)
    previous = (None, None)
    extended = False
    for actual in pairs:
        if model.transition_exists(previous, actual):
            if model.transition_with_error(previous, actual):
                model.update_error_description(previous, actual, description)
                extended = True
                break
        else:
            model.create_error(previous, actual, description)
            extended = True
            break
        previous = actual

    if not extended:  # now check whether the last state is finite state
        if model.transition_exists(previous, (None, None)):
            if model.transition_with_error(previous, (None, None)):
                model.update_error_description(previous, (None, None), description)
                extended = True
            else:
                print(input_file, "error not detectable, model not extended")
        else:
            model.create_error(previous, (None, None), description)
            extended = True

    if extended:
        model.save()
