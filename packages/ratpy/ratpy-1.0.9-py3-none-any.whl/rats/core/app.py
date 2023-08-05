from rats.core.session_data_tracker import SessionDataTracker
from rats.core.rats_data_tracker import RatsDataTracker
from rats.core.RATS_CONFIG import packagepath, cachepath, dfpath
from rats.core.rats_parser import RatsParser
from dash_extensions.enrich import DashProxy, MultiplexerTransform, TriggerTransform
import dash_bootstrap_components as dbc

app = DashProxy(__name__, external_stylesheets=[dbc.themes.FLATLY],
                suppress_callback_exceptions=True,
                transforms=[MultiplexerTransform(),
                            TriggerTransform()])
app.title='RATS'
session_data = SessionDataTracker(data_directory=str(packagepath / cachepath), parser=RatsParser)
rats_data = RatsDataTracker(str(packagepath / dfpath))
server = app.server
