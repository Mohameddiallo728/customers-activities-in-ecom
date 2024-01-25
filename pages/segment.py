import dash_bootstrap_components as dbc
from dash import html

from utils.data_loader import load_activities
from utils.visuals import generate_cluster_cards

df = load_activities()

layout = dbc.Container(
    [
        html.H1("Segments de Clients", className="mb-4"),
        html.Div(generate_cluster_cards(df), id="cluster-cards"),
    ],
    fluid=True,
)
