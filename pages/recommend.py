from lightfm import LightFM, cross_validation
from lightfm.data import Dataset
from lightfm.evaluation import auc_score

from utils.data_loader import load_encoded
from utils.visuals import *

data = load_encoded()

# Créer une instance de Dataset et construire les interactions utilisateur-item
dataset = Dataset()
dataset.fit(users=data['Customer ID'], items=data['product id'])
(interactions, _) = dataset.build_interactions(
    [(user, item, 1) for user, item in zip(data['Customer ID'], data['product id'])])

# Diviser les données en ensembles d'apprentissage et de test
train, test = cross_validation.random_train_test_split(interactions)

# Créer le modèle LightFM
model = LightFM(loss='warp')
model.fit(train, epochs=30, num_threads=2)

# Évaluer le modèle sur l'ensemble de test
test_auc = auc_score(model, test).mean()
customer_ids = sorted(data['Customer ID'].unique())
# Mise en page de l'application
layout = html.Div([
    html.H1("Recommandation de produits / Articles"),
    html.Hr(),
    # dbc.Card(
    #     dbc.CardBody(
    #         [
    #             html.H5(f"AUC : {round(float(test_auc) * 100, 2)}%", className="card-title"),
    #             html.P("L'AUC est une mesure couramment utilisée pour évaluer la performance d'un modèle de "
    #                    "classification", className="card-text",
    #                    ),
    #         ]
    #     ),
    #     className="w-100 mb-12",
    # ),
    html.P("Sélectionnez un utilisateur :"),
    dcc.Dropdown(
        id='user-dropdown',
        options=[{'label': str(user), 'value': user} for user in customer_ids],
        value=customer_ids[0],
        style={"height": "100%"}
    ),
    html.Hr(),
    dbc.Button("Obtenir des recommandations",
               color="primary",
               id='get-recommendations-button',
               className=""
               ),
    html.Hr(),
    html.Ul(id='recommendations-list')
])


# Fonction de recommandation mise à jour
def get_recommendations_info(user_id, num_recommendations=6):
    # Convertir user_id en entier
    user_id = int(user_id)

    # Obtenir les produits déjà achetés par l'utilisateur
    known_positives = data[data['Customer ID'] == user_id]['product id'].unique()

    # Prédire les produits que l'utilisateur pourrait aimer
    unique_product_ids = data['product id'].unique()
    scores = model.predict(user_id, list(range(len(unique_product_ids))))

    # Trier les produits par score de prédiction
    top_items_indices = scores.argsort()[-1:-num_recommendations - 1:-1]
    top_items = unique_product_ids[top_items_indices]
    top_scores = scores[top_items_indices]

    # Exclure les produits déjà achetés
    recommendations = [(item, score) for item, score in zip(top_items, top_scores) if item not in known_positives][
                      :num_recommendations]

    # Obtenir les détails des produits recommandés
    recommendations_info = data[data['product id'].isin([item[0] for item in recommendations])]

    return recommendations_info, top_scores[:num_recommendations]


# Callback pour mettre à jour les recommandations lorsque le bouton est cliqué
def update_recommendations(n_clicks, user_id):
    if n_clicks is None:
        return []

    # Obtenir les recommandations pour l'utilisateur sélectionné
    recommendations_info, scores = get_recommendations_info(user_id)

    # Afficher les recommandations
    product_cards = [
        generate_product_visuel(row, score)
        for (_, row), score in zip(recommendations_info.iterrows(), scores)
    ]

    return dbc.Row(product_cards, className="mb-4")
