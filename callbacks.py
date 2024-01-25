import dash

from pages import (
    dashboard,
    recommend,
    segment, bestproduct
)
from pages import notfound
from utils.data_loader import load_with_kmean
from utils.visuals import generate_user_modal

data = load_with_kmean()


def render_page_content(pathname):
    if pathname == "/":
        return dashboard.layout
    elif pathname == "/top_products":
        return bestproduct.layout
    elif pathname == "/dashboard":
        return dashboard.layout
    elif pathname == "/segment":
        return segment.layout
    elif pathname == "/recommend":
        return recommend.layout
    else:
        return notfound.layout


def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


def toggle_modal(clicked_category, opened):
    if clicked_category:
        filtered_data = data[data['Cluster'] == clicked_category]
        if not filtered_data.empty:
            modal_content = [generate_user_modal(clicked_category, filtered_data)]
            return modal_content, True  # Open the modal

    elif clicked_category == "close-modal":
        return dash.no_update, False  # Close the modal

    return dash.no_update, dash.no_update


def update_recommendations_model(selected_user, selected_model):
    return recommend.update_recommendations_model(selected_user, 6, selected_model)


def update_model_comparison_graph(selected_user):
    return recommend.update_model_comparison_graph(selected_user)
