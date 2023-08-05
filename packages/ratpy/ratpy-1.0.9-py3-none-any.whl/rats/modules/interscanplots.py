from rats.core.RATS_CONFIG import Packet
import pandas as pd
import plotly.express as px
pd.options.mode.chained_assignment = None

def interscanplot(df, timescale=1000000):
    title = 'title'
    df = df[[Packet.FUNCTION.field_name, Packet.TIME_STAMP.field_name, Packet.LLC_COUNT.field_name]].drop_duplicates()
    df = df.set_index([Packet.FUNCTION.field_name, Packet.LLC_COUNT.field_name]).diff()
    df = df.reset_index()
    df = df.iloc[1:]
    df.loc[:, 'timescale'] = timescale
    df.loc[:, Packet.TIME_STAMP.field_name] = df[Packet.TIME_STAMP.field_name]/df['timescale']
    df = df.sort_values(Packet.FUNCTION.field_name, ascending=False)

    fig = px.histogram(df, x=Packet.TIME_STAMP.field_name, title=title, template='simple_white')
    fig.update_yaxes(type='category')
    height = 380 if len(fig.data) == 1 else len(fig.data)*300
    fig.update_layout(height=height, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      modebar=dict(bgcolor='rgba(0,0,0,0)', color='grey', activecolor='lightgrey'))
    print(df.describe())

    return fig

