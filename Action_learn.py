import InputDataProcessing


def main(input_file, model):
    pairs = InputDataProcessing.process(input_file)
    previous = (None, None)
    for actual in pairs:
        model.add_transition(previous, actual)
        previous = actual
    model.add_transition(previous, (None, None))
