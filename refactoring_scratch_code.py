import os
import pandas as pd
import requests
import streamlit as st

from daily_values import daily_values as dv, dailyvalues_blank as dv_blank

DEMO_KEY = os.getenv('DEMO_KEY', "") # <-- change to 'search_key'
search_endpoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'

@st.cache_data
def add_daily_value_dicts(dict1: dict, dict2: dict): # <-- not used yet
    final_added_dict = {}
    for key in dict1:
        if key in dict2:
            final_added_dict[key] = {
                'value' : dict1[key]['value'] - dict2[key]['value'],
                'unit' : dict1[key]['unit']
            }    
    return(final_added_dict)

@st.cache_data
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

# @st.cache_data
# def create_mutable_ingredients_list():
#     mutable_ingredients_list = []
#     print('mutable ingredients list created')
#     return mutable_ingredients_list

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

@st.cache_data
def get_search_results_data(searchbar_input):
    results = requests.get(
        search_endpoint,
        params={"query" : searchbar_input, "api_key" : DEMO_KEY}
        )
    return(results)

@st.cache_data
def get_search_results_name(searchbar_input):
    results = get_search_results_data(searchbar_input)
    results_name = results.json().get('foods')[0].get('description')
    return(results_name)

@st.cache_data
def get_search_results_nutrients(searchbar_input):
    results = get_search_results_data(searchbar_input)
    results_nutrients = results.json().get('foods')[0].get('foodNutrients')
    return(results_nutrients)

def initialize_once(): # <-- alphabetize
    return {'initialized': False}

def perform_initialization(data: dict): # <-- alphabetize
    if not data['initialized']:
        print('Initializing once...')
        data['initialized'] = True

def print_list_as_bullets(list_name: list):
    mylist_bullets = ''
    for item in list_name:
        mylist_bullets += '- ' + item + '\n'
    st.markdown(mylist_bullets)

@st.cache_data
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

if __name__ == '__main__':

    st.set_page_config(layout='wide')

    initialized_data = initialize_once()
    # initialized_data['initialized'] currently == False
    # Put anything below that just needs to happen once.
    breakpoint()

    mutable_ingredients_list = []
    breakpoint()

    perform_initialization(initialized_data)
    breakpoint()

    if initialized_data['initialized']:

        # print('this prints just after the __main__ statement')

        # print('BEGINNING OF MAIN SECTION')

        # mutable_ingredients_list = [] # <-- was previously mylist_ingredients
        # print('Just after mutable_ingredients_list')
        # print(f'mutable_ingredients_list = {mutable_ingredients_list}')

        st.title('Nutrition Guide')

        (search_an_ingredient,
            my_ingredients_list,
            nutrients_i_have,
            nutrients_i_need) = st.columns((3, 2, 2, 2))

        with search_an_ingredient:
            st.header('Search an Ingredient')

            search = st.text_input(
                'Start by typing a food or ingredient below, and then press ENTER.'
            )

            if search:
                st.write(f'**Showing results for:** {get_search_results_name(search)}')
                
                # print('Just before add button')
                # print(f'mutable_ingredients_list = {mutable_ingredients_list}')
                button_add_to_list(
                    get_search_results_name(search),
                    mutable_ingredients_list
                )
                # print('Just after add button')
                # print(f'mutable_ingredients_list = {mutable_ingredients_list}')
                # print('Just before remove button')
                # print(f'mutable_ingredients_list = {mutable_ingredients_list}')
                button_remove_from_list(
                    get_search_results_name(search),
                    mutable_ingredients_list
                )
                # print('Just after remove button.')
                # print(f'mutable_ingredients_list = {mutable_ingredients_list}')
                draw_table_json_data(
                    get_search_results_nutrients(search)
                )
                
            else:
                #st.write() doesn't seem to be able to recognize '\n'?
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