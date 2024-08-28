import streamlit as st
import pandas as pd
import requests

# Replace with your Yelp API key
YELP_API_KEY = 'QqpMmw2tuGPpmPbikkghpkgZFvxfdetl3NPhp6THcPA8NcuRRDBmD8sY-QAqxdjD-Fe4KAOwvhkVp7xFmG2jbFiND-amRCkloLeHOn9ncLlHQdNHBKx10xd2AiPPZnYx'
YELP_API_URL = 'https://api.yelp.com/v3/businesses/search'

def set_background(image_url=None, color=None):
    st.markdown(
        f"""
        <style>
        .stApp {{
            {'background-image: url("' + image_url + '");' if image_url else ''}
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
    response = requests.get(YELP_API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return {}

@st.cache
def load_data():
    file_path = 'https://raw.githubusercontent.com/Lovelylove03/new-restaurant/main/df_mich.csv'
    data = pd.read_csv(file_path)
    return data

def main():
    set_background_image('1000_F_292203735_CSsyqyS6A4Z9Czd4Msf7qZEhoxjpzZl1.jpg')
    
    st.title("Gourmet Restaurant Recommendation System")

    data = load_data()

    st.sidebar.header('Your Search')
    country = st.sidebar.selectbox("Choose Country", sorted(data['Country'].unique()))
    filtered_towns = data[data['Country'] == country]['Town'].unique()
    town = st.sidebar.selectbox("Choose Town", sorted(filtered_towns))
    cuisine_preference = st.sidebar.selectbox("Choose Cuisine Type", data['Cuisine'].unique())

    price_options = {
        '€€€€': '1,2,3,4', '€€': '2', '€€€': '3', '$$': '2', '$$$$': '4'
    }
    selected_price = st.sidebar.selectbox("Choose Price Range", list(price_options.keys()))
    yelp_price = price_options.get(selected_price, '1,2,3,4')

    if st.sidebar.button("Get Recommendations"):
        data = fetch_restaurant_data(term=cuisine_preference, location=f"{town}, {country}", price_range=yelp_price, limit=5)
        if 'businesses' in data:
            businesses = data['businesses']
            for business in businesses:
                st.subheader(business['name'])
                st.write(f"Rating: {business['rating']}")
                st.write(f"Address: {', '.join(business['location']['display_address'])}")
                st.write(f"Phone: {business.get('display_phone', 'N/A')}")
                if business.get('image_url'):
                    st.image(business['image_url'])
                st.write(f"Price: {business.get('price', 'N/A')}")
                st.markdown(f"[Visit Yelp Page]({business.get('url', 'N/A')})", unsafe_allow_html=True)
                st.write("\n")
        else:
            st.write("No results found.")
    
if __name__ == '__main__':
    main()
