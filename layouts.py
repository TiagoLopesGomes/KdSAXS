import dash_bootstrap_components as dbc
from dash import dcc, html
from config import ALLOWED_MODELS, DEFAULT_MODEL, KD_RANGE, CONCENTRATION_RANGE, KD_POINTS, CONCENTRATION_POINTS

def create_model_selection():
    model_display_names = {
        'kds_saxs_mon_oligomer': 'Monomer-Oligomer',
        'kds_saxs_oligomer_fitting': 'Protein Binding'
    }

    return html.Div([
        html.Div([
            html.Div(["Choose model:", html.Sup(html.I(className="fas fa-info-circle", id="model-info", style={'marginLeft': '5px'}))], 
                     className="centered-bold-text"),
        
            dcc.Dropdown(
                id='model-selection',
                options=[{'label': model_display_names.get(model, model), 'value': model} for model in ALLOWED_MODELS],
                value=DEFAULT_MODEL,
                style={'width': '50%', 'padding': '5px'}
            ),
        ]),
        create_model_specific_inputs(),
    ], 
    className="section-frame section-frame-0")

def create_saxs_upload_section():
    return html.Div([
        html.Div([
            html.Div([
                "Upload experimental SAXS profiles and concentrations:",
                html.Sup(html.I(className="fas fa-info-circle", id="exp-saxs-info", style={'marginLeft': '5px'}))
            ], className="centered-bold-text", style={'flex': '1'}),
            
            # Reset button aligned with title
            html.Button([
                html.I(className="fas fa-trash-alt", style={'marginRight': '5px'}),
                "Reset"
            ],
            id='delete-all-exp-saxs',
            className='btn btn-danger btn-sm')
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'marginBottom': '20px',
            'justifyContent': 'space-between'
        }),
        
        html.Div([
            html.Label("Concentration units: ", 
                      style={
                          'marginRight': '10px',
                          'display': 'flex',
                          'alignItems': 'center',
                          'height': '38px'
                      }),
            dcc.Dropdown(
                id='concentration-units',
                options=[
                    {'label': 'nM', 'value': 'nM'},
                    {'label': 'µM', 'value': 'µM'},
                    {'label': 'mM', 'value': 'mM'}
                ],
                value='µM',
                style={'width': '100px'}
            ),
            html.Label("Angular units: ", 
                      style={
                          'marginLeft': '20px',
                          'marginRight': '10px',
                          'display': 'flex',
                          'alignItems': 'center',
                          'height': '38px'
                      }),
            dcc.Dropdown(
                id='q-units',
                options=[
                    {'label': '1/Å', 'value': '1'},
                    {'label': '1/nm', 'value': '2'}
                ],
                value='2',
                style={'width': '100px'},
                clearable=False
            )
        ], style={
            'marginBottom': '20px',
            'display': 'flex',
            'justifyContent': 'flex-end',
            'alignItems': 'center'
        }),
        
        html.Div(id='saxs-upload-container', children=[
            html.Div([
                html.Div([
                    dcc.Upload(
                        id={'type': 'upload-exp-saxs', 'index': 0},
                        children=html.Div(['Drag and Drop or Select Experimental SAXS File']),
                        className="upload-style",
                        multiple=False
                    ),
                    html.I(className="fas fa-minus-circle", 
                           id={'type': 'delete-saxs', 'index': 0},
                           n_clicks=0,
                           style={'position': 'absolute', 'top': '5px', 'right': '5px', 'cursor': 'pointer'})
                ], style={'position': 'relative', 'flex': '3', 'marginRight': '10px'}),
                dcc.Input(
                    id={'type': 'input-concentration', 'index': 0},
                    type='number',
                    placeholder='Concentration',
                    value=None,
                    min=0,
                    step=0.1,
                    className="input-style",
                    style={'flex': '1'}
                ),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
            html.Div([
                html.Div([
                    dcc.Upload(
                        id={'type': 'upload-exp-saxs', 'index': 1},
                        children=html.Div(['Drag and Drop or Select Experimental SAXS File']),
                        className="upload-style",
                        multiple=False
                    ),
                    html.I(className="fas fa-minus-circle", 
                           id={'type': 'delete-saxs', 'index': 1},
                           n_clicks=0,
                           style={'position': 'absolute', 'top': '5px', 'right': '5px', 'cursor': 'pointer'})
                ], style={'position': 'relative', 'flex': '3', 'marginRight': '10px'}),
                dcc.Input(
                    id={'type': 'input-concentration', 'index': 1},
                    type='number',
                    placeholder='Concentration',
                    value=None,
                    min=0,
                    step=0.1,
                    className="input-style",
                    style={'flex': '1'}
                ),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'})
        ]),
        html.Button('Add another SAXS profile', id='add-saxs-button', n_clicks=0, className='dash-button'),
    ], className="section-frame section-frame-1")

def create_theoretical_saxs_section():
    return html.Div([
        html.Div([
            "Upload theoretical SAXS profiles or PDB files (max 20 PDB files per state):",
            html.Sup(html.I(className="fas fa-info-circle", id="theo-saxs-info", style={'marginLeft': '5px'}))
        ], className="centered-bold-text"),
        
        # Add toggle switch
        html.Div([
            dbc.Switch(
                id='theoretical-input-type',
                label="Upload PDB files instead of SAXS profiles",
                value=False,
                className='mb-3'
            ),
        ]),
        
        # Container will be populated by callback based on model and toggle state
        html.Div(id='theoretical-saxs-upload-container'),
        html.Div(id='example-file-display')
    ], className="section-frame section-frame-2")

def create_kd_selection_section():
    return html.Div([
        html.Div([
            "Choose parameters for simulation:",
            html.Sup(html.I(className="fas fa-info-circle", id="sim-params-info", style={'marginLeft': '5px'}))
        ], className="centered-bold-text"),
        html.Div([
            html.Div([
                create_input_field("Kd min", "kd-min", value=KD_RANGE[0]),
                create_input_field("Kd max", "kd-max", value=KD_RANGE[1]),
                create_input_field("Points", "kd-points", value=KD_POINTS),
            ], className="input-row"),
            html.Div([
                create_input_field("Conc. min", "conc-min", value=CONCENTRATION_RANGE[0]),
                create_input_field("Conc. max", "conc-max", value=CONCENTRATION_RANGE[1]),
                create_input_field("Points", "conc-points", value=CONCENTRATION_POINTS),
            ], className="input-row"),
        ], className="input-container"),
        html.Button('Run Analysis', id='run-analysis', n_clicks=0, className='dash-button')
    ], className='section-frame section-frame-3')

def create_model_specific_inputs():
    return html.Div([
        html.Div([
            html.Div([
                html.Label(id='n-input-label', children="Stoichiometry: "),
                dcc.Input(
                    id='input-n',
                    type='number',
                    value=2,
                    min=1,
                    step=1,
                    className="input-style"
                )
            ], id='n-input-container', style={'display': 'inline-block', 'marginRight': '20px'}),

            html.Div([
                html.Label("Receptor concentration: "),
                dcc.Input(
                    id='input-receptor-concentration',
                    type='number',
                    value=None,
                    min=0,
                    step=0.1,
                    className="input-style"
                )
            ], id='receptor-concentration-container', style={'display': 'inline-block'})
        ], style={'display': 'flex', 'alignItems': 'flex-end'})
    ])

def create_input_field(label, id, value=None):
    return html.Div([
        html.Label(label, style={'display': 'block', 'marginBottom': '5px'}),
        dcc.Input(id=id, type='number', className="input-box", value=value)
    ], className="input-group")

def create_instructions():
    return html.Div([
        html.H2("Instructions", style={'textAlign': 'center', 'marginTop': '5px'}),
        html.Ul([
            html.Li([
                html.Span("K"),
                html.Sub("D"),
                html.Span("SAXS is a tool for studying protein interactions using Small Angle X-ray Scattering (SAXS) data."),
                " This application allows you to analyze binding equilibria and determine dissociation constants (K",
                html.Sub("D"),
                html.Span(") from SAXS experiments.")
            ]),
            html.Li("Upload your SAXS profiles or PDB files (e.g., MD, NMR, X-ray or Alphafold models), set parameters, and visualize results with interactive plots and downloadable CSV and PDF files."),
            html.Li(["When uploading PDB files, ",
                html.Span("K"),
                html.Sub("D"),
                html.Span("SAXS will automatically calculate and average the SAXS profiles for each state."),
            ]),
            html.Li([
                "Choose between: ",
                dbc.Button("Monomer-Oligomer ", id="popover-mon-oligomer", color="link"),
                " and ",
                dbc.Button("Protein binding", id="popover-oligomer-fitting", color="link"),
                "equilibria to fit your experimental data. For the Monomer-Oligomer model the stoichiometry (n) corresponds to the Oligomer stoichiometry. For the protein binding model the value n corresponds to the number of independent binding sites. For n=1 this model falls back to a simple 1:1 Receptor-Ligand binding model. When you click on a K",
                html.Sub("D"),
                " value in the χ² vs K",
                html.Sub("D"),
                " plot the molecular fractions are displayed at the right side plot.",
                
            ]),
            html.Li("The inputted concentrations, chosen parameters for the simulation and the uploaded experimental and theoretical SAXS profiles should be self-consistent in units."),
            # html.Li([
            #     "To see how the app works, you can ",
            #     html.Button("load an example", id="load-example", n_clicks=0, style={'cursor': 'pointer'}),
            #     " dataset."
            # ]),

            html.Li([
                "To see how the app works, you can load the example data by clicking ",
                       html.A("here", 
                       id="load-example", 
                       href="#", 
                       style={'cursor': 'pointer', 'color': '#007bff'}, 
                       n_clicks=0
                ),
                ", then go to the run analysis tab and check the expected results ",
                
                html.A("here", href="https://github.com/TiagoLopesGomes/KdSAXS/tree/main/examples/", target="_blank"),
                ", or check detailed usage instructions ",
                html.A("here", href="https://github.com/TiagoLopesGomes/KdSAXS#detailed-usage", target="_blank"),
                "."
            ]),
        ]),
    ], className="info-section")

def create_model_selection_tab():
    return dbc.Card(dbc.CardBody([
        create_model_selection()
    ]))

def create_experimental_saxs_tab():
    return dbc.Card(dbc.CardBody([
        create_saxs_upload_section()
    ]))

def create_theoretical_saxs_tab():
    return dbc.Card(dbc.CardBody([
        create_theoretical_saxs_section()
    ]))

def create_analysis_parameters_tab():
    return dbc.Card(dbc.CardBody([
        create_kd_selection_section()
    ]))

def create_info_tab():
    return dbc.Card(dbc.CardBody([
        create_instructions()
    ]))

def create_main_layout():
    return html.Div([
        dbc.Container([
            html.H1([
                "K",
                html.Sub("D"),
                "SAXS - analysing binding equilibria with SAXS data using explicit models"
            ], className="text-center my-4"),
            dbc.Tabs([
                dbc.Tab(create_info_tab(), label="1. Instructions"),
                dbc.Tab(create_model_selection_tab(), label="2. Model Selection"),
                dbc.Tab(create_experimental_saxs_tab(), label="3. Experimental SAXS"),
                dbc.Tab(create_theoretical_saxs_tab(), label="4. Theoretical SAXS"),
                dbc.Tab(create_analysis_parameters_tab(), label="5. Run analysis"),
            ]),
            dbc.Row([
                dbc.Col([
                    
                    # Buttons for chi² plot
                    html.Div([
                        dbc.Button("Save Chi2 Plot as CSV", id="save-chi2-csv", className='secondary-dash-button'),
                        dbc.Button('Save Chi2 Plot as PDF', id='save-chi2-pdf', className='secondary-dash-button'),
                    ], className="d-flex justify-content-end mb-2"),
                    dcc.Graph(id='chi2-plot')
                ], md=6),
                dbc.Col([
                    
                    # Buttons for fraction plot
                    html.Div([
                        dbc.Button("Save Fraction Plot as CSV", id="save-fraction-csv", className='secondary-dash-button'),
                        dbc.Button('Save Fraction Plot as PDF', id='save-fraction-pdf', className='secondary-dash-button'),
                    ], className="d-flex justify-content-end mb-2"),
                    dcc.Graph(id='fraction-plot')
                ], md=6),
            ]),
            html.Div(id='saxs-fit-plots', className="mt-4"),
            dcc.Store(id='message-trigger', storage_type='memory'),
            dcc.Store(id='example-data-store'),
            dcc.Store(id='calculation-trigger', storage_type='memory'),
            dbc.Modal(
                [
                    #dbc.ModalHeader(dbc.ModalTitle("Status")),
                    dbc.ModalBody(id='modal-content'),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
                    ),
                ],
                id="message-modal",
                is_open=False,
                centered=True,
                className="message-modal",
            ),
            dcc.Download(id="download-chi2-csv"),
            dcc.Download(id="download-chi2-pdf"),
            dcc.Download(id="download-fraction-csv"),
            dcc.Download(id="download-fraction-pdf"),
            dcc.Store(id='experimental-data-store', storage_type='memory'),
            dbc.Modal(
                [
                    #dbc.ModalHeader(dbc.ModalTitle("Status")),
                    dbc.ModalBody([
                        html.Div([
                            html.H4("Calculating...", className="mb-3", style={'color': '#007bff'}),
                            dbc.Spinner(size="lg", color="primary"),
                        ], style={'textAlign': 'center'})
                    ]),
                    #dbc.ModalFooter(
                    #    html.Div(className="ms-auto")
                    #),
                ],
                id="loading-modal",
                is_open=False,
                centered=True,
                backdrop="static",
                className="message-modal",
            ),
            
        ], fluid=True, className="px-4", style={'max-width': '1400px', 'margin': '0 auto'}),
    ], style={'background-color': '#f7f8fa'})