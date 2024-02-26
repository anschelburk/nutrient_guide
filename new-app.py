import streamlit as st
# import numpy as np
import pandas as pd
import os
from daily_values import daily_values as dv
import requests
from pprint import pprint as pp

st.set_page_config(layout="wide")

st.title('Nutrition Guide')

ingredients_search, ingredients_list, nutrients_have, nutrients_need = st.columns((3, 2, 2, 2))

# map_data = pd.DataFrame(
#     np.random.randn(1000,2) / [50,50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)

ingredients_search.header('Search an Ingredient')

search_endpoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'
DEMO_KEY = os.getenv('DEMO_KEY', "")
search = ingredients_search.text_input('To search an ingredient, type it below and press ENTER.')

# ingredients_search.write(f'You searched: {search}')

r = requests.get(search_endpoint, params={"query": search, "api_key":DEMO_KEY}) # using the requests library to make a GET request to the API
results_name = r.json().get('foods')[0].get('description')
# results_name = 'Name-goes-here'
results_nutrients = r.json().get('foods')[0].get('foodNutrients') # getting the JSON object of the response and navigating to the foodNutrients key
results_df = pd.DataFrame(data=results_nutrients, columns=['nutrientName', 'value', 'unitName'])
results_df = results_df.rename(columns={'nutrientName': 'Nutrient Name', 'value': 'Amount', 'unitName': 'Units'})
results_df.index = range(1, len(results_df)+1)
# results_df.set_index('Nutrient Name', inplace=True)

# results_df = results_df.drop(columns=1)

# further explanation of the code:
# r.json() returns a JSON object of the response
# r.json().get('foods') returns a list of foods
# r.json().get('foods')[0] returns the first food in the list
# r.json().get('foods')[0].get('foodNutrients') returns the foodNutrients of the first food in the list


ingredients_search.subheader(f'Showing results for: {results_name}')
button_addtolist = ingredients_search.button('Add to My Ingredients List')
ingredients_search.write(results_df)

# results = pd.DataFrame.query(selfexpr=search.lower(), )
# results = dv.get(search.lower())
# st.write(results)

# dict_foodname = []
# dict_nutrients = []
ingredients = {'foodname':[], 'nutrients':[]}

if button_addtolist:
    ingredients['foodname'].append(results_name)
    ingredients['nutrients'].append(results_nutrients)
    # ingredient_new = {results_name: results_df}
    # ingredients = ingredients.append(ingredient_new)



ingredients_list.subheader('My Ingredients List:')
ingredients_list.write('List of food names:')
ingredients_list.write(ingredients['foodname'])
ingredients_list.write('List of ingredients:')
ingredients_list.write(ingredients['nutrients'])

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

with nutrients_have:
    st.subheader('Nutrients I Have:')
    st.write('Still building this:')
    st.write(
        pd.DataFrame(
            data=(
                [1, 2, 3, 4, 5],
                ['a', 'b', 'c', 'd', 'e'],
                [0, 0, 0, 0, 0]
            )
        )
    )

with nutrients_need:
    st.subheader('Nutrients I Still Need:')
    st.write('% Daily Values:')
    st.write(
        pd.DataFrame
            .from_dict(dv, orient='index')
            .rename(columns={'value': 'Amount', 'unit': 'Units'})
        )