# analyzeHL7

The goal of this program is to use the hl7 library to build a parser that returns an HL7 ADT type message as a dictionary for future processing. There will be a minimum three classes:

1. AO3 - This will take in a single message and return specified fields in a dictionary.
2. A03dir - This will return a dictionary of dictionaries of all of the messages in a folder.It will use but not inherit form ADTmessage.
3. A03df - This will return a dataframe from the dictionary of dictionaries that were created in ADTdir.

As far limitations, the goal of this tool will be to build sufficient capacity to better analyze HL7 ADT messages in python. It will initially focus only on A03 (discharge) messages as most of the data from the admission messages exist in the discharge as well.

It is hoped that it can be built upon later with other message types (test results and scheduling messages for example).

An ideal workflow would be to use it in Jupyter to then clean and perform analytic operations on sets of messages to derive insights. 

