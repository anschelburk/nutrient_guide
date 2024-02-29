import streamlit as st
# import numpy as np
import pandas as pd
import os
from daily_values import daily_values as dv, dailyvalues_blank as dvb
import requests
from pprint import pprint as pp

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('nutrition.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS DailyValues (
    Nutrient TEXT,
    Value REAL,
    Unit TEXT
)
''')

# Data to insert
data = [
    ('added sugars', 50, 'g'),
    ('biotin', 30, 'mcg'),
    ('calcium', 1300, 'mg'),
    ('chloride', 2300, 'mg'),
    ('choline', 550, 'mg'),
    ('cholesterol', 300, 'mg'),
    ('chromium', 35, 'mcg'),
    ('copper', 0.9, 'mg'),
    ('dietary fiber', 28, 'g'),
    ('fat', 78, 'g'),
    ('folate/folic acid', 400, 'mcg DFE'),
    ('iodine', 150, 'mcg'),
    ('iron', 18, 'mg'),
    ('magnesium', 420, 'mg'),
    ('manganese', 2.3, 'mg'),
    ('molybdenum', 45, 'mcg'),
    ('niacin', 16, 'mg NE'),
    ('pantothenic acid', 5, 'mg'),
    ('phosphorus', 1250, 'mg'),
    ('potassium', 4700, 'mg'),
    ('protein', 50, 'g'),
    ('riboflavin', 1.3, 'mg'),
    ('saturated fat', 20, 'g'),
    ('selenium', 55, 'mcg'),
    ('sodium', 2300, 'mg'),
    ('thiamin', 1.2, 'mg'),
    ('total carbohydrate', 275, 'g'),
    ('vitamin a', 900, 'mcg RAE'),
    ('vitamin b6', 1.7, 'mg'),
    ('vitamin b12', 2.4, 'mcg'),
    ('vitamin c', 90, 'mg'),
    ('vitamin d', 20, 'mcg'),
    ('vitamin e', 15, 'mg alpha-tocopherol'),
    ('vitamin k', 120, 'mcg'),
    ('zinc', 11, 'mg')
]

# Insert the data
c.executemany('INSERT INTO DailyValues (Nutrient, Value, Unit) VALUES (?, ?, ?)', data)

# Commit the changes and close the connection
conn.commit()
conn.close()

# query the database and display the results in a dataframe
conn = sqlite3.connect('nutrition.db')
c = conn.cursor()
c.execute('SELECT * FROM DailyValues')
data = c.fetchall()
st.write(pd.DataFrame(data, columns=['Nutrient', 'Value', 'Unit']))
# conn.close()

# st.write(pd.DataFrame(data, columns=['Nutrient', 'Value', 'Unit']))


# Create the SQL connection to pets_db as specified in your secrets file.
# conn = st.connection('nutrition_db', type='sql')
# conn = sqlite3.connect('data_db')

# daily_values = {
#     "Added sugars": {"value": 50, "unit": "g"},
#     "Biotin": {"value": 30, "unit": "mcg"},
#     "Calcium": {"value": 1300, "unit": "mg"},
#     "Chloride": {"value": 2300, "unit": "mg"},
#     "Choline": {"value": 550, "unit": "mg"},
#     "Cholesterol": {"value": 300, "unit": "mg"},
#     "Chromium": {"value": 35, "unit": "mcg"},
#     "Copper": {"value": 0.9, "unit": "mg"},
#     "Dietary Fiber": {"value": 28, "unit": "g"},
#     "Fat": {"value": 78, "unit": "g"},
#     "Folate/Folic Acid": {"value": 400, "unit": "mcg DFE"},
#     "Iodine": {"value": 150, "unit": "mcg"},
#     "Iron": {"value": 18, "unit": "mg"},
#     "Magnesium": {"value": 420, "unit": "mg"},
#     "Manganese": {"value": 2.3, "unit": "mg"},
#     "Molybdenum": {"value": 45, "unit": "mcg"},
#     "Niacin": {"value": 16, "unit": "mg NE"},
#     "Pantothenic Acid": {"value": 5, "unit": "mg"},
#     "Phosphorus": {"value": 1250, "unit": "mg"},
#     "Potassium": {"value": 4700, "unit": "mg"},
#     "Protein": {"value": 50, "unit": "g"},
#     "Riboflavin": {"value": 1.3, "unit": "mg"},
#     "Saturated fat": {"value": 20, "unit": "g"},
#     "Selenium": {"value": 55, "unit": "mcg"},
#     "Sodium": {"value": 2300, "unit": "mg"},
#     "Thiamin": {"value": 1.2, "unit": "mg"},
#     "Total carbohydrate": {"value": 275, "unit": "g"},
#     "Vitamin A": {"value": 900, "unit": "mcg RAE"},
#     "Vitamin B6": {"value": 1.7, "unit": "mg"},
#     "Vitamin B12": {"value": 2.4, "unit": "mcg"},
#     "Vitamin C": {"value": 90, "unit": "mg"},
#     "Vitamin D": {"value": 20, "unit": "mcg"},
#     "Vitamin E": {"value": 15, "unit": "mg alpha-tocopherol"},
#     "Vitamin K": {"value": 120, "unit": "mcg"},
#     "Zinc": {"value": 11, "unit": "mg"}
# }

# # Insert some data with conn.session.
# with conn.session as s:
#     # s.execute('CREATE TABLE IF NOT EXISTS stored_nutrients (name TEXT, nutrients TEXT);')
#     # s.execute('DELETE FROM pet_owners;')
#     # pet_owners = {'jerry': 'fish', 'barbara': 'cat', 'alex': 'puppy'}
#     # for k in pet_owners:
#     #     s.execute(
#     #         'INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);',
#     #         params=dict(owner=k, pet=pet_owners[k])
#     #     )
#     # write a execute statement to insert a field for each of the daily values in the daily_values dictionary
#     s.execute('CREATE TABLE IF NOT EXISTS stored_nutrients (name TEXT, nutrients TEXT);')
#     s.execute('DELETE FROM stored_nutrients;')
#     for k in daily_values:
#         s.execute(
#             'INSERT INTO stored_nutrients (name, nutrients) VALUES (:name, :nutrients);',
#             params=dict(name=k, nutrients=daily_values[k])
#         )
#     s.commit()

# # Query and display the data you inserted
data_db = conn.query("select * from DailyValues")
st.dataframe(data_db)

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
    for i in mylist_ingredients:
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