import dash

from pages import (
    dashboard,
    recommend,
    segment, bestproduct
)
from pages import notfound
from utils.data_loader import load_with_kmean

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


def update_user_list(button0_clicks, button1_clicks, button2_clicks, button3_clicks, page_current):
    ctx = dash.callback_context
    # Check which button was clicked
    clicked_button_id = ctx.triggered_id.split(".")[0] if ctx.triggered_id else None

    # Handle button clicks
    if clicked_button_id == "button-0":
        category = 0
    elif clicked_button_id == "button-1":
        category = 1
    elif clicked_button_id == "button-2":
        category = 2
    elif clicked_button_id == "button-3":
        category = 3
    else:
        category = 0

    # Call the function from callbacks.py
    return segment.update_user_list(category, page_current)


def update_recommendations_model(selected_user, selected_model):
    return recommend.update_recommendations_model(selected_user, 6, selected_model)


def update_model_comparison_graph(selected_user):
    return recommend.update_model_comparison_graph(selected_user)
