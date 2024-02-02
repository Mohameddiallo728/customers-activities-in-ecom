import base64
from io import BytesIO

import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from dash import dcc, html
from wordcloud import WordCloud

from utils.ml import segment_by_purchases_frequency, get_category_label

layout_style = dict(
    plot_bgcolor='#f9f9f9',
    paper_bgcolor='#f9f9f9',
    title_font_size=17
)


def generate_grouped_cards(customers, products):
    sales_icon = html.Img(src="/assets/sales_icon.png",
                          style={'width': '80px', 'height': '80px', 'position': 'absolute', 'top': '60px',
                                 'right': '10px'})
    users_icon = html.Img(src="/assets/users-colored.png",
                          style={'width': '80px', 'height': '80px', 'position': 'absolute', 'top': '60px',
                                 'right': '20px'})
    age_icon = html.Img(src="/assets/age_icon.png",
                        style={'width': '80px', 'height': '80px', 'position': 'absolute', 'top': '60px',
                               'right': '20px'})
    box_icon = html.Img(src="/assets/best-product.png",
                        style={'width': '70px', 'height': '70px', 'position': 'absolute', 'top': '60px',
                               'right': '20px'})

    purchase = [
        dbc.CardHeader("Ventes"),
        dbc.CardBody(
            [
                html.H1("$ {:,.2f}".format(customers['Purchase Amount (USD)'].sum()), className="card-title"),
                html.P("Montant total de ventes", className="card-text"),
                sales_icon
            ]
        ),
    ]

    customer = [
        dbc.CardHeader("Clients"),
        dbc.CardBody(
            [
                html.H1(str(customers['Customer ID'].nunique()), className="card-title"),
                html.P("Nombre de clients", className="card-text"),
                users_icon
            ]
        ),
    ]

    age = [
        dbc.CardHeader("Ages"),
        dbc.CardBody(
            [
                html.H1("{} ans".format(round(customers['Age'].mean())), className="card-title"),
                html.P("Moyenne d'âges", className="card-text"),
                age_icon
            ]
        ),
    ]

    product = [
        dbc.CardHeader("Articles"),
        dbc.CardBody(
            [
                html.H1(str(products['Uniqe Id'].nunique()), className="card-title"),
                html.P("Nombre total de produit en stock", className="card-text"),
                box_icon
            ]
        ),
    ]

    cards = html.Div([
        dbc.Row(
            [
                dbc.Col(dbc.Card(purchase, color="cadetblue", inverse=True)),
                dbc.Col(dbc.Card(customer, color="black", inverse=True)),
                dbc.Col(dbc.Card(age, color="#609FFF", inverse=True)),
                dbc.Col(dbc.Card(product, color="rebeccapurple", inverse=True)),
            ],
            className="mb-3",
        )
    ])
    return cards


def generate_product_card(product_id, recommendations):
    product_info = recommendations[recommendations['product id'] == product_id].iloc[0]

    # Création de la card selon le modèle fourni
    card = dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=product_info['Image'],
                            className="img-fluid rounded-start",
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H5(product_info['Product Name'], className="card-title"),
                                html.H1(f"$ {product_info['Selling Price']}", className="card-text"),
                                dbc.Button("Voir le produit", color="primary", href=product_info["Product Url"])
                            ]
                        ),
                        className="col-md-8",
                    ),
                ],
                className="g-0 d-flex align-items-center",
            )
        ],
        className="mb-3",
        style={"maxWidth": "540px"},
    )
    return card


