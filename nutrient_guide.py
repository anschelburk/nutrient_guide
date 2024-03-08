import os
import pandas as pd
import requests
import streamlit as st

from recommended_daily_nutrients import recommended_daily_nutrients

st.set_page_config(layout='wide')

USDA_API_KEY = os.getenv('DEMO_KEY', "")
SEARCH_ENDPOINT = 'https://api.nal.usda.gov/fdc/v1/foods/search'

if not 'api_search_results_name' in st.session_state:
    st.session_state['api_search_results_name'] = ''
if not 'api_search_results_nutrients' in st.session_state:
    st.session_state['api_search_results_nutrients'] = []
if not 'my_ingredients_list' in st.session_state:
    st.session_state['my_ingredients_list'] = []
if not 'mylist_nutrients' in st.session_state:
    st.session_state['mylist_nutrients'] = {}
if not 'nutrients_i_have_dict' in st.session_state:
    st.session_state['nutrients_i_have_dict'] = {
            key: {
                'value': 0, 'unit': value['unit']
                } for key, value in recommended_daily_nutrients.items()
        }
if not 'nutrients_i_need_dict' in st.session_state:
    st.session_state['nutrients_i_need_dict'] = recommended_daily_nutrients
if not 'cached_ingredient_names_and_nutrients' in st.session_state:
    st.session_state['cached_ingredient_names_and_nutrients'] = {}
# if not 'results_name' in st.session_state:
#     st.session_state['results_name'] = ''
# if not 'results_nutrients' in st.session_state:
#     st.session_state['results_nutrients'] = []

def button_add_to_list(
        cached_ingredients_dict: dict,
        api_ingredient_name: str,
        api_ingredient_nutrients,
        current_nutrients_i_have_data: dict,
        current_nutrients_i_need_data: dict
    ):
    st_button = st.button('Add Ingredient to My List')
    if st_button:
        if not api_ingredient_name in cached_ingredients_dict.keys():
            api_ingredient_nutrients = format_json_data_as_dict(
                    api_ingredient_nutrients
                )
            cached_ingredients_dict[api_ingredient_name] = api_ingredient_nutrients
            merge_dicts_add(
                    current_nutrients_i_have_data,
                    cached_ingredients_dict[api_ingredient_name]
                )
            merge_dicts_subtract(
                    current_nutrients_i_need_data,
                    cached_ingredients_dict[api_ingredient_name]
                )
        else:
            pass

def button_remove_from_list(
        cached_ingredients_dict: dict,
        api_ingredient_name: str,
        current_nutrients_i_have_data: dict,
        current_nutrients_i_need_data: dict
    ):
    st_button = st.button('Add Ingredient to My List')
    if st_button:
        if api_ingredient_name in cached_ingredients_dict.keys():
            merge_dicts_add(
                    current_nutrients_i_need_data,
                    cached_ingredients_dict[api_ingredient_name]
                )
            merge_dicts_subtract(
                    current_nutrients_i_have_data,
                    cached_ingredients_dict[api_ingredient_name]
                )
            del cached_ingredients_dict[api_ingredient_name]
        else:
            pass

def draw_table_daily_values(data_source: dict):
    st.write(
        pd.DataFrame
            .from_dict(data_source, orient='index')
            .rename(columns={'value': 'Amount', 'unit': 'Units'})
        )

def format_json_data_as_dict(json_data_to_format):
    """
    Creates and then returns a new dict, formatted_json_data, that contains
    only the needed values from the json data retrieved by the API search,
    and is formatted to match the nutrients_i_have and nutrients_i_need dicts.
    """
    formatted_json_data = {
        key['nutrientName']: {
            'value': key['value'], 'unit': key['unitName']
            } for key in json_data_to_format
    }
    return formatted_json_data

def _normalize_nutrient_names(current_nutrients: dict, new_nutrients: dict):
    current_nutrients = {
        key.split(', ')[0]: value for key, value in current_nutrients.items()
    }
    new_nutrients = {
        key.split(', ')[0]: value for key, value in new_nutrients.items()
    }
    return current_nutrients, new_nutrients

