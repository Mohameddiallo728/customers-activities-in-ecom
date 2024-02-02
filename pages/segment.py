import dash_bootstrap_components as dbc
from dash import html

from utils.data_loader import load_activities
from utils.visuals import get_segments_by_purchases_frequency

df = load_activities()

layout = dbc.Container(
    [
        html.H1("Segments de Clients", className="mb-4"),
        get_segments_by_purchases_frequency(df),
        html.Hr(),
        html.Hr(),
        html.Hr(),
        html.Div([
            html.Div(id="user-list"),
            html.Hr(),
            dbc.Pagination(id="pagination", max_value=0, active_page=1),
        ])
    ],
    fluid=True,
)


def update_user_list(clicked_category, page_current):
    columns_to_display = [
        'Customer ID', 'Age', 'Gender', 'Category',
        'Purchase Amount (USD)', 'Location', 'Size', 'Season',
        'Review Rating', 'Subscription Status', 'Shipping Type',
        'Discount Applied', 'Promo Code Used', 'Previous Purchases',
        'Payment Method'
    ]

    filtered_data = df[df['Cluster'] == clicked_category]
    page_size = 10
    total_pages = round(len(filtered_data) / page_size)
    start_index = page_current * page_size
    end_index = start_index + page_size
    table_data = filtered_data.iloc[start_index:end_index][columns_to_display]

    pagination = dbc.Pagination(id="pagination", max_value=total_pages, active_page=page_current,
                                previous_next=True, fully_expanded=False)

    table = dbc.Table.from_dataframe(
        table_data,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
    )

    return html.Div([
        dbc.Row([table, html.Hr(), pagination])
    ])