def generate_product_visuel(product_info):
    # Création de la card selon le modèle fourni
    info_elements = html.Span(
        [
            dbc.Badge(
                product_info['Sub Category'],
                color="secondary",
                text_color="black",
                className="border me-1",
            ),
            dbc.Badge(
                "Model : " + product_info['Model Number'],
                color="warning",
                text_color="black",
                className="border me-1",
            ),
            dbc.Badge(
                f"Poids : {product_info['Shipping Weight (lbs)']} lbs",
                color="secondary",
                text_color="black",
                className="border me-1",
            ),
            html.Br(), html.Br(),
        ]
    )
    card = dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=product_info['Image'],
                            className="img-fluid rounded-start",
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H5(product_info['Product Name'], className="card-title"),
                                info_elements,
                                html.H1(f"$ {product_info['Selling Price']}", className="card-text price"),
                                dbc.Button("Voir le produit", color="primary", href=product_info["Product Url"],
                                           className="see-product")
                            ]
                        ),
                        className="col-md-8",
                    ),
                ],
                className="g-0 d-flex align-items-center",
            )
        ],
        className="mb-3",
        style={"maxWidth": "700px", "marginRight": "20px", "marginLeft": "20px"},
    )
    return card


def generate_top_interactive_products_card(data):
    # Obtenir les 10 produits les plus interactifs
    top_products = data.groupby('Product Name').size().reset_index(name='Count')
    top_products = top_products.nlargest(10, 'Count')

    # Joindre les informations sur les produits avec le reste des colonnes
    top_products = pd.merge(top_products, data, on='Product Name', how='left')

    # Créer une liste de cartes pour chaque produit
    product_cards = [generate_product_visuel(product_info) for _, product_info in top_products.iterrows()]

    # Placez les cartes dans une Row
    product_cards_row = dbc.Row(product_cards, className="mb-4")

    return product_cards_row


def generate_product_card2(product_id, recommendations):
    product_info = recommendations[recommendations['product id'] == product_id].iloc[0]

    # Création d'éléments graphiques pour afficher les informations
    info_elements = [
        html.P(f"Category: {product_info['product_category']}", className="card-text"),
        html.P(f"Sub Category: {product_info['Sub Category']}", className="card-text"),
        html.P(f"Weight: {product_info['Shipping Weight (lbs)']} lbs", className="card-text"),
        html.P(f"Dimensions: {product_info['Length']} x {product_info['Width']} x {product_info['Height']}",
               className="card-text"),
        html.P(f"Selling Price: ${product_info['Selling Price']}", className="card-text", style={"font-size": "1.5em"}),
        html.P(f"Model Number: {product_info['Model Number']}", className="card-text"),
    ]

    card = dbc.Card(
        [
            dbc.CardImg(src=product_info['Image'], top=True),
            dbc.CardBody(
                [
                    html.H4(product_info['Product Name'], className="card-title"),
                    *info_elements,  # Utilisation de l'opérateur * pour déballer la liste
                    dbc.Button("Voir le produit", color="primary", href=product_info["Product Url"])
                ]
            ),
        ],
        style={"width": "18rem", "margin": "10px"},
    )
    return card


