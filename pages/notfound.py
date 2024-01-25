from dash import Input, Output, State, dcc, html

layout = html.Div(
    [
        html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"The pathname was not recognised..."),
    ],
    className="p-3 bg-light rounded-3",
)
