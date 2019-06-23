# Semi-automatic diagnostic tool

**Author:** Martin Holkovic, iholkovic@fit.vutbr.cz

**Description:** The idea behind this tool was published in the DCNET 2019 conference.

## Notes
- Only PCAP files in pcapng format are supported (old format doesn't support comments).
- The tool also exports a model into a format suitable for the dot linux tool. This file has the suffix .dot appended after the model file. To generate PNG file showing the model, use: `dot -Tpng PATH1 -o PATH2`, where PATH1 = model with .dot suffix; PATH2 = path to the location where the PNG should be exported.
- When a new protocol should be added, add request-reply Wireshark's field names into `field_names.txt` file.


## How to use the tool:

1) Train the tool on correct communication(s):

`python3 sa-diag.py -i PATH1 -m PATH2 -a learn`

2) Extend the correct model with error communication(s):

`python3 sa-diag.py -i PATH1 -m PATH2 -a extend`

3) Use the model to diagnose an unknown communication(s):

`python3 sa-diag.py -i PATH1 -m PATH2 -a diagnose`

Where:
* *PATH1 is path to the PCAP file or directory with PCAP files*
* *PATH2 is the location where the model is expected and/or the model is exported*