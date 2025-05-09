import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from ner_visualizer.config import config_page

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample text
text = "This is an example text where entities like Python, Dash, and web development can be highlighted."

# Define configuration for the buttons (initial config can be empty)
button_config = [
    {"label": "Highlight Python", "action": "highlight_python"},
    {"label": "Highlight Dash", "action": "highlight_dash"},
    {"label": "Highlight Web Development", "action": "highlight_web"},
]

# Layout of the app
app.layout = html.Div(
    [
        # Navigation Bar
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.NavItem(dbc.NavLink("Config", href="/config")),
                    ],
                    brand="Text Highlighting App",
                    brand_href="/",
                    color="primary",
                    dark=True,
                ),
            ]
        ),
        # Page Content
        html.Div(id="page-content"),
    ]
)


# Main Page Layout
def main_page():
    return html.Div(
        children=[
            # Display text
            html.Div(
                children=[html.P(text, id="text", style={"font-family": "Arial", "font-size": "18px", "line-height": "1.5"})],
                style={"padding": "20px", "background-color": "#f4f4f4"},
            ),
            # Buttons based on configuration
            html.Div(
                children=[dbc.Button(btn["label"], id=f"btn-{btn['action']}", n_clicks=0) for btn in button_config], style={"padding": "20px"}
            ),
        ]
    )


# Callback to switch between pages
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/config":
        return config_page()  # Import the config page from config.py
    else:
        return main_page()


def run():
    app.run(debug=True)


# Run the app
if __name__ == "__main__":
    run()
