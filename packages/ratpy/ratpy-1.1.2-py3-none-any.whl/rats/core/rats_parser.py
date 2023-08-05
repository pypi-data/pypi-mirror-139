from rats.core.RATS_CONFIG import splitchar, dfpath, packagepath, Packet, LLCEDB, LLCEDBFormat
import rats.core.topoparser as topo
from datetime import datetime
import pandas as pd
import numpy as np
from rats.modules.errors import SamplesMissingError


class RatsParser:

    dataframe: pd.DataFrame
    valid: bool = True
    gds_protocol_version: int
    fudge: int = 2047
    errors: bool
    status_message: str = 'No errors to report'
    different_to_n_dataframes: int = 0 # USED IN SESSION DATA TRACKER

    def __init__(self, filepath=None, dataframe=None):
        self.filepath = filepath + '.txt'
        self.filename = filepath.split(splitchar)[-1].split('.')[0]
        # rats_logger.info(f'RatsParser instantiated for {self.filename}')

    def _create_partitioned_dataframe(self):
        """
        Takes the .txt file and reads it into a dataframe so that it can be sorted
        """
        series_stream = []
        with open(self.filepath, 'r') as f:
            # Create a list of every line in the .txt file
            line = f.readline()
            while line:
                series_stream.append(line.strip())
                line = f.readline()

        reject_characters = ['-', ']', ':']
        # lines in the .txt file which start with these characters can be rejected - might add to config later
        df = pd.DataFrame(series_stream, columns=['bytes'])
        df = df[~df['bytes'].str.contains('|'.join(reject_characters))]
        # Use dataframe filtering to reject any line which contains one of the characters in reject_characters
        df['index_count'] = df.index.values
        deltas = df['index_count'].diff()[1:]
        # deltas works out the diff erence between each value in index_count vs the previous value
        gaps = deltas[deltas > 1]
        # Where the difference in the index is greater than 1, a new packet started
        packet_number_dictionary = {}
        for i in range(len(gaps.index.values)):
            packet_number_dictionary[gaps.index.values[i]] = i + 1
            # gaps.index.values[i] is an index to the line on which the packets started
            # i iterates and yields the actual packet number to be mapped to the main dataframe
        df['packet_number'] = df.index.map(packet_number_dictionary)
        df.reset_index(inplace=True)
        # df.loc[:,'packet_number'].fillna(method='bfill', inplace=True)
        df.fillna(method='ffill', inplace=True)
        df['packet_number'].fillna(0,inplace=True)
        df.drop('index_count', axis=1, inplace=True)
        # rats_logger.info(f'packet numbers have been parsed and added to dataframe for {self.filename}')

        self.dataframe = df
        # =============================================================================================================

    def _separate_header_and_data(self):

        def __operation(df):
            """
            To be used on a groupby object, i.e.: GroupByObject.apply(_partition_packet_data)
            expects a dataframe constructed from only one packet of data, and splits the packet into
            the header and the datastream
            """
            data = df.bytes.tolist()
            stream = ' '.join(data).split()
            counter = 0
            packet_dictionary = {}
            for field in Packet:
                if field.name == 'DATA':
                    bytes = stream[counter:]
                else:
                    bytes = stream[counter:counter + field.number_of_bytes]

                bytes = ' '.join(bytes)
                packet_dictionary[field.field_name] = bytes
                counter += field.number_of_bytes

            return pd.DataFrame.from_records([packet_dictionary])

        try:
            self.dataframe = self.dataframe.groupby('packet_number').apply(__operation)
            self.dataframe.reset_index(inplace=True)
            self.gds_protocol_version = int(self.dataframe[Packet.ACTIVE_EDBS.field_name].iloc[0].replace(' ', ''), 16) - self.fudge # TODO: remove fudge
            # rats_logger.info(f'Packet headers successfully partitioned from packet data for file: {self.filename}')
        except:
            self.valid = False
            self.status_message += 'Failed to partition the header from the full data stream'
            # rats_logger.error(f'In the process of partitioning the data stream and assigning the samples to the relevant'
            #              f'EDBs, there was a mismatch in the assignment of packet numbers, therefore file: '
            #              f'{self.filename} could not be processed.')


        #==============================================================================================================


    def _assign_samples_to_edbs(self):
        """
        Takes a dataframe which has been partitioned into header fields and a data stream and breaks up the
        datastream, then assigns the samples to the correct EDBs
        """

        input_bytes = 4 if self.gds_protocol_version > 0 else 2
        # rats_logger.info(f'GDS protocol version for {self.filename}: {input_bytes*4}')

        # This will generate the number and 'ID' of each EDB which is active on the RATS inputs
        def __operate(df):
            try:
                active_edb_flags = f"{int(df[Packet.ACTIVE_EDBS.field_name].iloc[0].replace(' ', ''), 16):0<b}"
                flaglist = [i + 1 for i, x in enumerate(active_edb_flags) if x == '1']
                bytes = df[Packet.DATA.field_name].iloc[0].split()

                bytes = [bytes[i:i + input_bytes] for i in range(0, len(bytes), input_bytes)] # split into either 16 or 32 bit...
                bytes = [''.join(x) for x in bytes] # concat the lists in the list of lists
                bytes = [bytes[i:i + len(flaglist)] for i in range(0, len(bytes), len(flaglist))] # each edb must have an output per cycle, to this makes a list of lists for the full data from each cycle

                df_dict = df.iloc[0].drop(Packet.DATA.field_name).to_dict()
                df_dict[Packet.DATA.field_name] = bytes # reconstruct the data so that each row corresponds to one cycle


                for i in df_dict:
                    if i != Packet.DATA.field_name and type(df_dict[i]) == str:
                        df_dict[i] = df_dict[i].replace(' ', '') # remove spaces from header ascii hex


                # propagate sample rate into time column
                packet_start_time = int(df_dict[Packet.TIME_STAMP.field_name].replace(' ', ''), 16) # fetch start time...

                # =================================================
                # TODO: remove this next fudge for interscan jitter
                # packet_start_time += np.random.randint(485)
                # ================================================fint

                number_of_samples = len(bytes) # each item in bytes is the entire dataset from a single cycle
                sample_rate = int(df_dict[Packet.SAMPLE_RATE.field_name].replace(' ', ''), 16) # fetch sample rate reported in headers
                # packet_jitter = np.random.randint(485)
                propagated_time_column = [packet_start_time + (i * sample_rate) for i in range(number_of_samples)]

                llc_edb_index = flaglist.index(LLCEDB)

                llc_dictionary = {bit.name: [] for bit in LLCEDBFormat}

                for i in bytes:
                    binary_llc_edb = f"{int(i[llc_edb_index], 16):0>16b}"

                    for bit in LLCEDBFormat:
                        llc_dictionary[bit.name].append(int(binary_llc_edb[15 - bit.value]))

                df_dict[Packet.TIME_STAMP.field_name] = propagated_time_column
                df_dict[Packet.SAMPLE_RATE.field_name] = sample_rate
                df_dict[Packet.ACTIVE_EDBS.field_name] = [flaglist]

                for llc, state in llc_dictionary.items():
                    if 'BIT' in llc:
                        pass
                    else:
                        df_dict[llc] = state

                try:
                    for i, j in enumerate(df_dict[Packet.DATA.field_name]):  # Loop will pad data if there are any samples missing... just in case.
                        list = j

                        if len(list) < len(df_dict[Packet.ACTIVE_EDBS.field_name][0]):
                            raise SamplesMissingError

                except SamplesMissingError as e:
                    # need to find a way to log this and highlight to user....
                    while len(list) < len(df_dict[Packet.ACTIVE_EDBS.field_name][0]):
                        list.append('0000')
                    df_dict[Packet.DATA.field_name][i] = list

                df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in df_dict.items()]))

                df.drop('level_1', axis=1, inplace=True)

                df.fillna(method='ffill', inplace=True)


                df = df.explode([Packet.ACTIVE_EDBS.field_name, Packet.DATA.field_name])
                df[Packet.ACTIVE_EDBS.field_name] = df[Packet.ACTIVE_EDBS.field_name].astype(int)
                df = df[df[Packet.ACTIVE_EDBS.field_name] != LLCEDB]
                df[Packet.FUNCTION.field_name] = df[Packet.FUNCTION.field_name].apply(int, base=16)
                df[Packet.PACKET_COUNT.field_name] = df[Packet.PACKET_COUNT.field_name].apply(int, base=16)
                df[Packet.LLC_COUNT.field_name] = df[Packet.LLC_COUNT.field_name].apply(int, base=16)
                df.rename(columns={'index':'rats_sample'})
                return df
            except Exception as e:
                print(e)


        try:
            self.dataframe = self.dataframe.groupby('packet_count').apply(__operate)
            self.dataframe = self.dataframe.droplevel(0)
            self.dataframe.reset_index(inplace=True)
            self.valid = True
            # rats_logger.info(f'Samples and EDBs aligned for dataframe from file: {self.filename}')
        except Exception as e:
            self.valid = False
            # rats_logger.error(f'Samples and EDBs could not be aligned for dataframe from file: {self.filename}')


    def _validate_initial_partition(self, dataframe):
        """
        Take output from previous wrapper and make sure packet_number and packet_count line up, then delete packet_number
        Uses pandas built-in testing functions for now. Likely to be replaced later with better method of validation
        """
        comp1 = dataframe['packet_number'].apply(int)
        comp2 = dataframe['packet_count'].str.replace(' ', '').apply(int, base=16)
        comp1.name = 'Test'
        comp2.name = 'Test'
        try:
            pd.testing.assert_series_equal(comp1, comp2)
            self.dataframe.drop('packet_number', axis=1, inplace=True)

        except AssertionError as e:
            # rats_logger.info(e)
            # rats_logger.info('partition_packet_data did not yield valid results; packet_number and packet_count columns '
            #             'are not equal')
            self.valid = False

    def _find_outliers_hash(self):
        """
        Designed to find outliers by generating hashes of the data rather than using the mode of the mean... will use the mode
        of the hash
        maybe I want to use this as an apply... feed in dataframe grouped by function number
        Also need to hash per edb.. crap. more complicated than I thought
        """
        def __operate(df):
            hash_list = [hash(' '.join([str(llc) for llc in frame.data.tolist()])) for llc, frame in
                         df.groupby([Packet.LLC_COUNT.field_name])]

            hash_per_llc = pd.Series(hash_list, index=df[Packet.LLC_COUNT.field_name].unique())
            hash_mode = pd.Series(hash_per_llc).mode()

            df['hash'] = df[Packet.LLC_COUNT.field_name].map(hash_per_llc.to_dict())
            df['filter'] = hash_mode.values[0]
            df['anomalous'] = np.where(df['hash'] != df['filter'], 1, 0)
            df.drop(['hash', 'filter'], axis=1)
            if 1 in df['anomalous']:
                self.errors = True
                self.status_message = 'There seems to be some erroneous data in this file'
            return df

        self.dataframe = self.dataframe.groupby([Packet.FUNCTION.field_name, Packet.ACTIVE_EDBS.field_name]).apply(__operate)
        # this groups by function and EDB, so the output should be an anomalous set.. ok test without decimate
        self.dataframe.drop(['hash','filter'], axis=1, inplace=True)

    def _scale_twos_comp_values(self, dataframe):
        """
        Generic function to take a dataframe with column; Packet.DATA.field_name and work out the twos complement values
        This is applied to a groupby object in self._scale_and_rename_rats_inputs
        """
        input_bytes = 4 if self.gds_protocol_version > 0 else 2

        def to_int(x):
            x = int(x, input_bytes * 8)
            if (x & (1 << (input_bytes * 8 - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
                x = x - (1 << input_bytes * 8)  # compute negative value...
            return x

        dataframe[Packet.DATA.field_name] = dataframe[Packet.DATA.field_name].apply(to_int)


        dataframe[Packet.DATA.field_name] = ((
                    (dataframe.maximum - dataframe.minimum) * (dataframe[Packet.DATA.field_name] / (2 ** ((input_bytes * 8)))))) + \
                            ((dataframe.maximum - dataframe.minimum) / 2) + dataframe.minimum

        # dataframe.drop(['minimum','maximum'], axis=1, inplace=True)

        return dataframe

    def _scale_and_rename_rats_inputs(self):
        active_edbs = self.dataframe[Packet.ACTIVE_EDBS.field_name].unique()

        df = self.dataframe.copy()

        try:
            instanceName = self.filename.split('_')[-1].split('.')[0].replace('-','_') # everything before the extension
            instanceName='ION_GUIDE' #TODO: remove when filenames include instancename
            topodata = topo.extractscale(instanceName, active_edbs)

            print(topodata)

            df['minimum'] = df[Packet.ACTIVE_EDBS.field_name].map(topodata['minimum'])
            df['maximum'] = df[Packet.ACTIVE_EDBS.field_name].map(topodata['maximum'])
            df['units'] = df[Packet.ACTIVE_EDBS.field_name].map(topodata['units'])
            df['board'] = instanceName
            df = df.groupby([Packet.ACTIVE_EDBS.field_name]).apply(self._scale_twos_comp_values)

            # this is problematic.... need a new column ideally...
            df[Packet.ACTIVE_EDBS.field_name+'_id'] = df[Packet.ACTIVE_EDBS.field_name].map(topodata['descriptions'])

            self.dataframe = df

        except Exception as e:
            print(f'Failed to parse topography files and datasheets. Exception reported: {e}')
            df['board'] = 'UNDEFINED - UNABLE TO PARSE TOPOLOGY DATA'
            df['minimum'] = -1
            df['maximum'] = 1

            df = df.groupby([Packet.ACTIVE_EDBS.field_name]).apply(self._scale_twos_comp_values)
            df[Packet.ACTIVE_EDBS.field_name+'_id'] = df[Packet.ACTIVE_EDBS.field_name]

            self.dataframe = df

    def save_dataframe(self):
        try:
            self.dataframe.to_feather(f'{str(packagepath / dfpath / self.filename)}.feather')
        except Exception as e:
            print('Failed to save the dataframe')
            print(e)

    def load_dataframe(self):
        # use this function to load in old frames and apply topo...
        self.dataframe = pd.read_feather(f'{str(packagepath / dfpath / self.filename)}.feather')

    def parse(self):
        try:
            self.load_dataframe()
            self.valid = True
            if 1 in self.dataframe.anomalous.values:
                self.status_message = 'There seems to be some anomalous data in this file'

        except:
            if self.valid:
                start_time = datetime.now()
                self._create_partitioned_dataframe()
                self._separate_header_and_data()
                self._validate_initial_partition(self.dataframe)
            if self.valid:
                self._assign_samples_to_edbs()
                self._find_outliers_hash()
                self._scale_and_rename_rats_inputs()
                self.save_dataframe()
            else:
                print('INVALID')

            if not self.valid:
                pass

    def apply_scale(self):
        if self.valid:
            self.load_dataframe()


# Test Case
# filename = 'C:\\Users\\uksayr\\AppData\\Roaming\\JetBrains\\PyCharm2021.2\\scratches\\gds_000C00_30_14092021_1520.txt'
# filename = 'C:\\Users\\uksayr\\AppData\\Roaming\\JetBrains\\PyCharm2021.2\\scratches\\gds_000C00_2E_22112021_0958.txt'
# parser_class = RatsParser(filename)
# parser_class.parse()

