from utils.data_loader import *
from utils.visuals import *

recommendations = load_recommendations()
layout = html.Div([
    html.H1("Produits phares"),
    html.Hr(),
    generate_top_interactive_products_card(recommendations),
    html.Hr(),
    generate_top_interactive_products_barplot(recommendations)
])
