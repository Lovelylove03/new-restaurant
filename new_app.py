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
    # Ensure parameters are properly formatted
    params = {
        'term': term,
        'location': location,
        'price': ','.join(price_range) if isinstance(price_range, list) else price_range,  # Correct format
        'sort_by': sort_by,
        'limit': limit
    }
    try:
        response = requests.get(YELP_API_URL, headers=headers, params=params)
        response.raise_for_status()  # This will raise an error for 4xx/5xx responses
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

    cuisine_preference = st.sidebar.selectbox("Choose Cuisine Type", data['Cuisine'].unique())

    # Add an option for "No Award" to allow filtering without an award
    unique_awards = ['No Award'] + sorted(data['Award'].dropna().unique())
    selected_award = st.sidebar.selectbox("Choose Award", unique_awards)

    # Using numerical rates instead of symbols
    price_options = {1: '1', 2: '2', 3: '3', 4: '4'}
    selected_price = st.sidebar.selectbox("Choose Rates (1=Low, 4=High)", list(price_options.keys()))
    yelp_price = price_options.get(selected_price, '1,2,3,4')

    if st.sidebar.button("Get Recommendations"):
        # Build the location parameter based on user input
        if town == 'All Towns':
            location = country
        else:
            location = f"{town}, {country}"
        
        # Fetch restaurant data
        data = fetch_restaurant_data(term=cuisine_preference, location=location, price_range=yelp_price, limit=5)
        
        if 'businesses' in data:
            businesses = data['businesses']
            
            # Filter results based on the selected award
            if selected_award != 'No Award':
                filtered_businesses = [business for business in businesses if selected_award in [category['title'] for category in business.get('categories', [])]]
            else:
                filtered_businesses = businesses
            
            # Show available recommendations if selected criteria is not available
            if not filtered_businesses:
                st.write("No results found for the selected criteria. Showing all available recommendations.")
                filtered_businesses = businesses  # Show all available businesses
            
            # Display results
            if filtered_businesses:
                st.write(f"Showing results for {selected_award if selected_award != 'No Award' else 'all available awards'} in {location}.")
                for business in filtered_businesses:
                    st.subheader(business['name'])
                    st.write(f"Rating: {business['rating']}")
                    st.write(f"Address: {', '.join(business['location']['display_address'])}")
                    st.write(f"Phone: {business.get('display_phone', 'N/A')}")
                    if business.get('image_url'):
                        st.image(business['image_url'])
                    st.markdown(f"[Visit Yelp Page]({business.get('url', 'N/A')})", unsafe_allow_html=True)
                    st.write("\n")
            else:
                st.write("No results found.")
        else:
            st.write("No results found.")
    
if __name__ == '__main__':
    main()
