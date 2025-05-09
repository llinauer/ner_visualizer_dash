from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash
from ner_visualizer.app import app

# Global button config list (can be initialized as empty or with default buttons)
button_config = [
    {"label": "Highlight Python", "action": "highlight_python"},
    {"label": "Highlight Dash", "action": "highlight_dash"},
    {"label": "Highlight Web Development", "action": "highlight_web"},
]


# Config Page Layout
def config_page():
    return html.Div(
        children=[
            html.H2("Configure Buttons"),
            html.Div(
                children=[
                    dbc.Input(id="button-label", placeholder="Button Label", style={"margin-bottom": "10px"}),
                    dbc.Input(id="button-action", placeholder="Button Action", style={"margin-bottom": "10px"}),
                    dbc.Button("Add Button", id="add-button", n_clicks=0),
                ],
                style={"padding": "20px"},
            ),
            html.Div(
                children=[
                    html.H4("Current Buttons:"),
                    html.Ul(id="button-list"),
                ],
                style={"padding": "20px"},
            ),
        ]
    )


# Callback to update the list of buttons on the config page
@app.callback(
    Output("button-list", "children"),
    [Input("add-button", "n_clicks"), Input({"type": "remove-button", "index": dash.dependencies.ALL}, "n_clicks")],
    [State("button-label", "value"), State("button-action", "value")],
)
def update_buttons(add_n_clicks, remove_n_clicks, label, action):
    ctx = dash.callback_context

    # If there's no click yet, just return the initial list
    if not ctx.triggered:
        return [html.Li(f"{btn['label']} -> {btn['action']}") for btn in button_config]

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Add a new button
    if triggered_id == "add-button" and label and action:
        button_config.append({"label": label, "action": action})

    # Remove a button (identify by index)
    if "remove-button" in triggered_id:
        button_index = int(triggered_id.split("{")[1].split("}")[0])  # Extract button index
        del button_config[button_index]

    # Update the list of buttons with Remove buttons next to each
    return [
        html.Li(f"{btn['label']} -> {btn['action']} " + html.Button("Remove", id={"type": "remove-button", "index": i}))
        for i, btn in enumerate(button_config)
    ]
