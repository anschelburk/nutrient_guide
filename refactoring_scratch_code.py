import os
import pandas as pd
import requests
import streamlit as st

from daily_values import daily_values as dv, dailyvalues_blank as dv_blank
    
st.set_page_config(layout='wide')

st.session_state['DEMO_KEY'] = os.getenv('DEMO_KEY', "") # <-- change to 'search_key'
st.session_state['search_endpoint'] = 'https://api.nal.usda.gov/fdc/v1/foods/search'
st.session_state['dailyvalues_full'] = dv
st.session_state['dailyvalues_blank'] = dv_blank

if not 'mylist_ingredients' in st.session_state:
    st.session_state['mylist_ingredients'] = []
if not 'mylist_nutrients' in st.session_state:
    st.session_state['mylist_nutrients'] = {}
if not 'nutrients_i_have_dict' in st.session_state:
    st.session_state['nutrients_i_have_dict'] = st.session_state['dailyvalues_blank']
if not 'nutrients_i_need_dict' in st.session_state:
    st.session_state['nutrients_i_need_dict'] = st.session_state['dailyvalues_full']
if not 'results_name' in st.session_state:
    st.session_state['results_name'] = ''
if not 'results_nutrients' in st.session_state:
    st.session_state['results_nutrients'] = ''

def button_add_to_list(
        results_name = st.session_state['results_name'],
        mylist_ingredients = st.session_state['mylist_ingredients']
):
    st_button = st.button('Add Ingredient to My List')
    if st_button:
        mylist_ingredients.append(results_name)
        merge_dicts_add(
            st.session_state['nutrients_i_have_dict'],
            format_json_data_as_dict(
                st.session_state['results_nutrients']
            )
        )

def button_remove_from_list(
        results_name = st.session_state['results_name'],
        mylist_ingredients = st.session_state['mylist_ingredients']
):
    st_button = st.button('Remove Ingredient from My List')
    if st_button:
        mylist_ingredients.remove(results_name)
        merge_dicts_subtract(
            st.session_state['nutrients_i_need_dict'],
            format_json_data_as_dict(
                st.session_state['results_nutrients']
            )
        )

def draw_table_daily_values(data_source: dict):
    st.write(
        pd.DataFrame
            .from_dict(data_source, orient='index')
            .rename(columns={'value': 'Amount', 'unit': 'Units'})
        )

def format_daily_values_dict(dailyvalues_dict: dict):
    st.session_state['formatted_daily_values_dict'] = {key: {"nutrient": value} for key, value in dailyvalues_dict.items()}

def format_json_data_as_dict(data):
    """
    Formats json data retrieved from API by returning new dict from the json
    data that matches the format of the dicts imported from daily_values.py
    """
    json_data_formatted = {}
    for item in data:
        nutrient_name_json = item['nutrientName']
        nutrient_amount_json = item['value']
        nutrient_unit_json = item['unitName']
        json_data_formatted[nutrient_name_json] = {
            'value': nutrient_amount_json,
            'unit': nutrient_unit_json
        }
    return(json_data_formatted)

def get_search_results_data(searchbar_input):
        return(requests.get(
            st.session_state['search_endpoint'],
            params={"query": searchbar_input, "api_key": st.session_state['DEMO_KEY']}
        ))

def merge_dicts_add(current_nutrients: dict, new_nutrients: dict): # <-- Not used yet
    """
    Adds the values of new_nutrients to current_nutrients. Returns a modified
    version of my_current_nutrients.
    """
    for key in new_nutrients:
        if key in current_nutrients.keys():
            current_nutrients[key]['value'] += new_nutrients[key]['value']
        else:
            current_nutrients[key] = new_nutrients[key]    
    return(current_nutrients)

def merge_dicts_subtract(dict1: dict, dict2: dict): # <-- Not used yet
    """
    Subtracts the values of dict2 from dict1. dict2.values() --> dict1.values().
    Returns a modified version of dict1.
    """
    final_added_dict = {}
    for key in dict2.keys():
        if key in dict1:
            dict1[key]['value'] -= dict2[key]['value']
        else:
            dict1[key] = dict2[key]    
    return(final_added_dict)

def print_list_as_bullets(list_name: list):
    mylist_bullets = ''
    for item in list_name:
        mylist_bullets += '- ' + item + '\n'
    st.markdown(mylist_bullets)

def subtract_daily_value_dicts(dict1: dict, dict2: dict):
    final_subtracted_dict = {}
    for key in dict1:
        if key in dict2:
            final_subtracted_dict[key] = {
                'value' : dict1[key]['value'] - dict2[key]['value'],
                'unit' : dict1[key]['unit']
            }    
    return(final_subtracted_dict)

def update_search_results_name(searchbar_input):
    st.session_state['results_name'] = get_search_results_data(searchbar_input).json().get('foods')[0].get('description')

def update_search_results_nutrients(searchbar_input):
    st.session_state['results_nutrients'] = get_search_results_data(searchbar_input).json().get('foods')[0].get('foodNutrients')

if __name__ == '__main__':

    st.title('Nutrient Guide')

    (search_an_ingredient,
        my_ingredients_list,
        nutrients_i_have,
        nutrients_i_need) = st.columns((3, 2, 2, 2))

    with search_an_ingredient:
        st.header('Search an Ingredient')
        st.session_state['search'] = st.text_input(
            'Start by typing a food or ingredient below, and then press ENTER.'
        )
        if st.session_state['search']:
            update_search_results_name(st.session_state['search'])
            update_search_results_nutrients(st.session_state['search'])
            st.write('Showing results for:', st.session_state['results_name'])
            button_add_to_list()
            button_remove_from_list()
            draw_table_daily_values(
                format_json_data_as_dict(
                    st.session_state['results_nutrients']
                )
            )

        else:
            st.write(f'No results yet. Need help getting started? Try searching **sweet potato**.')

    with my_ingredients_list:
        st.subheader('My Ingredients List')
        print_list_as_bullets(st.session_state['mylist_ingredients'])

    with nutrients_i_have:
        st.subheader('Nutrients I Have')
        draw_table_daily_values(st.session_state['nutrients_i_have_dict'])

    with nutrients_i_need:
        st.subheader('Nutrients I Need')
        draw_table_daily_values(
            st.session_state['nutrients_i_need_dict']
        )