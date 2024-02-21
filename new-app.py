import streamlit as st
# import numpy as np
import pandas as pd
import os
from daily_values import daily_values as dv
import requests
from pprint import pprint as pp

# map_data = pd.DataFrame(
#     np.random.randn(1000,2) / [50,50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)

search_endpoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'
DEMO_KEY = os.getenv('DEMO_KEY', "")
st.title('Nutrition Guide')
search = st.text_input('Search an ingredient:')
st.write(f'You searched: {search}')

r = requests.get(search_endpoint, params={"query": search, "api_key":DEMO_KEY}) # using the requests library to make a GET request to the API
results_name = r.json().get('foods')[0].get('description')
# results_name = 'Name-goes-here'
results_nutrients = r.json().get('foods')[0].get('foodNutrients') # getting the JSON object of the response and navigating to the foodNutrients key
results_df = pd.DataFrame(data=results_nutrients, columns=['nutrientName', 'value', 'unitName'])
results_df = results_df.rename(columns={'nutrientName': 'Nutrient Name', 'value': 'Amount', 'unitName': 'Units'})
# results_df = results_df.drop(columns=1)

# further explanation of the code:
# r.json() returns a JSON object of the response
# r.json().get('foods') returns a list of foods
# r.json().get('foods')[0] returns the first food in the list
# r.json().get('foods')[0].get('foodNutrients') returns the foodNutrients of the first food in the list


st.title('Results:')
st.write(f'Food Name: {results_name}')
st.button('Add to list')
st.write('Nutrient Results (filtered table):')
st.write(results_df)

# results = pd.DataFrame.query(selfexpr=search.lower(), )
# results = dv.get(search.lower())
# st.write(results)

# dict_foodname = []
# dict_nutrients = []
ingredients = {'foodname':[], 'nutrients':[]}

if st.button:
    ingredients['foodname'].append(results_name)
    ingredients['nutrients'].append(results_nutrients)
    # ingredient_new = {results_name: results_df}
    # ingredients = ingredients.append(ingredient_new)

st.write('My list:')
st.write('List of food names:')
st.write(ingredients['foodname'])
st.write('List of ingredients:')
st.write(ingredients['nutrients'])

# if st.button:
#     ingredients[search] = results
#     st.write(ingredients)

# pp(ingredients)
# next you want to present a button to store the search query (add to list)
#1 user presses the button (add to list)
#2 the search query is stored in a dictionary with the key being the search query and the value being the results { pumpkin: {results} }
#3 after storing you have a method that presents the stored search queries and displays a table (df) of all the ingredients and their nutritional values
#4 then you'll have a method to reference the stored daily values and compate the total nutritional values of the stored ingredients to the daily values
#5 then you'll have a method to display the results of the comparison