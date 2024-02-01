from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from surprise import BaselineOnly, KNNWithZScore
from surprise import KNNBasic
from surprise import SVD
from surprise.model_selection import train_test_split


def map_frequency_to_numeric(frequency):
    mapping = {
        'Fortnightly': 2,
        'Weekly': 1,
        'Annually': 52,
        'Quarterly': 4,
        'Every 3 Months': 3,
        'Bi-Weekly': 2,  # Assumption: Bi-weekly is treated as fortnightly
        'Monthly': 12
    }
    return mapping.get(frequency, 0)  # Default to 0 if the value is not in the mapping


def get_category_label(category):
    labels = {
        0: 'Clients Sûrs',
        1: 'Clients Versatiles',
        2: 'Clients Nécessitant une Attention'
    }
    return labels.get(category, 'Autre')


def get_category_color(category):
    color_mapping = {
        0: "info",  # Couleur pour la catégorie 0
        1: "cadetblue",  # Couleur pour la catégorie 1
        2: "rebeccapurple",  # Couleur pour la catégorie 2
    }
    return color_mapping.get(category, "secondary")


def apply_kmeans(data):
    data['Frequency of Purchases'] = data['Frequency of Purchases'].apply(map_frequency_to_numeric)

    features = data[['Frequency of Purchases', 'Purchase Amount (USD)', 'Review Rating']]
    features = features.dropna()

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    num_clusters = 3
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    data['Cluster'] = kmeans.fit_predict(features_scaled)
    silhouette_avg = silhouette_score(features_scaled, data['Cluster'])
    print('silhouette_avg : ', silhouette_avg)
    print('Cl 0 : ', data[data['Cluster'] == 0]['Purchase Amount (USD)'].mean())
    print('Cl 1 :', data[data['Cluster'] == 1]['Purchase Amount (USD)'].mean())
    print('Cl 2 :', data[data['Cluster'] == 2]['Purchase Amount (USD)'].mean())
    return data, silhouette_avg


def train_knn_model(data):
    model = KNNBasic(sim_options={'user_based': True})
    trainset, _ = train_test_split(data, test_size=0.2)
    model.fit(trainset)
    return model


def train_baseline_model(data):
    model = BaselineOnly()
    trainset, _ = train_test_split(data, test_size=0.2)
    model.fit(trainset)
    return model


def train_svd_model(data):
    model = SVD()
    trainset, _ = train_test_split(data, test_size=0.2)
    model.fit(trainset)
    return model


def train_svd_model(data):
    model = SVD()
    trainset, _ = train_test_split(data, test_size=0.2)
    model.fit(trainset)
    return model


def train_knn_with_zscore_model(data):
    model = KNNWithZScore(sim_options={'user_based': True})
    trainset, _ = train_test_split(data, test_size=0.2)
    model.fit(trainset)
    return model
