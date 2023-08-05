import pandas as pd
import datetime
import plotly
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from rats.modules import scopeplots
from rats.core.RATS_CONFIG import packagepath, dfpath, Packet

def register_callbacks(app, number_of_banks: int, callback_designation: str = 'scope_app_') -> None:
    for bank in range(number_of_banks):
        @app.callback([Output(f'{callback_designation}plot{bank}', 'figure'),
                       Output(f'{callback_designation}edbselect{bank}', 'options'),
                       Output(f'{callback_designation}edbselect{bank}','value'),
                       Output(f'{callback_designation}fileselect-accordion{bank}','title')],
                      [Input(f'{callback_designation}replot{bank}', 'n_clicks'),
                       Input(f'{callback_designation}centre_data', 'n_clicks')],
                      [State(f'{callback_designation}llc', 'value'),
                       State(f'{callback_designation}buffer', 'value'),
                       State(f'{callback_designation}fileselect{bank}', 'value'),
                       State(f'{callback_designation}edbselect{bank}', 'value')], prevent_initial_call=True)
        def plotbank(replot, centre, llc, buffer, file, edbs=[]):
            # 'centre' not used in function but required to fire the update. Do not remove
            if replot == 0:
                raise PreventUpdate

            df = pd.read_feather(str(packagepath/ dfpath / f'{file}.feather'))
            df.name = 'some name'

            options_creator_df = df[[Packet.ACTIVE_EDBS.field_name, Packet.ACTIVE_EDBS.field_name+'_id']].drop_duplicates()
            optionsdict = options_creator_df.to_dict(orient='list')
            options = [{"label": f"EDB {x}: {y}", "value": y} for x,y in list(zip(optionsdict['EDB'], optionsdict['EDB_id']))]
            s = scopeplots.scopeplot(df, llc=llc, buffer=buffer, facet=True, show_sip=False, timescale=1, edbs=edbs)

            return s, options, edbs, file

        @app.callback(Output(f'{callback_designation}download{bank}', 'data'),
                      [Input(f'{callback_designation}download-btn{bank}', 'n_clicks')],
                      [State(f'{callback_designation}plot{bank}', 'figure'),
                       State(f'{callback_designation}fileselect{bank}', 'value')], prevent_initial_call=True)
        def handle_scope_download(click, fig, filename):
            date = datetime.datetime.now().strftime("%d%b%Y-%T")
            html = plotly.io.to_html(fig)
            return dict(content=html, filename=f"{date}-{filename}-{callback_designation}.html")