def merge_dicts_add(current_nutrients: dict, new_nutrients: dict):
    """
    Adds the values of new_nutrients to current_nutrients. Returns a modified
    version of current_nutrients.
    """
    current_nutrients, new_nutrients = _normalize_nutrient_names(
        current_nutrients, new_nutrients
    )

    for key in new_nutrients:
        if key in current_nutrients.keys():
            current_nutrients[key]['value'] += new_nutrients[key]['value']
        else:
            current_nutrients[key] = new_nutrients[key]
    return current_nutrients

def merge_dicts_subtract(current_nutrients: dict, new_nutrients: dict):
    """
    Subtracts the values of new_nutrients from current_nutrients. Returns a modified
    version of current_nutrients.
    """
    for key in new_nutrients:
        stripped_key = key.split(',')[0]
        if key in current_nutrients.keys():
            current_nutrients[key]['value'] -= new_nutrients[key]['value']
        else:
            if ',' in key:
                if stripped_key in current_nutrients.keys():
                    current_nutrients[stripped_key]['value'] -= new_nutrients[key]['value']
                else:
                    current_nutrients[key] = new_nutrients[key]
            else:
                current_nutrients[key] = new_nutrients[key]
    return current_nutrients

def print_my_nutrients_list_with_dropdown_lists(list_of_my_nutrients: list):
    for item in list_of_my_nutrients:
        st.write(item)
        st.selectbox(
            'Please select how many of this food item you would like:',
            list(range(0, 11)),
            index = 1,
            key = item
        )
        st.write('\n')

def retrieve_api_search_data(
        searchbar_input: str,
        api_search_endpoint,
        api_search_key
):
    api_search_result = requests.get(
        api_search_endpoint,
        params={"query": searchbar_input, "api_key": api_search_key}
    ).json().get('foods')[0]
    updated_results_name = api_search_result.get('description')
    updated_results_nutrients = api_search_result.get('foodNutrients')
    return(updated_results_name, updated_results_nutrients)

def update_nutrients_cache_with_api_search_results(
        searchbar_input: str,
        nutrients_cache_to_update: dict,
        api_search_endpoint,
        api_search_key
):
    api_search_result = requests.get(
            api_search_endpoint,
            params={"query": searchbar_input, "api_key": api_search_key}
        ).json().get('foods')[0]
    ingredient_name_from_api_search = api_search_result.get('description')
    nutrients_from_api_search = api_search_result.get('foodNutrients')
    nutrients_cache_to_update[
            ingredient_name_from_api_search
        ] = nutrients_from_api_search

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
            (st.session_state['api_search_results_name'],
             st.session_state['api_search_results_nutrients']) = retrieve_api_search_data(
                searchbar_input = st.session_state['search'],
                api_search_endpoint = SEARCH_ENDPOINT,
                api_search_key = USDA_API_KEY
            )
            st.write('Showing results for:', st.session_state['api_search_results_name'])
            button_add_to_list(
                    cached_ingredients_dict = st.session_state[
                        'cached_ingredient_names_and_nutrients'],
                    api_ingredient_name = st.session_state[
                        'api_search_results_name'],
                    api_ingredient_nutrients = st.session_state[
                        'api_search_results_nutrients'],
                    current_nutrients_i_have_data = st.session_state[
                        'nutrients_i_have_dict'],
                    current_nutrients_i_need_data = st.session_state[
                        'nutrients_i_need_dict']
                )
            button_remove_from_list(
                    cached_ingredients_dict = st.session_state[
                        'cached_ingredient_names_and_nutrients'],
                    api_ingredient_name = st.session_state[
                        'api_search_results_name'],
                    current_nutrients_i_have_data = st.session_state[
                        'nutrients_i_have_dict'],
                    current_nutrients_i_need_data = st.session_state[
                        'nutrients_i_need_dict']
                )
            draw_table_daily_values(
                format_json_data_as_dict(
                    st.session_state['api_search_results_nutrients']
                )
            )

        else:
            st.write(f'No results yet. Need help getting started? Try searching **sweet potato**.')

    with my_ingredients_list:
        st.subheader('My Ingredients List')
        print_my_nutrients_list_with_dropdown_lists(
            st.session_state['cached_ingredient_names_and_nutrients'].keys()
        )

    with nutrients_i_have:
        st.subheader('Nutrients I Have')
        draw_table_daily_values(st.session_state['nutrients_i_have_dict'])

    with nutrients_i_need:
        st.subheader('Nutrients I Need')
        draw_table_daily_values(
            st.session_state['nutrients_i_need_dict']
        )
