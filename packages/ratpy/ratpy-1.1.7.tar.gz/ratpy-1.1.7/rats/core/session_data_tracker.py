import pandas as pd
import os
from rats.core.RATS_CONFIG import Packet, splitchar

class SessionDataTracker:
    '''This class is instantiated in rats.core.app'''
    data_files: pd.DataFrame = pd.DataFrame(columns=['File','Log'])
    topo_files: pd.DataFrame = None

    def __init__(self, data_directory, parser):
        self.data_directory = data_directory + splitchar
        self.parser = parser

    def scan_for_files(self):
        """Checks for .txt files in the specified data directory, then adds the files to the data_files dataframe"""
        file_list = [str(filename) for filename in os.listdir(self.data_directory)
                     if '.txt' in filename]
        temp_file_frame = pd.DataFrame(dict(File=[file.split('.')[0] for file in file_list], Log=['not processed'] * len(file_list)))

        if self.data_files is None:
            self.data_files = temp_file_frame
        else:
            # filter the temp file dataframe to exclude already present files, then append to the data_files frame
            temp_file_frame = temp_file_frame[~temp_file_frame['File'].isin(self.data_files['File'].values)]
            self.data_files = self.data_files.append(temp_file_frame, ignore_index=True)


    def parse_data_files(self):
        """Use the parser passed to this class to parse the files"""
        if self.data_files.empty:
            pass
        # dumb... basically this now does nothing...
        else:
            for name in self.data_files.File.values:
                parser_class = self.parser(self.data_directory+name)
                parser_class.parse()
                self.data_files.loc[self.data_files['File'] == name, 'Log'] = parser_class.status_message

                name = name+'.txt'
                if os.path.isfile(self.data_directory+name) or os.path.islink(self.data_directory+name):
                    os.unlink(self.data_directory+name)
                    print(f'{name} parsed and deleted from cache')



    def compare_data_files(self):
        if not self.data_files.empty:
            for name in self.data_files.File.values:
                parser_1 = self.parser(self.data_directory+name)
                parser_1.parse()
                parser_1.dataframe = parser_1.dataframe[[Packet.LLC_COUNT.field_name, Packet.FUNCTION.field_name]]
                parser_1.dataframe.drop_duplicates(inplace=True)

                for second_name in self.data_files.File.values:
                    if second_name != name:
                        parser_2 = self.parser(self.data_directory+second_name)
                        parser_2.parse()
                        parser_2.dataframe = parser_2.dataframe[[Packet.LLC_COUNT.field_name, Packet.FUNCTION.field_name]]
                        parser_2.dataframe.drop_duplicates(inplace=True)

                        if not parser_1.dataframe[Packet.FUNCTION.field_name].equals\
                        (parser_2.dataframe[Packet.FUNCTION.field_name]):
                            parser_1.different_to_n_dataframes += 1

                if parser_1.different_to_n_dataframes == 1 and len(self.data_files.File.values) < 3:
                    # There are only two files, so
                    status_message = f'\n{Packet.LLC_COUNT.field_name} vs {Packet.FUNCTION.field_name} ' \
                                     f'differs from the other file.'
                elif parser_1.different_to_n_dataframes > 1:
                    status_message = f'\n{Packet.LLC_COUNT.field_name} vs {Packet.FUNCTION.field_name} ' \
                                     f'differs from more than one other file.'
                else:
                    status_message=''

                # needs some work....
                self.data_files.loc[self.data_files['File'] == name, 'Log'] = self.data_files['Log'] + \
                                                                              f'\n{status_message}'

    def save_session_data(self):
        if self.data_files is None:
            pass
        elif self.data_files.empty:
            pass
        else:
            self.data_files.to_feather(self.data_directory + 'sessionfilenames')

    def load_session_data(self):
        self.data_files = pd.read_feather(self.data_directory + 'sessionfilenames')