def generate_gender_pie_chart(data):
    gender_colors = [
        '#609FFF',  # Male
        '#FFBF6D',  # Female
    ]
    # Pie chart avec Plotly Express
    fig = px.pie(data, names='Gender', title='Répartition des Genres',
                 labels={'Gender': 'Count'},
                 height=450, hole=0.3, color_discrete_sequence=gender_colors)

    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_category_distribution(data):
    # Countplot pour 'Category'
    fig = px.histogram(data, x='Category', title='Répartition des Catégories',
                       labels={'Category': 'Count'},
                       height=450, barmode='overlay', color='Category')
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_purchase_frequency(data):
    # Group data by 'Frequency of Purchases' and calculate the sum of 'Purchase Amount (USD)'
    frequency_sum = data.groupby('Frequency of Purchases')['Purchase Amount (USD)'].sum().reset_index(
        name='Total Purchase Amount')
    # Create a bar chart for the sum of purchase amounts by frequency
    fig = px.bar(frequency_sum, x='Frequency of Purchases', y='Total Purchase Amount', title='Fréquence des achats',
                 color='Frequency of Purchases')
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_size_distribution(data):
    # Countplot pour 'Size'
    fig = px.histogram(data, x='Size', title='Répartition des Tailles', labels={'Size': 'Count'},
                       height=400, barmode='overlay', color='Size')

    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_season_countplot(data):
    # Countplot pour 'Season'
    fig = px.histogram(data, x='Season', title='Répartition des Saisons',
                       labels={'Season': 'Count'},
                       height=400, barmode='overlay', color='Season')
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_shipping_type_countplot(data):
    # Countplot pour 'Shipping Type'
    fig = px.histogram(data, x='Shipping Type', title='Répartition des Types d\'Expédition',
                       labels={'Shipping Type': 'Count'},
                       height=400, barmode='overlay', color='Shipping Type')
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_item_purchased_countplot(data):
    # Countplot pour 'Item Purchased'
    fig = px.histogram(data, x='Item Purchased', title='Répartition des Articles Achetés',
                       labels={'Item Purchased': 'Count'},
                       height=400, color_discrete_sequence=['skyblue'])
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_location_countplot(data):
    # Countplot pour 'Location'
    fig = px.histogram(data, x='Location', title='Répartition des Locations',
                       labels={'Location': 'Count'},
                       height=400, color_discrete_sequence=['#609FFF'])
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_sales_map(data):
    # Create a scatter map using latitude and longitude columns
    fig = px.scatter_mapbox(data,
                            lat='Latitude',
                            lon='Longitude',
                            hover_name='Location',
                            hover_data={'Purchase Amount (USD)': ':,.2f'},
                            color='Purchase Amount (USD)',
                            title='Carte des ventes par locations',
                            height=750,
                            mapbox_style='carto-positron',
                            zoom=3)

    # Update layout with any additional styling
    fig.update_layout(layout_style)

    # Return the Dash Graph component with the generated figure
    return dcc.Graph(figure=fig)


