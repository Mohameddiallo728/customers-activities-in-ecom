import dash
import dash_bootstrap_components as dbc
from dash import State, dcc, html
from dash.dependencies import Input, Output

import callbacks

# Initialiser l'application Dash

app = dash.Dash(
    external_stylesheets=[dbc.themes.MORPH],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    suppress_callback_exceptions=True
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Analytics", className="ms-2", id="navbar-brand"),
            dbc.Nav(
                [
                    dbc.Button(
                        html.Img(src="/assets/Menu.png", style={"height": "1.5rem", "width": "1.5rem"}),
                        className="navbar-toggler",
                        id="sidebar-toggle",
                    ),
                ],
                className="mr-auto",  # Align the button to the left
                navbar=True,
            ),
            dbc.Nav(
                [
                    dbc.NavItem(html.P("By _medi728 follow on ",
                                       className="social-p")),
                    dbc.NavItem(html.A(html.Img(src="/assets/linkedin-logo.png", style={"height": "1.5rem", "width": "1.5rem"}),
                                       href="www.linkedin.com/in/mohamed-diallo-02a0b5194",
                                       className="nav-link")),
                    dbc.NavItem(html.A(html.Img(src="/assets/github-logo.png", style={"height": "1.8rem", "width": "1.8rem"}),
                                       href="https://github.com/Mohameddiallo728",
                                       className="nav-link")),
                    dbc.NavItem(html.A(html.Img(src="/assets/gitlab-logo.png", style={"height": "1.5rem", "width": "1.5rem"}),
                                       href="https://gitlab.com/Mohamed_diallo",
                                       className="nav-link")),
                ],
                className="ml-auto social-link",  # Align the items to the right
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    fixed="top",
)


sidebar = html.Div(
    [
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.Img(src="/assets/home-colored.png",
                                     style={"height": "1.5rem", "width": "1.5rem", "marginTop": '-8px'}),
                            "  Accueil",
                        ],
                        href="/",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.Img(src="/assets/best-product.png",
                                     style={"height": "1.5rem", "width": "1.5rem", "marginTop": '-3px'}),
                            "  Top Produits",
                        ],
                        href="/top_products",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.Img(src="/assets/users-colored.png",
                                     style={"height": "1.5rem", "width": "1.5rem", "marginTop": '-5px'}),
                            "  Clients",
                        ],
                        href="/segment",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.Img(src="/assets/robot-9.png",
                                     style={"height": "1.5rem", "width": "1.5rem", "marginTop": '-7px'}),
                            "  Recommendation",
                        ],
                        href="/recommend",
                        active="exact",
                    ),
                ],
                vertical=True,
                pills=True,
                style={"height": "100vh", "overflowY": "auto", "color": "black"},
            ),
            id="collapse"
        ),
    ],
    id="sidebar",
)

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), navbar, sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    return callbacks.render_page_content(pathname)


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    return callbacks.toggle_classname(n, classname)


@app.callback(
    Output("collapse", "is_open"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    return callbacks.toggle_collapse(n, is_open)


@app.callback(
    Output("user-list", "children"),
    [Input("button-0", "n_clicks"),
     Input("button-1", "n_clicks"),
     Input("button-2", "n_clicks"),
     Input('pagination', 'active_page')],
    prevent_initial_call=True
)
def update_user_list(button0_clicks, button1_clicks, button2_clicks, active_page):
    return callbacks.update_user_list(button0_clicks, button1_clicks, button2_clicks, active_page)


@app.callback(
    Output('output-recommendations-multiple', 'children'),
    [Input('user-dropdown', 'value'),
     Input('model-dropdown', 'value')]
)
def update_recommendations_model(selected_user, selected_model):
    return callbacks.update_recommendations_model(selected_user, selected_model)


@app.callback(
    Output('model-comparison-graph', 'figure'),
    Input('user-dropdown', 'value')
)
def update_model_comparison_graph(selected_user):
    return callbacks.update_model_comparison_graph(selected_user)


if __name__ == "__main__":
    app.run_server(debug=True)
