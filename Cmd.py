from subprocess import Popen, PIPE


def convert_command_to_arguments(command_line):
    """
    Converts command line to list of arguments, where 1 item = 1 command parameter.
    Be aware that some parameters can consists of multiple words (ex.: -Y "not tcp and not udp").
    :param command_line: Command line.
    :rtype: List of arguments for Popen.
    """
    argument_list = []
    command_line += "\""
    part = command_line.split("\"")
    for i in range(0, int(len(part) / 2)):
        argument_list += part[i * 2].strip().split(" ")
        if part[i * 2 + 1] != "":
            argument_list += [part[i * 2 + 1]]
    argument_list = [x for x in argument_list if len(x)]
    return argument_list


def run_command(command_line):
    """
    Runs command line and returns both STDIN and STDERR.
    :param command_line: Command line.
    :return: Returned STDIN as string.
    """
    argument_list = convert_command_to_arguments(command_line)
    p = Popen(argument_list, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    cmd_output = p.communicate()
    stdout = cmd_output[0].decode("utf-8")
    return stdout
