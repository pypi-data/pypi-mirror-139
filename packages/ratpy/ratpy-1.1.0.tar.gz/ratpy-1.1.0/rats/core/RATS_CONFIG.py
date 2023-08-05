"""
This configuration file is used to define the expected structure of the data packets

Contents are defined in order of appearance and have a number of bytes associated with them
"""
import os.path
import pathlib
import logging
import datetime
from enum import Enum

class PlotBanks(Enum):
    def __init__(self, designation, number_of_plot_banks):
        self.designation = designation
        self.number_of_plot_banks = number_of_plot_banks
    """Defines the number of plot banks that each app displays"""
    DASHBOARD = "dashboard_app_",2
    SCOPE_APP = "scope_app_",10
    INTERSCAN_APP = "interscan_app_",10
    DATA_MANAGEMENT_APP = "data_management_app_",1 # number_of_plot_banks redundant for this app

#=====================================================================================================================
#                              PACKET FORMAT CONFIGURATION
#=====================================================================================================================
class Packet(Enum):
    #=====================================================================================
    # define modified enum class to handle multiple attribute assignment
    # DO NOT MODIFY
    def __init__(self, field_name, number_of_bytes):
        self.field_name = field_name
        self.number_of_bytes = number_of_bytes
    #=====================================================================================
    """
    The order of appearance of these fields should match the expected format of the RATS .txt file
    the Enum property names SHOULD NOT be changed
    
    Attribute format; PROPERTY = field_name, number_of_bytes
    """
    PROTOCOL = "rats_gds_protocol_version", 1
    PAYLOAD_SIZE = "payload_size", 1
    PACKET_COUNT = "packet_count", 2
    TIME_STAMP = "time", 6
    SAMPLE_RATE = "rats_sample_rate", 2
    LLC_COUNT = "llc_trigger_count", 4
    FUNCTION = "function_number", 2
    SAMPLE = "sample_number", 2
    BARCODE_HASH = "barcode_hash", 4
    RETENTION_TIME = "retention_time", 4
    RESERVED = "reserved", 2
    ACTIVE_EDBS = "EDB", 2

    # ============================================================
    DATA = "data", 0 # Do not modify the order or size of this entry



#=====================================================================================================================
#                              LLC CONFIGURATION
#=====================================================================================================================

#   ON WHICH EDB DO WE EXPECT TO FIND THE LLC STATES, THIS IS UNLIKELY TO CHANGE, SO DON'T MESS WITH THIS
LLCEDB = 1

class LLCEDBFormat(Enum):
    """
    CHANGE THE ENUM PROPERTY NAMES TO DEFINE THE ACTIVE LLCS. ANY PROPERTY WITH 'BIT' IN ITS NAME WILL NOT BE STORED
    BY THE PARSING OPERATION.
    """
    BIT0 = 0
    BIT1 = 1
    BIT2 = 2
    BIT3 = 3
    BIT4 = 4
    BIT5 = 5
    BIT6 = 6
    BIT7 = 7
    BIT8 = 8
    BIT9 = 9
    SIP = 10  # SIP is recorded on bit 10
    BIT11 = 11
    BUFFIS = 12 # BUFFIS is recorded on bit 12
    BIT13 = 13
    BIT14 = 14
    BIT15 = 15

#=====================================================================================================================
#                              FILE PATH CONFIGURATION
#=====================================================================================================================
'''names of the relevant subdirectories under the rats directory'''

packagepath = pathlib.Path(__file__).parent.parent.resolve()
splitchar = os.path.sep
cachepath = 'cache'
dfpath = 'feathereddataframes'
figurepath = 'pickledfigures'
topopath = 'topo'
logs = 'logs'
