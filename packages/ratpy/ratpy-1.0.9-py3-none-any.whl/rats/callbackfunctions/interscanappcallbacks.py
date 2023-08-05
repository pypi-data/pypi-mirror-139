import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from rats.modules import interscanplots
from rats.core.RATS_CONFIG import packagepath, dfpath
import plotly
import datetime


def register_callbacks(app=None, number_of_banks: int = 1, callback_designation:str = 'interscan_app_') -> None:
    for bank in range(number_of_banks):
        @app.callback(Output(f'{callback_designation}plot{bank}', 'figure'),
                      [Input(f'{callback_designation}replot{bank}', 'n_clicks')],
                      [State(f'{callback_designation}fileselect{bank}', 'value')], prevent_initial_call=True)
        def handle_interscan_replots(replot, file):
            if replot == 0:
                raise PreventUpdate

            df = pd.read_feather(str(packagepath / dfpath / f'{file}.feather'))
            plot = interscanplots.interscanplot(df)

            return plot

        @app.callback(Output(f'{callback_designation}download{bank}', 'data'),
                      [Input(f'{callback_designation}download-btn{bank}', 'n_clicks')],
                      [State(f'{callback_designation}plot{bank}', 'figure'),
                       State(f'{callback_designation}fileselect{bank}', 'value')], prevent_initial_call=True)
        def handle_interscan_download(click, fig, filename):
            date = datetime.datetime.now().strftime("%d%b%Y-%T")
            html = plotly.io.to_html(fig)
            return dict(content=html, filename=f"{date}-{filename}-{callback_designation}.html")
