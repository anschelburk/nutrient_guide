import os
import pandas as pd
import requests
import streamlit as st

from daily_values import daily_values as dv, dailyvalues_blank as dv_blank

def add_daily_value_dicts(dict1: dict, dict2: dict): # <-- not used yet
    final_added_dict = {}
    for key in dict1:
        if key in dict2:
            final_added_dict[key] = {
                'value' : dict1[key]['value'] - dict2[key]['value'],
                'unit' : dict1[key]['unit']
            }    
    return(final_added_dict)

def add_item_to_list(item_name, list_name: list):
    return(list_name.append(item_name))

def button_add_to_list(item_name, list_name):
    st_button_add_to_list = st.button('Add Ingredient to My List')
    if st_button_add_to_list:
        add_item_to_list(item_name, list_name)
    
def button_remove_from_list(item_name, list_name):
    st_button_remove_from_list = st.button('Remove Ingredient from My List')
    if st_button_remove_from_list:
        remove_item_from_list(item_name, list_name)

def draw_table_daily_values(data_source: dict):
    st.write(
        pd.DataFrame
            .from_dict(data_source, orient='index')
            .rename(columns={'value': 'Amount', 'unit': 'Units'})
        )

def draw_table_json_data(data_source):
    results_df = pd.DataFrame(
        data=data_source,
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
    st.write(results_df)

def print_list_as_bullets(list_name: list):
    mylist_bullets = ''
    for item in list_name:
        mylist_bullets += '- ' + item + '\n'
    st.markdown(mylist_bullets)

def remove_item_from_list(item_name, list_name: list):
    return(list_name.remove(item_name))

def subtract_daily_value_dicts(dict1: dict, dict2: dict):
    final_subtracted_dict = {}
    for key in dict1:
        if key in dict2:
            final_subtracted_dict[key] = {
                'value' : dict1[key]['value'] - dict2[key]['value'],
                'unit' : dict1[key]['unit']
            }    
    return(final_subtracted_dict)

DEMO_KEY = os.getenv('DEMO_KEY', "") # <-- change to 'search_key'
search_endpoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'

if __name__ == '__main__':

    print('BEGINNING OF MAIN SECTION')

    mutable_ingredients_list = [] # <-- was previously mylist_ingredients
    print('Just after mutable_ingredients_list')
    print(f'mutable_ingredients_list = {mutable_ingredients_list}')

    st.set_page_config(layout='wide')

    st.title('Nutrition Guide')

    (search_an_ingredient,
     my_ingredients_list,
     nutrients_i_have,
     nutrients_i_need) = st.columns((3, 2, 2, 2))
    
    with search_an_ingredient:
        st.header('Search an Ingredient')

        search = st.text_input(
            'Start by typing an ingredient below, and pressing ENTER.'
        )

        results = requests.get(
            search_endpoint,
            params={"query" : search, "api_key" : DEMO_KEY}
            )
    
        if search:
            results_name = results.json().get('foods')[0].get('description')
            results_nutrients = results.json().get('foods')[0].get('foodNutrients')
            st.write(f'**Showing results for:** {results_name}')
            
            print('Just before add button')
            print(f'mutable_ingredients_list = {mutable_ingredients_list}')
            button_add_to_list(results_name, mutable_ingredients_list)
            print('Just after add button')
            print(f'mutable_ingredients_list = {mutable_ingredients_list}')
            print('Just before remove button')
            print(f'mutable_ingredients_list = {mutable_ingredients_list}')
            button_remove_from_list(results_name, mutable_ingredients_list)
            print('Just after remove button.')
            print(f'mutable_ingredients_list = {mutable_ingredients_list}')
            draw_table_json_data(results_nutrients)
            
        else:
            st.write(f'No results yet. Need help getting started? Try searching **sweet potato**.')

    with my_ingredients_list:
        st.subheader('My Ingredients List')
        print_list_as_bullets(mutable_ingredients_list)
    
    with nutrients_i_have:
        st.subheader('Nutrients I Have')
        nutrients_i_have_dict = dv_blank
        draw_table_daily_values(nutrients_i_have_dict)
    
    with nutrients_i_need:
        st.subheader('Nutrients I Need')
        nutrients_i_need_dict = subtract_daily_value_dicts(
            dv, nutrients_i_have_dict
            )
        draw_table_daily_values(nutrients_i_need_dict)