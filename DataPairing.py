
def process(messages):
    """
    Implements Data Pairing pipeline.
    :param messages: Sequence of detected queries and replies.
    :return: List of paired queries with replies.
    """
    result = []
    query = (None, True)  # each query consists of value and flag if it was paired
    for message in messages:
        m_type = message[0]
        m_value = message[1]
        if m_type == "query":
            if not query[1]:  # new query but the last one was not paired
                result.append((query[0], None))  # pair with None reply
            query = (m_value, False)
        elif m_type == "reply":
            result.append((query[0], m_value))
            query = (query[0], True)  # update the flag that query was paired
    if not query[1]:  # unpaired query at the end of conversation
        result.append((query[0], None))
    return result
