from rats.core.RATS_CONFIG import Packet
import numpy as np
import pandas as pd
import plotly.express as px
pd.options.mode.chained_assignment = None




def bigpictureplot(df, decimate=True, timescale=1000000):

    def assign_erroneous_edbs(df):
        # Function for use in a pandas .apply() method to a pandas groupby object
        errors = ' '.join(df[df['state'] == 'ERRORS'][Packet.ACTIVE_EDBS.field_name].astype(str).to_list())
        df['EDBs in error'] = errors
        return (df)

    title = df.board.unique()[0]
    df = df[[Packet.FUNCTION.field_name, Packet.PACKET_COUNT.field_name, Packet.LLC_COUNT.field_name,
             Packet.ACTIVE_EDBS.field_name, 'anomalous', Packet.TIME_STAMP.field_name]]

    df.drop_duplicates(subset=[Packet.LLC_COUNT.field_name, Packet.ACTIVE_EDBS.field_name, 'anomalous'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['state'] = np.where(df['anomalous'] == 0, 'GOOD', 'ERRORS')
    # df['time'] = df['time'] / df['timescale']

    if decimate:

        def decimate_bp_plot(df):
            # Wrapper function to use in a .apply() method
            if 'ERRORS' in df['state'].values:
                return df
            else:
                first = df.drop_duplicates(subset='function_number', keep='first')
                last = df.drop_duplicates(subset='function_number', keep='last')
                return pd.concat([first, last])

        df = df.groupby('state').apply(decimate_bp_plot)
        df[Packet.FUNCTION.field_name] = df[Packet.FUNCTION.field_name].astype('category')
        errors = df[df['state'] == 'ERRORS']

        df = df.groupby(Packet.LLC_COUNT.field_name).apply(assign_erroneous_edbs)

        fig = px.scatter(df,
                         x=Packet.LLC_COUNT.field_name, y=Packet.FUNCTION.field_name,
                         color='state',
                         hover_data=[Packet.LLC_COUNT.field_name, 'EDBs in error'],
                         title=title, template='simple_white')

        fig.update_traces(mode='lines+markers')

        if len(errors) > 0: # if this condition is satisfied, we need to style the 'errors' trace:
            fig.data[0].mode = 'markers'
            fig.data[1].mode = 'lines'
            fig.data[0].marker.color = 'red'
            fig.data[1].marker.color = 'blue'
            fig.data[1].marker.opacity = 0.5

    else:
        df['EDBs in error'] = np.where(df['state'] == 'ERRORS', df[Packet.ACTIVE_EDBS.field_name], 'NA')
        df = df.groupby(Packet.LLC_COUNT.field_name).apply(assign_erroneous_edbs)
        fig = px.scatter(df, x=Packet.LLC_COUNT.field_name, y=Packet.FUNCTION.field_name, color='state',
                         hover_data=[Packet.LLC_COUNT.field_name, 'EDBs in error'],
                         title=title, render_mode='webgl', template='simple_white')
        errors = df[df['state'] == 'ERRORS']


        if len(errors) > 0:
            fig.data[0].mode = 'markers'
            fig.data[0].marker.color = 'red'
            fig.data[1].marker.color = 'blue'

    fig.update_layout(showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      modebar=dict(bgcolor='rgba(0,0,0,0)', color='grey', activecolor='lightgrey'))
    fig.update_traces(marker=dict(size=12))
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    return fig

