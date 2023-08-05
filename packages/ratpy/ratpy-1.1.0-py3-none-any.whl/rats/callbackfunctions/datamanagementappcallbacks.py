from dash.dependencies import Input, State
from dash_extensions.enrich import Output, Trigger
from dash.exceptions import PreventUpdate
from dash import html
from rats.core.app import session_data, rats_data
import dash_bootstrap_components as dbc
from rats.core.RATS_CONFIG import PlotBanks

def register_callbacks(app=None,callback_designation:str = 'data_management_app_') -> None:
    outputs = [Output(f'{PlotBanks.INTERSCAN_APP.designation}fileselect{i}', 'options') for i in
               range(PlotBanks.INTERSCAN_APP.number_of_plot_banks)] + \
              [Output(f'{PlotBanks.SCOPE_APP.designation}fileselect{i}', 'options') for i in
               range(PlotBanks.SCOPE_APP.number_of_plot_banks)] + \
              [Output(f'{PlotBanks.DASHBOARD.designation}fileselect{i}', 'options') for i in
               range(PlotBanks.DASHBOARD.number_of_plot_banks)]

    @app.callback([Output(f'{callback_designation}data', 'options'),
                   Output(f'{callback_designation}report', 'children')],
                  [Input(f'{callback_designation}pulldata', 'n_clicks')])
    def pulldata(click):

        options = []

        rats_data.scan_for_files()
        file_list = rats_data.data_files['file'].tolist()
        sizes = rats_data.data_files['file_size'].tolist()
        total_size = rats_data.data_files['file_size'].sum()
        for file, size in zip(file_list, sizes):


            options.append(dict(label=f'{file.split(".")[0]}: {size:.2f}Mb', value=file))

        return [options] + [f'Total data use: {total_size:.2f}Mb']

    @app.callback([Output(f'{callback_designation}message', 'children'),
                   Output('deleteselecteddata_target', 'children'),
                   Output('refresh-overlay', 'style')] + outputs,
                  [Trigger(f'{callback_designation}delete', 'n_clicks')],
                  [State(f'{callback_designation}data', 'value')], prevent_initial_call=True)
    def delete_selected_data(values):
        session_file_filter_values = [file[:-8] for file in values]  # remove '.feather' from filename

        session_data.data_files = session_data.data_files[~session_data.data_files['File'].
            isin(session_file_filter_values)]

        children = dbc.Table.from_dataframe(session_data.data_files, striped=True, id='table')

        filenames = session_data.data_files['File'].tolist()

        options = []

        for i in range(len(filenames)):
            item = {'label': f'{filenames[i]}', 'value': f'{filenames[i]}'}
            options.append(item)

        rats_data.delete_data(values)

        return ['Cleared requested files. Please click scan for data again.', children, {'display': 'flex'}] + \
               [options for _ in outputs]

    @app.callback([Output(f'{callback_designation}clearstatus', 'children'),
                   Output('clearprogramdata_target', 'children'),
                   Output('refresh-overlay', 'style')] + outputs,
                  [Trigger(f'{callback_designation}cleardata', 'n_clicks')], prevent_initial_call=True)
    def clearprogramdata():
        print('Ratdash has cleared all the program data!')

        rats_data.scan_for_files()
        stored_files = rats_data.data_files['file'].tolist()
        stored_files_filter = [file[:-8] for file in stored_files]
        try:
            session_data.data_files = session_data.data_files[
                ~session_data.data_files['file'].isin(stored_files_filter)]
        except:
            pass
        rats_data.delete_data(all=True)
        options = []
        children = html.Div(children=[
            html.Div([], id='datalist', className='col')],
            id='deleteselecteddata_target', className='container')

        return ['All previously processed data has been cleared', children, {'display': 'flex'}] + \
               [options for _ in outputs]
