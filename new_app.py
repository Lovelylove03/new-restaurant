import streamlit as st
import pandas as pd
import requests

# Replace with your Yelp API key
YELP_API_KEY = 'QqpMmw2tuGPpmPbikkghpkgZFvxfdetl3NPhp6THcPA8NcuRRDBmD8sY-QAqxdjD-Fe4KAOwvhkVp7xFmG2jbFiND-amRCkloLeHOn9ncLlHQdNHBKx10xd2AiPPZnYx'
YELP_API_URL = 'https://api.yelp.com/v3/businesses/search'

def set_background(color=None):
    st.markdown(
        f"""
        <style>
        .stApp {{
            {'background-color: ' + color + ';' if color else ''}
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def fetch_restaurant_data(term, location, price_range, sort_by='rating', limit=5):
    headers = {
        'Authorization': f'Bearer {YELP_API_KEY}',
    }
    params = {
        'term': term,
        'location': location,
        'price': price_range,
        'sort_by': sort_by,
        'limit': limit
    }
    try:
        response = requests.get(YELP_API_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return {}

@st.cache_data
def load_data():
    file_path = 'https://raw.githubusercontent.com/Lovelylove03/new-restaurant/main/df_mich.csv'
    data = pd.read_csv(file_path)
    return data

def main():
    # Set green palette background
    set_background(color="#e0f7e9")  # Light green background color

    st.title("Gastronomic Getaway")

    data = load_data()

    st.sidebar.header('Your Search')

    # Select country
    country = st.sidebar.selectbox("Choose Country", sorted(data['Country'].unique()))

    # Add an option for "All Towns" to allow country-only filtering
    filtered_towns = data[data['Country'] == country]['Town'].unique()
    town_options = ['All Towns'] + sorted(filtered_towns)
    town = st.sidebar.selectbox("Choose Town", town_options)

    cuisine_preference = st.sidebar.selectbox("Choose
