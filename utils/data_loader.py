import pandas as pd

from utils.visuals import apply_kmeans


def load_activities():
    # Load your data here
    data = pd.read_csv('data/cleaned/activities.csv', encoding='ISO-8859-1')
    return data


def load_customers():
    # Load your data here
    data = pd.read_csv('data/cleaned/customers.csv', encoding='ISO-8859-1')
    return data


def load_products():
    # Load your data here
    data = pd.read_csv('data/cleaned/products.csv', encoding='ISO-8859-1')
    return data


def load_recommendations():
    # Load your data here
    data = pd.read_csv('data/cleaned/recommendations.csv', encoding='ISO-8859-1')
    return data


def load_with_kmean():
    df = load_activities()
    data = apply_kmeans(df)
    return data
