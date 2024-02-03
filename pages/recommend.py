from lightfm import LightFM
from lightfm import cross_validation
from lightfm.data import Dataset

# Charger les données
from utils.data_loader import load_recommendations
from utils.visuals import *

data = load_recommendations()

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

# Mise en page de l'application
layout = html.Div([
    html.H1("Système de Recommandation"),

    html.Label("Sélectionnez un utilisateur :"),
    dcc.Dropdown(
        id='user-dropdown',
        options=[{'label': str(user), 'value': user} for user in data['Customer ID'].unique()],
        value=data['Customer ID'].iloc[0]
    ),

    html.Button("Obtenir des recommandations", id='get-recommendations-button'),

    html.H3("Produits recommandés :"),
    html.Ul(id='recommendations-list')
])


# Fonction de recommandation mise à jour
def get_recommendations_info(user_id, num_recommendations=5):
    # Convertir user_id en entier
    user_id = int(user_id)

    # Obtenir les produits déjà achetés par l'utilisateur
    known_positives = data[data['Customer ID'] == user_id]['product id'].unique()

    # Prédire les produits que l'utilisateur pourrait aimer
    unique_product_ids = data['product id'].unique()
    scores = model.predict(user_id, list(range(len(unique_product_ids))))

    # Trier les produits par score de prédiction
    top_items = unique_product_ids[scores.argsort()[-1:-num_recommendations - 1:-1]]

    # Exclure les produits déjà achetés
    recommendations = [item for item in top_items if item not in known_positives][:num_recommendations]

    # Obtenir les détails des produits recommandés
    recommendations_info = data[data['product id'].isin(recommendations)]

    return recommendations_info


# Callback pour mettre à jour les recommandations lorsque le bouton est cliqué
def update_recommendations(n_clicks, user_id):
    if n_clicks is None:
        return []

    # Obtenir les recommandations pour l'utilisateur sélectionné
    recommendations_info = get_recommendations_info(user_id)

    # Afficher les recommandations
    product_cards = [
        generate_product_visuel(row)  # Utilisez width=6 pour occuper la moitié de la ligne
        for _, row in recommendations_info.iterrows()
    ]

    return dbc.Row(product_cards, className="mb-4")
