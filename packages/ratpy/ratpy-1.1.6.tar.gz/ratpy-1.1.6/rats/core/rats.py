"""
File contains the boilerplate for the single page rats visualiser app.

This page brings together the views and callback functions within the frame of the general page
"""


from dash import html, dcc
import dash_bootstrap_components as dbc
from rats.core.app import app
import rats.views.ratdash as ratdash
import rats.views.scopeapp as scopeapp
import rats.views.interscanapp as interscanapp
import rats.views.data_management_app as datamanagementapp
import rats.callbackfunctions.corecallbacks as core_callbacks
import rats.callbackfunctions.ratdashcallbacks as ratdash_callbacks
import rats.callbackfunctions.scopeappcallbacks as scope_app_callbacks
import rats.callbackfunctions.interscanappcallbacks as interscan_app_callbacks
import rats.callbackfunctions.datamanagementappcallbacks as data_management_app_callbacks
from rats.core.RATS_CONFIG import PlotBanks

import dash_uploader as du

topodatatable = core_callbacks.populatetoporeport()

ratdash_callbacks.register_callbacks(app,PlotBanks.DASHBOARD.number_of_plot_banks, PlotBanks.DASHBOARD.designation)
scope_app_callbacks.register_callbacks(app,PlotBanks.SCOPE_APP.number_of_plot_banks, PlotBanks.SCOPE_APP.designation)
interscan_app_callbacks.register_callbacks(app,PlotBanks.INTERSCAN_APP.number_of_plot_banks, PlotBanks.INTERSCAN_APP.designation)
data_management_app_callbacks.register_callbacks(app, PlotBanks.DATA_MANAGEMENT_APP.designation)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    #############################################################################################
    # HEADER
    #############################################################################################
    html.Div([
        # html.Div(className='container', children=[
        html.Div(className='logo', children=[html.Img(src='assets/graph-up.svg', className='logo-svg'),
                                             html.Span('RATS'), ' DATA VISUALISER']),

        html.Div([], id='runstatus', className='text-center text-danger'),

        # ==================================================
        # the du.Upload max_files attribute is still experimental. This is a potential weak point in the app
        # but seems to work fine for now
        # ==================================================


    ],
        # className='container-fluid bg-secondary p-4 text-center rounded-bottom text-white'
        className='header-bar'
    ),

    dbc.Accordion(id='accordion-upload',
        children=[
            dbc.AccordionItem(id='accordion-topo-item',
                              children=[
                                  dcc.Upload(
                                      id='upload-topo',
                                      children=html.Div([
                                          'Drag and Drop or Click to Select Relevant Topo Files'
                                      ]),
                                      multiple=True
                                  ),

                                  html.P('Topo files and EDS files loaded:'),
                                  html.Div([
                                      html.Div([topodatatable], id='toporeport', className='col')
                                  ], id='topodatacontainer', className='container'),

                                  html.Button(['Clear Topo Data'], id='cleartopo', n_clicks=None,
                                              className='btn btn-danger', type='button'),

                                  html.Div([], id='clearedtopo')
                              ],
                              title="Upload Topology File and Data Sheets",
                              ),

            dbc.AccordionItem(id='accordion-upload-item',
                children=[
                    du.Upload(max_files=10,
                              filetypes=['txt'],
                              text='Drag and drop files here or click to browse',
                              text_completed='Uploaded File(s) include: ',
                              ),
                    html.Button(id='rats_upload_button', className='btn rats-btn', children='Process Available Data')
                ],
                title="Upload RATS Data",
            ),


        ],
        start_collapsed=True),

    html.Div(className='body-content', children=[
                    dbc.Spinner([
                                      html.Div(id='clearprogramdata_target', children=[
                                          html.Div(children=[
                                              html.Div([], id='datalist', className='col')],
                                              id='deleteselecteddata_target', className='container'),
                                      ]),
                                    ]),
                        html.Div([html.Div([], id='errorlog', className='col')], id='errorlogcontainer',
                                 className='container'),

                        html.Br(),

                        html.Div([
                            dcc.Textarea(
                                id='notes',
                                style={'width': '100%', 'height': 100},
                                persistence=True,
                                persistence_type='local'
                            ),
                        ], className='container'),

                        html.Br(),

                        #############################################################################################
                        # BODY CONTENT
                        #############################################################################################
                        dbc.Tabs(id='rattab', className='justify-content-center', persistence=True, persistence_type='local', children=[

                            # ==========================================================================================
                            #    Apps go here
                            # ==========================================================================================
                            # ERROR DETECTION APP
                            dcc.Tab(label='Error Detection', value='ratdash', children=[
                                html.Div(className='tab-padding', children=[
                                ratdash.createcontent(PlotBanks.DASHBOARD.number_of_plot_banks,
                                                      PlotBanks.DASHBOARD.designation)
                            ]),
                            ]),
                            # SCOPE APP
                            dcc.Tab(label='Scope', value='scopeapp', children=[
                                html.Div(className='tab-padding', children=[
                                    scopeapp.createcontent(PlotBanks.SCOPE_APP.number_of_plot_banks,
                                                           PlotBanks.SCOPE_APP.designation)
                                ]),
                            ]),
                            # JITTER APP
                            dcc.Tab(label='Jitter Analysis', value='interscanapp', children=[
                                html.Div(className='tab-padding', children=[
                                interscanapp.createcontent(PlotBanks.INTERSCAN_APP.number_of_plot_banks,
                                                           PlotBanks.INTERSCAN_APP.designation)
                            ]),
                            ]),
                            # DATA MANAGEMENT APP
                            dcc.Tab(label='Data Management', value='datamanagementapp', children=[
                                html.Div(className='tab-padding', children=[
                                datamanagementapp.createcontent()
                            ]),
                            ]),

                        ]),

                        #############################################################################################
                        # FOOTER
                        #############################################################################################

                        html.Br(),
                        html.Br(),


                    html.Div(className='footer'),
                    html.Div(className='footer-overlay',
                             children=[
                                 html.Div(className='logo', children=[html.Span('WATERS'
                                                                                '')])
                             ])
                        ]),

#============================================================================
#    OVERLAY DIV
#============================================================================
    html.Div(id='refresh-overlay',
             className='refresh-overlay',
             children=[html.A(children=['CLICK to Refresh the Page'],
                              href='/', id = 'refresh-page-btn',
                              className='btn rats-refresh-btn refresh-page',
                              n_clicks=0)
                       ],
             style={'display': 'None'}),
    ])





app.run_server()
