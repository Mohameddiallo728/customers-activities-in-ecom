import pandas as pd

from utils.visuals import segment_by_purchases_frequency


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


def load_encoded():
    # Load your data here
    data = pd.read_csv('data/cleaned/data_encoded.csv', encoding='ISO-8859-1')
    return data
