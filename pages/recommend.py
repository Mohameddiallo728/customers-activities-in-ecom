import plotly.graph_objects as go
from dash import dcc, html
from dash.exceptions import PreventUpdate
from surprise import Dataset, Reader, accuracy
from surprise.model_selection import train_test_split

from utils.data_loader import load_recommendations
from utils.ml import train_baseline_model
from utils.ml import train_knn_model
from utils.ml import train_knn_with_zscore_model
from utils.ml import train_svd_model
from utils.visuals import generate_product_card, generate_product_card2

# Chargement des données et prétraitement pour le modèle de filtrage collaboratif
recommendations = load_recommendations()

reader = Reader(rating_scale=(0, 5))
surprise_data = Dataset.load_from_df(recommendations[['Customer ID', 'product id', 'Review Rating']], reader)
trainset, _ = train_test_split(surprise_data, test_size=0.2)


# Initialisation des modèles
knn_model = train_knn_model(surprise_data)
baseline_model = train_baseline_model(surprise_data)
svd_model = train_svd_model(surprise_data)
knn_with_zscore_model = train_knn_with_zscore_model(surprise_data)

# Liste des modèles
models = {
    'KNN Basic': knn_model,
    'Baseline': baseline_model,
    'SVD': svd_model,
    'KNN With ZScore': knn_with_zscore_model
}


# Création de la mise en page Dash
layout = html.Div([
    html.H1("Recommandation de Produits"),

    html.Label("Sélectionnez un utilisateur:"),
    dcc.Dropdown(
        id='user-dropdown',
        options=[{'label': str(user), 'value': user} for user in recommendations['Customer ID'].unique()],
        value=recommendations['Customer ID'].iloc[0],
        style={'width': '50%'}
    ),

    html.Br(),

    html.Label("Sélectionnez le modèle de recommandation:"),
    dcc.Dropdown(
        id='model-dropdown',
        options=[{'label': model_name, 'value': model_name} for model_name in models.keys()],
        value='KNN Basic',
        style={'width': '50%'}
    ),

    html.Br(),

    html.Div(id='output-recommendations-multiple'),

    dcc.Graph(id='model-comparison-graph')
])


def update_recommendations_model(selected_user, num_products, selected_model):
    if selected_user is None:
        raise PreventUpdate  # Si l'utilisateur n'est pas sélectionné, arrêtez l'exécution

    model = models[selected_model]

    user_attributes = ['Color', 'Size', 'Purchase Amount (USD)', 'Season', 'Previous Purchases', 'Shipping Type',
                       'Interaction type', 'Selling Price', 'Shipping Weight (lbs)', 'Length', 'Width', 'Height']

    # Utiliser le modèle pour prédire les évaluations des produits pour l'utilisateur sélectionné
    user_ratings = recommendations[recommendations['Customer ID'] == selected_user][['Customer ID', 'product id',
                                                                                     'Review Rating'] + user_attributes]

    # Gestion des valeurs manquantes si nécessaire
    user_ratings = user_ratings.dropna()

    user_ratings = list(zip(*[user_ratings[c] for c in ['Customer ID', 'product id',
                                                        'Review Rating'] + user_attributes]))

    print(f"User Ratings: {user_ratings}")

    predictions = []
    for row in user_ratings:
        uid, iid, true_r, color, size, purchase_amount, season, previous_purchases, shipping_type, interaction_type, \
        selling_price, shipping_weight, length, width, height = row

        # Modifier cette ligne en fonction de votre modèle et des attributs supplémentaires
        pred = model.predict(uid, iid, r_ui=true_r, verbose=False)
        predictions.append((pred.uid, pred.iid, pred.est))

    print(f"Predictions: {predictions}")

    # Le tri et la sélection des produits recommandés doivent être en dehors de la boucle
    # Tri des prédictions par estimation décroissante
    sorted_predictions = sorted(predictions, key=lambda x: x[2], reverse=True)

    # Sélectionner les produits recommandés (plusieurs produits)
    recommended_products = set()  # Utilisez un ensemble pour garantir l'unicité des produits
    for uid, iid, est in sorted_predictions:
        if iid not in recommended_products and len(recommended_products) < num_products:
            recommended_products.add(iid)

    print(f"Recommended Products: {recommended_products}")

    product_cards = []
    for product_id in recommended_products:
        product = generate_product_card(product_id, recommendations)
        product_cards.append(product)

    return product_cards



def update_model_comparison_graph(selected_user):
    if selected_user is None:
        raise PreventUpdate

    # Créez une liste pour stocker les scores pour chaque modèle
    model_scores = {model_name: [] for model_name in models}
    num_time_periods = 10
    # Boucle sur les périodes de temps ou d'autres mesures
    for time_period in range(num_time_periods):  # Remplacez num_time_periods par le nombre approprié
        # Obtenez les scores pour chaque modèle
        for model_name, model in models.items():
            # Divisez le jeu de données en ensembles de formation et de test (effectué une seule fois)
            trainset, testset = train_test_split(surprise_data, test_size=0.2)

            # Entraînez le modèle sur l'ensemble de formation
            model.fit(trainset)

            # Faites des prédictions sur l'ensemble de test
            predictions = model.test(testset)

            # Calculez le RMSE en utilisant accuracy.rmse
            rmse = accuracy.rmse(predictions)

            # Ajoutez le score à la liste correspondante pour le modèle
            model_scores[model_name].append(rmse)

    # Créez un graphique linéaire interactif pour montrer la performance relative des modèles au fil du temps
    fig = go.Figure()

    for model_name, scores in model_scores.items():
        fig.add_trace(go.Scatter(x=list(range(num_time_periods)), y=scores, mode='lines', name=model_name))

    fig.update_layout(title='Performance relative des modèles de recommandation au fil du temps',
                      xaxis_title='Période de temps',
                      yaxis_title='RMSE')

    return fig
