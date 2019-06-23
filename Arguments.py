import argparse


def parse():
    """
    Parse the program arguments.
    :return: Arguments dictionary.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to the input PCAP file or directory with PCAP files")
    ap.add_argument("-m", "--model", required=True, help="path to the protocol model file")
    ap.add_argument("-a", "--action", required=True, choices=['learn', 'extend', 'diagnose'], help="what should be done with input data")
    arguments = vars(ap.parse_args())
    return arguments