def generate_sales_over_time(data):
    # Convertissez la colonne 'Date' en format de date si ce n'est pas déjà fait
    data['Date'] = pd.to_datetime(data['Date'])

    # Extraitz la colonne 'Month' à partir de la colonne 'Date'
    data['Month'] = data['Date'].dt.to_period('M').astype(str)

    # Calculez la somme des ventes par mois
    monthly_sales = data.groupby('Month')['Purchase Amount (USD)'].sum().reset_index()

    # Utilisez un graphique de ligne pour représenter l'évolution des ventes par mois
    fig = px.line(monthly_sales, x='Month', y='Purchase Amount (USD)',
                  title='Évolution des Ventes par Mois')
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_sales_by_category(data):
    fig = px.pie(data, names='Category', title='Répartition des Ventes par Catégorie', hole=0.3)
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_purchase_by_gender(data):
    gender_colors = [
        '#FFBF6D',  # Male
        '#609FFF'  # Female
    ]
    # Calculez la somme des montants d'achats par genre
    purchase_by_gender = data.groupby('Gender')['Purchase Amount (USD)'].sum().reset_index()

    # Utilisez un graphique de barres pour représenter la somme des montants d'achats par genre
    fig = px.bar(purchase_by_gender, x='Gender', y='Purchase Amount (USD)', color='Gender',
                 title='Influence du Genre sur les Achats', color_discrete_sequence=gender_colors)
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_age_vs_purchase(data):
    # Calculez la somme des montants d'achats par groupe d'âge et genre
    age_vs_purchase = data.groupby(['Age', 'Gender'])['Purchase Amount (USD)'].sum().reset_index()

    # Utilisez un graphique de dispersion pour représenter la relation entre l'âge des clients et le montant des
    # achats avec légende par genre
    fig = px.line(age_vs_purchase, x='Age', y='Purchase Amount (USD)', color='Gender',
                  title='Relation entre l\'Âge des Clients et le Montant des Achats',
                  labels={'Purchase Amount (USD)': 'Montant des Achats (USD)', 'Age': 'Âge'})
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_sales_by_size(data):
    # Calculez la somme des montants d'achats par taille et catégorie
    sales_by_size = data.groupby(['Size'])['Purchase Amount (USD)'].sum().reset_index()

    # Utilisez un graphique de barres pour représenter la somme des montants d'achats par taille avec légende par catégorie
    fig = px.bar(sales_by_size, x='Size', y='Purchase Amount (USD)', color='Size',
                 title='Impact de la Taille sur les Ventes',
                 labels={'Purchase Amount (USD)': 'Montant des Achats (USD)', 'Size': 'Taille'})
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_sales_by_season(data):
    # Calculez la somme des montants d'achats par saison et genre
    sales_by_season = data.groupby(['Season'])['Purchase Amount (USD)'].sum().reset_index()

    # Utilisez un graphique de barres pour représenter la somme des montants d'achats par saison avec légende par genre
    fig = px.bar(sales_by_season, x='Season', y='Purchase Amount (USD)', color='Season',
                 title='Analyse des Saisons sur les Ventes',
                 labels={'Purchase Amount (USD)': 'Montant des Achats (USD)', 'Season': 'Saison'})
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_interaction_type_pie_chart(data):
    # Utilisez Plotly Express pour créer un donut chart interactif
    fig = px.pie(data, names='Interaction type', title='Répartition des Types d\'Interactions',
                 labels={'Interaction type': 'Type d\'Interaction'},
                 height=450, color='Interaction type', hole=0.3)
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_interaction_heatmap(data):
    # Pivoter les données pour obtenir une table pour la heatmap
    heatmap_data = data.pivot_table(index='Interaction type', columns='Heure', values='user id', aggfunc='count')

    # Utiliser Plotly Express pour créer la heatmap
    fig = px.imshow(heatmap_data,
                    labels=dict(x='Heure de la Journée', y='Type d\'Interaction',
                                color='Nombre d\'Interactions'),
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    color_continuous_scale='viridis',
                    title='Heatmap d\'Heure des Interactions')

    fig.update_layout(xaxis_title='Heure de la Journée', yaxis_title='Type d\'Interaction',
                      coloraxis_colorbar=dict(title='Nombre d\'Interactions'))
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_interaction_over_time(data):
    # Convertir la colonne 'Date' en format datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Extraitz la colonne 'Month' à partir de la colonne 'Date'
    data['Month'] = data['Date'].dt.to_period('M').astype(str)

    # Calculez le nombre d'interactions par mois pour chaque type d'interaction
    monthly_interactions = data.groupby(['Month', 'Interaction type'])['user id'].count().reset_index()

    # Utilisez un graphique de ligne pour représenter l'évolution des interactions par mois avec différentes couleurs pour chaque type d'interaction
    fig = px.line(monthly_interactions, x='Month', y='user id', color='Interaction type',
                  title='Évolution des Interactions par Mois',
                  labels={'user id': 'Nombre d\'Interactions', 'Month': 'Mois'},
                  category_orders={'Month': sorted(data['Month'].unique())})
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_temporal_interaction_plot(data):
    # Convertir la colonne 'Date' en format datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Extraire le mois à partir de la colonne 'Date' et le convertir en chaînes de caractères
    data['Month'] = data['Date'].dt.to_period('M').astype(str)

    # Créer un lineplot par mois pour chaque type d'interaction avec Plotly Express
    fig = px.line(data, x='Month', y='user id', color='Interaction type', markers=True,
                  title='Graphique Temporel des Interactions',
                  labels={'user id': 'Nombre d\'Interactions', 'Month': 'Mois'},
                  category_orders={'Month': sorted(data['Month'].unique())})

    fig.update_layout(xaxis_title='Mois', yaxis_title='Nombre d\'Interactions')
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_top_interactive_products_barplot(data):
    # Obtenir les 10 produits les plus interactifs
    top_products = data['Product Name'].value_counts().nlargest(10)

    # Utiliser Plotly Express pour créer le barplot interactif
    fig = px.bar(top_products, x=top_products.values, y=top_products.index,
                 orientation='h', color=top_products.values,
                 labels={'y': 'Nom du Produit', 'x': 'Nombre d\'Interactions'},
                 title='Top 10 des Produits les Plus Interactifs')

    fig.update_layout(xaxis_title='Nombre d\'Interactions', yaxis_title='Nom du Produit')
    fig.update_layout(layout_style)
    return dcc.Graph(figure=fig)


