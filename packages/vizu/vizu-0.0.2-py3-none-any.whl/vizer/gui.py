import dash_bootstrap_components as dbc
from dash import html
from dash_extensions.enrich import Dash
from pandas import DataFrame

from vizer.control import create_layout, create_callbacks


def create_webapp(df: DataFrame):

    css = [dbc.themes.BOOTSTRAP] + ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"]
    app = Dash(__name__, external_stylesheets=css, prevent_initial_callbacks=True, suppress_callback_exceptions=True)

    app.layout = html.Div([
            create_layout(df)
        ], style={'height': '100vh'})

    create_callbacks(app, df)
    return app
