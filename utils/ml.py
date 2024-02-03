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

