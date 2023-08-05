from dash import html
import dash_bootstrap_components as dbc

def createcontent(designation:str = 'data_management_app_'):

    layout = html.Div(className='container-fluid', children=[
        html.Div(className='card rats-card rats-single-card', children=[
            html.Div(className='card-header rats-card-header', children=[
                html.Div(
                    [html.Button(id=f'{designation}pulldata', children='Click to scan for currently archived data',
                                 className='btn rats-btn', type='button', n_clicks=0)
                     ], id=f'{designation}pullcontainer', className='col-12 text-center'),
                html.Br()
            ]),
            html.Div(className='card-body text-center rats-card-body program-data', children=[

                dbc.Checklist(
                    options=[],
                    id=f"{designation}data",
                    className='program-data-table'),

                html.Div(id=f'{designation}report', className='data-use-report'),

                dbc.Button(id=f'{designation}delete', children='Delete selected dataframes',
                           className='btn btn-warning rats-btn-warning me-1', type='button', n_clicks=0),

                dbc.Button(id=f'{designation}cleardata', children=['Delete all dataframes'],  n_clicks=None,
                           className='btn btn-danger rats-btn-danger me-1', type='button'),

                html.Div(id=f'{designation}clearstatus', className='text-center text-danger'),

                html.Div(id=f'{designation}message'),
                html.Div(className='data-management-bottom-padding'),


            ])
        ])
    ])

    return layout
