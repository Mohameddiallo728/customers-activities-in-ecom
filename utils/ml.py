from lightfm import cross_validation, LightFM
from lightfm.data import Dataset
from lightfm.evaluation import auc_score
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def map_frequency_to_numeric(frequency):
    mapping = {
        'Fortnightly': 15,  # each 15 days that means each 2 weeks (Bi-weekly)
        'Weekly': 7,  # each 7 days that means each week
        'Annually': 365,  # each 365 days that means once a year
        'Quarterly': 120,  # each 120 days that means each 4 months
        'Every 3 Months': 90,  # each 90 days that means each 3 months
        'Bi-Weekly': 14,  # each 14 days that means each 2 weeks
        'Monthly': 30  # each 30 days that means each months
    }
    return mapping.get(frequency, 0)  # Default to 0 if the value is not in the mapping


def get_category_label(total_purchase_amount):
    # Déterminez une interprétation en fonction de la somme totale des montants d'achat
    if total_purchase_amount >= 50000:
        return 'Très Grand Acheteur'
    elif total_purchase_amount >= 40000:
        return 'Grand Acheteur'
    elif total_purchase_amount >= 30000:
        return 'Acheteur Moyen'
    elif total_purchase_amount >= 20000:
        return 'Petit Acheteur'
    elif total_purchase_amount >= 10000:
        return 'Très Petit Acheteur'
    else:
        return 'Minimal Acheteur'


def segment_by_purchases_frequency(data):
    data['Frequency of Purchases'] = data['Frequency of Purchases'].apply(map_frequency_to_numeric)

    features = data[['Age', 'Purchase Amount (USD)', 'Frequency of Purchases']]

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=4, random_state=42)
    data['Cluster'] = kmeans.fit_predict(features_scaled)
    silhouette_avg = silhouette_score(features_scaled, data['Cluster'])
    return data, silhouette_avg


def create_and_tune_recommender(raw_data):
    def evaluate_models(loss_functions, hyperparameters, interactions):
        """Evaluates different model configurations and returns the best model."""
        best_score = 0
        best_model = None
        for loss_function in loss_functions:
            for params in hyperparameters:
                model = LightFM(loss=loss_function, **params)
                model.fit(interactions, epochs=30, num_threads=2)

                # Evaluate performance using appropriate metrics
                test_auc = auc_score(model, test).mean()
                if test_auc > best_score:
                    best_score = test_auc
                    best_model = model

        return best_model, best_score

    encoded_data = raw_data.copy()
    # encoded_data = preprocess_data(raw_data.copy())
    dataset = Dataset()
    dataset.fit(users=encoded_data['Customer ID'], items=encoded_data['product id'])
    (interactions, _) = dataset.build_interactions(
        [(user, item, 1) for user, item in zip(encoded_data['Customer ID'], encoded_data['product id'])])

    # Split interactions into training and testing sets
    train, test = cross_validation.random_train_test_split(interactions)

    # Define loss functions and hyperparameters to try
    loss_functions = ['warp', 'bpr']
    hyperparameters = [
        # Explore different learning rates
        {'learning_rate': 0.01, 'no_components': 32},
        {'learning_rate': 0.05, 'no_components': 32},
        {'learning_rate': 0.1, 'no_components': 32},
        {'learning_rate': 0.05, 'no_components': 64},
        {'learning_rate': 0.1, 'no_components': 64},
        {'learning_rate': 0.01, 'no_components': 128},
        {'learning_rate': 0.05, 'no_components': 128},
        {'learning_rate': 0.1, 'no_components': 128},
    ]

    best_model, best_score = evaluate_models(loss_functions, hyperparameters, train)
    return best_model, best_score
