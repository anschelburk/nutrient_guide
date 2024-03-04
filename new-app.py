import streamlit as st
# import numpy as np
import pandas as pd
import os
from daily_values import daily_values as dv, dailyvalues_blank as dvb
import requests
from pprint import pprint as pp

st.set_page_config(layout="wide")
st.title('Nutrition Guide')
ingredients_search, ingredients_list, nutrients_have, nutrients_need = st.columns((3, 2, 2, 2))

# map_data = pd.DataFrame(
#     np.random.randn(1000,2) / [50,50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

search_endpoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'
DEMO_KEY = os.getenv('DEMO_KEY', "")
mylist_ingredients = []

with ingredients_search:
    st.header('Search an Ingredient')
    search = st.text_input(
        'To search an ingredient, type it below and press ENTER.'
        )

# ingredients_search.write(f'You searched: {search}')

results = requests.get(
    search_endpoint,
    params={"query" : search, "api_key" : DEMO_KEY}
    ) # using the requests library to make a GET request to the API
if results:
    results_name = results.json().get('foods')[0].get('description')
    # results_name = 'Name-goes-here'
    results_nutrients = results.json().get('foods')[0].get('foodNutrients')
        # getting the JSON object of the response and navigating to the foodNutrients key
    results_df = pd.DataFrame(
        data=results_nutrients,
        columns=['nutrientName', 'value', 'unitName']
        )
    results_df = results_df.rename(
        columns={
            'nutrientName': 'Nutrient Name',
            'value': 'Amount',
            'unitName': 'Units'
            }
        )
    results_df.index = range(1, len(results_df)+1)

if search == '':
    results_name = ''
# results_df.set_index('Nutrient Name', inplace=True)

# results_df = results_df.drop(columns=1)

# further explanation of the code:
# results.json() returns a JSON object of the response
# results.json().get('foods') returns a list of foods
# results.json().get('foods')[0] returns the first food in the list
# results.json().get('foods')[0].get('foodNutrients') returns the foodNutrients of the first food in the list

### BUTTON FUNCTIONS

def button_remove():
    print("Button Remove was clicked.")


def button_addtolist(results_name):
    print("Button Add to List was clicked.")
    mylist_ingredients.append(results_name)
    results_nutrients = results.json().get('foods')[0].get('foodNutrients')
    # if a key is in the nutrients_i_have dictionary, add the value to the existing value
    # if a key is not in the nutrients_i_have dictionary, add the key and value to the dictionary
    if not nutrients_i_have:
        nutrients_i_have = {}
    for nutrient in results_nutrients:
        if nutrient['nutrientName'] in nutrients_i_have:
            nutrients_i_have[nutrient['nutrientName']]['value'] += nutrient['value']
        else:
            nutrients_i_have[nutrient['nutrientName']] = {
                'value' : nutrient['value'],
                'unit' : nutrient['unitName']
            }
            
    # mylist_ingredients.append(results_name)
    # ingredients['foodname'].append(results_name)
    # ingredients['nutrients'].append(results_nutrients


with ingredients_search:
    if results_name:
        st.subheader(f'Showing results for: {results_name}')
        button_addtolist = st.button('Add to My Ingredients List', on_click=button_addtolist(results_name))
        _button_remove = st.button('Remove from My Ingredients List', on_click=button_remove())
        st.write(results_df)
        ingredients_filtered = {}
        # for key in results_nutrients:
        #     ingredients_filtered[results_nutrients][key]['nutrientName'] = {
        #         'value' : results_nutrients[key]['value'],
        #         'unit' : results_nutrients[key]['unitName']
        #     }
        # for key in results_nutrients:
        #     ingredients_filtered.update(
        #         results_nutrients[key]['nutrientName'] : {
        #                 'value' : results_nutrients[key]['value'],
        #                 'unit' : results_nutrients[key]['unitName']
        #          }
        #     )

        if results_nutrients:
            st.write(results_nutrients[0]['nutrientName'])
            st.write(results_nutrients)
            # ingredients_dict = {
            #     results_nutrients['nutrientName'] : {
            #         'value' : results_nutrients['value'],
            #         'unit' : results_nutrients['unitName']
            #     }
            # }

# st.map(map_data)
# print(button_remove)

print("Hello, my name is Anschel")

def no_access():
    print("You have no access to this function")

# ingredients_search.subheader(f'Showing results for: {results_name}')
# button_addtolist = ingredients_search.button('Add to My Ingredients List')
# button_remove = ingredients_search.button('Remove from My Ingredients List')
# ingredients_search.write(results_df)

# results = pd.DataFrame.query(selfexpr=search.lower(), )
# results = dv.get(search.lower())
# st.write(results)

# dict_foodname = []
# dict_nutrients = []
# ingredients = {'foodname':[], 'nutrients':[]}


# if button_addtolist:
#     mylist_ingredients.append(results_name)
#     breakpoint()
    # ingredients['nutrients'].append(results_nutrients)
    # ingredient_new = {results_name: results_df}
    # ingredients = ingredients.append(ingredient_new)
# if button_remove:
    # mylist_ingredients.remove(results_name)

with ingredients_list:
    st.subheader('My Ingredients List:')
    mylist_bullets = ''
    for i in st.session_state.mylist_ingredients:
        mylist_bullets += '- ' + i + '\n'
    st.markdown(mylist_bullets)

# if st.button: 
    #
    #
#     ingredients[search] = results
#     st.write(ingredients)

# pp(ingredients)
# next you want to present a button to store the search query (add to list)
#1 user presses the button (add to list)
#2 the search query is stored in a dictionary with the key being the search query and the value being the results { pumpkin: {results} }
#3 after storing you have a method that presents the stored search queries and displays a table (df) of all the ingredients and their nutritional values
#4 then you'll have a method to reference the stored daily values and compate the total nutritional values of the stored ingredients to the daily values
#5 then you'll have a method to display the results of the comparison

# def create_table_labels():

def create_nutrients_i_have_table():
    st.subheader('Nutrients I Have:')
    mylist_have = dvb
    # for key in mylist_have:
    #     mylist_have[key]['value'] = 3
    st.write(
        pd.DataFrame
            .from_dict(mylist_have, orient='index')
            .rename(columns={'value': 'Amount', 'unit': 'Units'})
        )
    # return mylist_have

def create_nutrients_i_need_table(mylist_have):
    st.subheader('Nutrients I Need:')
    mylist_need = {}
    for key in dv:
        if key in mylist_have:
            mylist_need[key] = {
                'value' : dv[key]['value'] - mylist_have[key]['value'],
                'unit' : dv[key]['unit']
                }
    st.write(
        pd.DataFrame
            .from_dict(mylist_need, orient='index')
            .rename(columns={'value': 'Amount', 'unit': 'Units'})
        )
    
if __name__ == '__main__':
    print("first run")
    nutrients_i_have = {}
    # create_table_labels()
    create_nutrients_i_have_table()
    create_nutrients_i_need_table(mylist_have=dvb)