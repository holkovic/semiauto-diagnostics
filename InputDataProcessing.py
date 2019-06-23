
import PacketsParser
import DataFilter
import DataPairing

field_names_file = "field_names.txt"


def process(input_file):
    """
    Implements PCAP file processing pipeline.
    :param input_file: Path to the PCAP file.
    :return: List of query-reply pairs.
    """
    json_data = PacketsParser.process(input_file, field_names_file)
    messages = DataFilter.process(json_data, field_names_file)
    pairs = DataPairing.process(messages)
    return pairs
