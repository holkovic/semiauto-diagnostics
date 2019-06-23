
import Files


def get_field_names(field_names_file):
    """
    Loads content of the protocol field names dictionary.
    :param field_names_file: Path to the file.
    :return: Dictionary of protocol fields.
    """
    result = {}
    file_content = Files.load_file(field_names_file)
    lines = file_content.split("\n")
    for line in lines:
        parts = line.split(";")
        if len(parts) >= 2:
            result[parts[0]] = (parts[1], parts[2])
    return result


def detect_protocol_and_get_its_field_names(packet, field_names):
    """
    Tries to find first protocol with defined field names.
    :param packet: Packet from Packets Parser stage.
    :param field_names: Dictionary with known protocols and their field names.
    :return: Protocol field names of the first detected protocol, None otherwise.
    """
    for field_name in field_names:
        if field_name in packet:
            return field_names[field_name]
    return None


def find_requests_and_replies(packet, protocol_fields):
    """
    Tries to find requests and replies in input data.
    :param packet: JSON data from Packets Parser
    :param protocol_fields: Tuple of query and reply field names.
    :return: Detected queries and replies inside the packet data.
    """
    result = []
    field_types = [("query", protocol_fields[0]), ("reply", protocol_fields[1])] # {protocol_fields[0]: "query", protocol_fields[1]: "reply"}
    for field in field_types:
        field_type = field[0]
        field_name = field[1]
        if field_name in packet:
            for value in packet[field_name]:
                if len(value) <= 6:
                    result.append((field_type, value))
    return result


def process(json_data, field_names_file):
    """
    Implements input data filtering pipeline.
    :param json_data: Data from Packets Parser stage.
    :return: List of detected queries and replies.
    """
    result = []
    field_names = get_field_names(field_names_file)
    protocol_fields = None
    for packet in json_data:
        if protocol_fields is None:  # looking for protocol
            protocol_fields = detect_protocol_and_get_its_field_names(packet, field_names)
        if protocol_fields is not None:  # protocol detected
            result += find_requests_and_replies(packet, protocol_fields)
    if protocol_fields is None:
        raise Exception("No known protocol has been detected.")
    return result