def generate_wordcloud(data):
    # Concaténer tous les mots de la colonne 'Item Purchased'
    text = ' '.join(data['Item Purchased'])

    # Générer le nuage de mots
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Enregistrer l'image du nuage de mots dans BytesIO
    img_stream = BytesIO()
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(img_stream, format='png')
    plt.close()

    # Convertir l'image en base64 pour l'afficher dans Dash
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    # Créer une balise img avec l'image encodée en base64
    wordcloud_image = html.Img(src=f'data:image/png;base64,{img_base64}', style={'width': '100%', 'height': '100%'})

    return wordcloud_image


def get_segments_by_purchases_frequency(data):
    data = segment_by_purchases_frequency(data)[0]
    categories = data['Cluster'].unique()
    cards = []

    for category in categories:
        filtered_data = data[data['Cluster'] == category]
        # Calcul des pourcentages d'hommes et de femmes
        total_gender_count = len(filtered_data)
        male_percentage = round(len(filtered_data[filtered_data['Gender'] == 'Male']) / total_gender_count * 100)
        female_percentage = round(len(filtered_data[filtered_data['Gender'] == 'Female']) / total_gender_count * 100)

        # Création de deux divs colorés
        male_div = html.Div([
            html.P(f"{male_percentage}% Homme", className="card-text"),
        ], style={'background-color': '#609FFF', 'color': 'white', 'padding': '5px', 'margin': '5px',
                  'border-radius': '3px', 'text-align': 'center'})

        female_div = html.Div([
            html.P(f"{female_percentage}% Femme", className="card-text"),
        ], style={'background-color': '#FFBF6D', 'color': 'white', 'padding': '5px', 'margin': '5px',
                  'border-radius': '3px', 'text-align': 'center'})

        info_elements = [
            dbc.Row([
                dbc.Col(male_div),
                dbc.Col(female_div),
            ], className="mb-4", style={'borderBottom': '1px solid #ccc', 'paddingBottom': '10px'}),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        html.H1(len(filtered_data), className="card-title"), html.Span("Clients")
                    ]), style={'borderRight': '1px solid #ccc', 'marginRight': '10px', 'textAlign': 'center'}),
                    dbc.Col(html.Div([
                        html.H1(round(filtered_data['Age'].mean()), className="card-title"), html.Span("Âge moyen")
                    ]), style={'borderRight': '1px solid #ccc', 'marginRight': '10px', 'textAlign': 'center'}),
                    dbc.Col(html.Div([
                        html.H1(f"{filtered_data['Review Rating'].mean():.1f}", className="card-title"),
                        html.Span("Note")
                    ]), style={'textAlign': 'center'}),
                ],
                className="g-0", style={'borderBottom': '1px solid #ccc', 'paddingBottom': '20px'}
            ),
            html.Hr(),
            html.H1(f"$ {'{:,}'.format(filtered_data['Purchase Amount (USD)'].sum()).replace(',', ' ')}",
                    className="card-title", style={'textAlign': 'center'}),
        ]
        card_content = [
            dbc.CardHeader(f"{get_category_label(filtered_data['Purchase Amount (USD)'].sum())}",
                           style={'cursor': 'pointer'}),
            dbc.CardBody([
                *info_elements,
                html.Hr(),
                dbc.Button("Afficher la liste", color="primary", id=f"button-{category}", n_clicks=0),
            ]),
        ]

        card = dbc.Col(
            dbc.Card(card_content, color="#f9f9f9", inverse=True, id=f"cluster-card-{category}",
                     className="text-black"))

        cards.append(card)

    return html.Div([
        dbc.Row(cards, className="mb-6")
    ])
