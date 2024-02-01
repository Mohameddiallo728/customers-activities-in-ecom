from utils.data_loader import *
from utils.visuals import *

activities = load_activities()
customers = load_customers()
products = load_products()
recommendations = load_recommendations()
layout = html.Div([
    html.H1("Tableau de bord"),
    html.Hr(),
    generate_grouped_cards(customers, products),
    html.Hr(),
    dbc.Row([
        dbc.Col(generate_gender_pie_chart(customers)),
        dbc.Col(generate_purchase_by_gender(customers)),
    ], className="mb-4"),
    html.Hr(),
    generate_age_vs_purchase(customers),
    html.Hr(),
    dbc.Row([
        dbc.Col(generate_category_distribution(customers)),
        dbc.Col(generate_sales_by_category(customers)),
    ], className="mb-4"),
    html.Hr(),
    dbc.Row([
        dbc.Col(generate_item_purchased_countplot(customers)),
        dbc.Col(generate_shipping_type_countplot(customers)),
    ], className="mb-4"),
    html.Hr(),
    dbc.Row([
        dbc.Col(generate_size_distribution(customers)),
        dbc.Col(generate_season_countplot(customers)),
    ], className="mb-4"),
    html.Hr(),
    generate_sales_map(activities),
    html.Hr(),
    generate_location_countplot(customers),
    html.Hr(),
    dbc.Row([
        dbc.Col(generate_sales_over_time(activities)),
        dbc.Col(generate_sales_by_season(customers)),
    ], className="mb-4"),
    html.Hr(),
    dbc.Row([
        dbc.Col(generate_sales_by_size(customers)),
        dbc.Col(generate_purchase_frequency(customers)),
    ], className="mb-4"),
    html.Hr(),
    dbc.Row([
        dbc.Col(generate_interaction_type_pie_chart(activities)),
        dbc.Col(generate_interaction_heatmap(activities)),
    ], className="mb-4"),
    html.Hr(),
    generate_interaction_over_time(activities)
])
