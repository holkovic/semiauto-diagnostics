import InputDataProcessing


def report(pcap, description):
    """
    The detected error is reported to the user.
    :param pcap: Path to the PCAP file.
    :param description: Detected error.
    """
    print(pcap, description)


def main(input_file, model):
    pairs = InputDataProcessing.process(input_file) + [(None, None)]
    previous = (None, None)
    for actual in pairs:
        if model.transition_exists(previous, actual):
            if model.transition_with_error(previous, actual):
                description = model.get_error(previous, actual)
                return report(input_file, description)
        else:
            return report(input_file, "unknown error detected")
        previous = actual

    return report(input_file, "<OK>")
