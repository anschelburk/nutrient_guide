import streamlit as st
# import numpy as np
# import pandas as pd
import requests
from daily_values import daily_values as dv
import requests

# map_data = pd.DataFrame(
#     np.random.randn(1000,2) / [50,50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)

DEMO_KEY = "DEMO_KEY"
search_endpoint = "https://api.nal.usda.gov/fdc/v1/foods/search"


st.title('Nutrition Guide')
search = st.text_input('Search an ingredient:')
st.write(f'You searched: {search}')

st.title('Results:')
r = requests.get(search_endpoint, params={"query": search, "api_key":DEMO_KEY}) # using the requests library to make a GET request to the API
results = st.write(r.json().get('foods')[0].get('foodNutrients')) # getting the JSON object of the response and navigating to the foodNutrients key

# further explanation of the code:
# r.json() returns a JSON object of the response
# r.json().get('foods') returns a list of foods
# r.json().get('foods')[0] returns the first food in the list
# r.json().get('foods')[0].get('foodNutrients') returns the foodNutrients of the first food in the list

"""
You can further use the api explorer here: https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/getFoodsSearch
to see the different parameters you can use to customize your search and review the 'shape' of the response.
"""




# results = pd.DataFrame.query(selfexpr=search.lower(), )
# results = dv.get(search.lower())
# st.write(results)

