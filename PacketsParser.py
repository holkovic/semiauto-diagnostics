import json
import Cmd, Files


def _get_fields(field_names_file):
    """
    Loads content of the file and extracts the field names.
    :param field_names_file: Path to the file with defined field names.
    :return: List of field names.
    """
    result = []
    file_content = Files.load_file(field_names_file)
    lines = file_content.split("\n")
    for line in lines:
        parts = line.split(";")
        result += parts
    result = list(filter(None, result))  # remove empty elements
    return result


def _create_fields_filter(field_names_file):
    """
    Based on the defined field names generates arguments for tshark filtering.
    :param field_names_file:  Path to the file with defined field names.
    :return: Tshark arguments in string format.
    """
    fields_list = _get_fields(field_names_file)
    result = ""
    for field in fields_list:
        result += " -e " + field
    return result


def _create_command_with_params(pcap_file, field_names_file):
    """
    Creates a command with arguments.
    :param pcap_file: Path to the PCAP file.
    :param field_names_file: Path to the file with defined field names.
    :return: Command line command.
    """
    command = "tshark"
    command += " -r " + pcap_file
    command += " -T json"
    command += _create_fields_filter(field_names_file)
    return command


def _extract_protocol_layers(deserialized_data):
    """
    Removes unnecessary values from packets dictionaries.
    :param deserialized_data: Deserialized data from tshark.
    :return: List of filtered packets in dictionary format.
    """
    packets_filtered = []
    for packet in deserialized_data:
        packets_filtered.append(packet["_source"]["layers"])
    return packets_filtered


def process(pcap_file, field_names_file):
    """
    Run tshark and exports its output.
    :return: JSON data.
    """
    command = _create_command_with_params(pcap_file, field_names_file)
    tshark_data = Cmd.run_command(command)
    deserialized_data = json.loads(tshark_data)
    extracted_data = _extract_protocol_layers(deserialized_data)
    return extracted_data
