import streamlit as st
# import numpy as np
import pandas as pd
from daily_values import daily_values as dv
import requests

# map_data = pd.DataFrame(
#     np.random.randn(1000,2) / [50,50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)

st.title('Nutrition Guide')
search = st.text_input('Search an ingredient:')
st.write(f'You searched: {search}')

r = requests.get(search_endpoint, params={"query": search, "api_key":DEMO_KEY}) # using the requests library to make a GET request to the API
results_name = r.json().get('foods')[0].get('description')
results_nutrients = r.json().get('foods')[0].get('foodNutrients') # getting the JSON object of the response and navigating to the foodNutrients key
results_df = pd.DataFrame(data=results_nutrients, columns=['nutrientName', 'value', 'unitName'])

# further explanation of the code:
# r.json() returns a JSON object of the response
# r.json().get('foods') returns a list of foods
# r.json().get('foods')[0] returns the first food in the list
# r.json().get('foods')[0].get('foodNutrients') returns the foodNutrients of the first food in the list


st.title('Results:')
results = pd.DataFrame.query(selfexpr=search.lower(), )
# results = dv.get(search.lower())
# st.write(results)

