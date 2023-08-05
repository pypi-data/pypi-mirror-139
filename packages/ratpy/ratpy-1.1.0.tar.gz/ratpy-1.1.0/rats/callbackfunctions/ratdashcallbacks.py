from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from rats.modules import bigpictureplots, scopeplots
from rats.core.RATS_CONFIG import packagepath, dfpath
import plotly
import datetime

def register_callbacks(app=None, number_of_banks: int = 1, callback_designation:str = 'dashboard_app_') -> None:
    for bank in range(number_of_banks):
        @app.callback([Output(f'{callback_designation}bigpictureplot{bank}', 'figure'),
                       Output(f'{callback_designation}scopeplot{bank}', 'figure'),
                       Output(f'{callback_designation}replot{bank}', 'n_clicks'),
                       Output(f'{callback_designation}fileselect-accordion{bank}','title')],
                      [Input(f'{callback_designation}replot{bank}', 'n_clicks'),
                       Input(f'{callback_designation}bigpictureplot{bank}', 'clickData'),
                       Input(f'{callback_designation}numberofscans{bank}', 'value')],
                      [State(f'{callback_designation}fileselect{bank}', 'value'),
                       State(f'{callback_designation}bigpictureplot{bank}', 'figure')])
        def handle_dashboard_plots(replot, bigpictureclickdata, scans, file, bigpicture):
            if replot == 0:
                raise PreventUpdate

            df = pd.read_feather(str(packagepath/ dfpath / f'{file}.feather'))
            df.name = 'some name'
            if replot is None:
                bp = bigpicture
            else:
                bp = bigpictureplots.bigpictureplot(df, decimate=True)

            s = scopeplots.scopeplot(df, buffer=scans, facet=False, show_sip=True, timescale=1)

            # ========================================================
            # PLOT LINKAGES
            # ========================================================
            if bigpictureclickdata is not None:
                df = pd.read_feather(str(packagepath / dfpath / f'{file}.feather'))
                start = int(bigpictureclickdata['points'][0]['x'])
                s = scopeplots.scopeplot(df, llc=start, buffer=scans, facet=False, show_sip=True, timescale=1)

            return bp, s, None, file

        @app.callback(Output(f'{callback_designation}download_bigpictureplot{bank}', 'data'),
                      [Input(f'{callback_designation}download-bigpicture-btn{bank}', 'n_clicks')],
                      [State(f'{callback_designation}bigpictureplot{bank}', 'figure'),
                       State(f'{callback_designation}fileselect{bank}', 'value')], prevent_initial_call=True)
        def handle_bigpicture_download(click, fig, filename):
            date = datetime.datetime.now().strftime("%d%b%Y-%T")
            html = plotly.io.to_html(fig)
            return dict(content=html, filename=f"{date}-{filename}-{callback_designation}bp.html")

        @app.callback(Output(f'{callback_designation}download_scope{bank}', 'data'),
                      [Input(f'{callback_designation}download-scope-btn{bank}', 'n_clicks')],
                      [State(f'{callback_designation}scopeplot{bank}', 'figure'),
                       State(f'{callback_designation}fileselect{bank}', 'value')], prevent_initial_call=True)
        def handle_dashboard_download(click, fig, filename):
            date = datetime.datetime.now().strftime("%d%b%Y-%T")
            html = plotly.io.to_html(fig)
            return dict(content=html, filename=f"{date}-{filename}-{callback_designation}scope.html")
