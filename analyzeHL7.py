import hl7
import os
import numpy
import pandas as pd
class A03:
    """
    This class will take an A03 in the hl7-python API object format. I will extract a series of values from it, convert them to strings,
    and return a dictionary. The DG1 segment(s) will return as a dictionary as there are often more than one DG1 segments.
    There may be None values when an IndexError exception is called.
    """
    def __init__(self,h):
        self.__result_dict  = dict() #store the message data
        self.__result_dict  = dict() #create a dictionary to store the message results
        try:
            self.__result_dict ['facility_name'] = str(h['MSH'][0][4]).split("^")[0] #get the facility name
        except IndexError:
            self.__result_dict ['facility_name'] = str(h['MSH'][0][4])
        self.__result_dict ['message_date_time'] = str(h['MSH'][0][7])#get the message D/T
        self.__result_dict ['message_type'] = str(h['MSH'][0][9]) #get the message type
        self.__result_dict ['control_id'] = str(h['MSH'][0][10]) #get the control_id
        self.__result_dict ['last_name'] = str(h['PID'][0][5]).split("^")[0] #get the last name
        self.__result_dict ['first_name'] = str(h['PID'][0][5]).split("^")[1] #get the first name
        try:
            self.__result_dict ['middle_name'] = str(h['PID'][0][5]).split("^")[2] #get the middle_name
        except IndexError:
            self.__result_dict ['middle_name'] = None
        self.__result_dict ['date_of_birth'] = str(h['PID'][0][7]) #get the dob
        self.__result_dict ['gender'] = str(h['PID'][0][8]) #get gender
        self.__result_dict ['zip_code'] = str(h['PID'][0][11]).split("^")[4] #get zip code
        try:
            self.__result_dict ['common_key'] = str(h['PID'][0][3]).split("^")[8].split("~")[1] #get the common key - a Michigan-centric identifier.
        except IndexError:
            self.__result_dict ['common_key'] = None
        self.__result_dict ['patient_class'] = str(h['PV1'][0][2]) #get the patient class - an overall categorization of the visit - inpatient, outpatient, ER, etc...
        self.__result_dict ['service_type'] = str(h['PV1'][0][10]) #get the type of service rendered
        self.__result_dict ['admit_source'] = str(h['PV1'][0][14]) #get the source of the admission
        self.__result_dict ['admit_date_time'] = str(h['PV1'][0][44])
        self.__result_dict ['discharge_date_time'] = str(h['PV1'][0][45]).replace("\n","")
        #create a dictionary for the DG1 segment(s)
        number_of_dx = len(h['DG1']) #each dg1 segment is its own dictionary
        self.__dg_segment = "" #create blank string to temporarily store the DG data as the segment is being parsed.
        #new
        try:
            if number_of_dx == 1:
                self.__dg_segment = str(h['DG1'][0][3]).split("^")[0]
            else:
                for dg_segment_number in range(0,number_of_dx):
                    self.__dg_segment = self.__dg_segment + str(h['DG1'][dg_segment_number][3]).split("^")[0] + ","
        except:
            pass
        finally:    
            if len(self.__dg_segment) > 0 and self.__dg_segment[-1] == ",":
                self.__result_dict ['dx'] = self.__dg_segment[0:-1]
            else:
                self.__result_dict ['dx'] = self.__dg_segment[0:-1]
            del h #get rid of the message object
    def get_message(self):
        """
        Returns the dictionary
        """
        return self.__result_dict
class A03dir():
    """
    This class will search through a directory, produce a list of the files in a given directory.
    Then it will check each file to see if it is parseable as an HL7 message.
    HL7 messages will then be tested to see if they are A03s.
    A03s will be parsed and returned as dictionary of dictionaries.
    """
    def __init__(self,path):
        self.__path = path #the directory to search.
        self.__dir_file_listing = self.__get_file_list()
        self.__remove_non_readable_files()

    def __get_file_list(self):
        """
        Returns the files in the directory passed to the __init__() method
        """
        self.__file_list = list()
        for (dirpath, dirnames, filenames) in os.walk(self.__path): #searches the directory path and returns only the files.
            self.__file_list.extend(filenames)
            return self.__file_list
    def __remove_non_readable_files(self):
        """
        Removes the items from the list of files that cannot be parsed with the file open() method.
        """
        for file_item in self.__dir_file_listing:
            if os.access(file_item,os.R_OK) == False: ##os.access will return False for any reason if the file cannot be open. No try/catch required.
                self.__dir_file_listing.remove(file_item)
    def process_list(self):
        """
        Iterates through the list of readable files and returns a dictionary of dictionaries of the fields from the files.
        Files are first checked to see if they are parseable as HL7 files.
        """
        return_dict = dict()
        for readable_file in self.__dir_file_listing:
            try:
                f = open(readable_file,"r")
                first_line = f.readline() #grab the first line
                first_line = first_line + "\r"
                if hl7.ishl7(first_line) == True:
                    message = ""
                    f.seek(0,0)
                    for line in f:
                       # print(line)
                        message = message + line + "\r"
                    f.close()
                else: # Talk about this.
                    continue
                h = hl7.parse(message) #parse the message
                if str(h['MSH'][0][9]) == 'ADT^A03': #check if the message is an ADT discharge
                    msg = A03(h)
                    return_dict[readable_file] = msg.get_message()
            except:
                continue
        return return_dict
class A03df:
    """
    This class will use A03dir (and A03) to create and return a dataframe from the result dictionary.
    This can then be used for future analysis.
    """
    def __init__(self,h):
        self.__current_directory = h
        self.__dir = A03dir(self.__current_directory)
        self.__message_directory = self.__dir.process_list()
        
    def return_df(self):
        """
        Returns the dataframe
        """
        return pd.DataFrame.from_dict(self.__message_directory,orient='index')









