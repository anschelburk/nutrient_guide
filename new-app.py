import streamlit as st
# import numpy as np
import pandas as pd
import requests
import json
from daily_values import daily_values as dv

# map_data = pd.DataFrame(
#     np.random.randn(1000,2) / [50,50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)
# search_endpoint = "https://api.nal.usda.gov/fdc/v1/foods/list"

DEMO_KEY = "DEMO_KEY"
search_endpoint = "https://api.nal.usda.gov/fdc/v1/foods/search"


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
st.write(f'Food Name: {results_name}')
# st.write(results_nutrients[0].get('nutrientName'))
# st.write(results_nutrients[0])
st.write('Food Nutrients (filtered table):')
st.write(results_df)
# st.dataframe(
#     data=results_nutrients,
#     column_order=('nutrientName', 'value', 'unitName')
#     # column_config={
#     #     'nutrientName': st.column_config.Column(label = 'Nutrient'),
#     #     'value': st.column_config.Column(label = 'Amount'),
#     #     'unitName': st.column_config.Column(label = 'Units')
#     # }
# )
# st.dataframe(data=results_nutrients, column_order={'nutrientName', 'value', 'unitName'})
st.write('Food Nutrients (full table, reference):')
st.dataframe(results_nutrients)
st.write('Food Nutrients (unformatted, reference):')
st.write(results_nutrients)


# """
# You can further use the api explorer here: https://app.swaggerhub.com/apis/fdcnal/food-data_central_api/1.0.1#/FDC/getFoodsSearch
# to see the different parameters you can use to customize your search and review the 'shape' of the response.
# """




# results = pd.DataFrame.query(selfexpr=search.lower(), )
# results = dv.get(search.lower())
# st.write(results)

