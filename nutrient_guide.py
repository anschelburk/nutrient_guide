import os
import pandas as pd
import requests
import streamlit as st

from decouple import config
from enum import Enum
from recommended_daily_nutrients import recommended_daily_nutrients

st.set_page_config(layout='wide')

class ModifyDictsAction(Enum):
    ADD = 1
    SUBTRACT = 2

USDA_API_KEY = config('API_KEY')
# USDA_API_KEY = os.getenv('API_KEY', "")
# api_search_key = USDA_API_KEY
SEARCH_ENDPOINT = 'https://api.nal.usda.gov/fdc/v1/foods/search'

# Designed to revert to blank list on each refresh
# initial_ingredients_list = []

if not 'api_search_results_name' in st.session_state:
    st.session_state['api_search_results_name'] = ''
if not 'api_search_results_nutrients' in st.session_state:
    st.session_state['api_search_results_nutrients'] = []
if not 'cached_ingredient_names_and_nutrients' in st.session_state:
    st.session_state['cached_ingredient_names_and_nutrients'] = {}
if not 'dict_items_to_delete' in st.session_state:
    st.session_state['dict_items_to_delete'] = []
if not 'nutrients_i_have_dict' in st.session_state:
    st.session_state['nutrients_i_have_dict'] = {
            key: {
                'value': 0, 'unit': value['unit']
                } for key, value in recommended_daily_nutrients.items()
        }
if not 'nutrients_i_need_dict' in st.session_state:
    st.session_state['nutrients_i_need_dict'] = dict(recommended_daily_nutrients)

def button_add_to_list(
        cached_ingredients_dict: dict,
        api_ingredient_name: str,
        api_ingredient_nutrients,
        current_nutrients_i_have_data: dict,
        current_nutrients_i_need_data: dict
    ):
    st_button = st.button('Add Ingredient to My List')
    default_ingredient_quantity = 1
    if st_button:
        if not api_ingredient_name in cached_ingredients_dict.keys():
            api_ingredient_nutrients = format_json_data_as_dict(
                    api_ingredient_nutrients)
            cached_ingredients_dict[api_ingredient_name] = {
                'quantity': default_ingredient_quantity,
                'nutrients': api_ingredient_nutrients}
            modify_dicts(

                current_nutrients = current_nutrients_i_have_data,
                new_nutrients = cached_ingredients_dict[
                    api_ingredient_name]['nutrients'],
                ingredient_quantity = default_ingredient_quantity,
                action_to_take = ModifyDictsAction.ADD)
            modify_dicts(
                current_nutrients_i_need_data,
                cached_ingredients_dict[api_ingredient_name]['nutrients'],
                ingredient_quantity = default_ingredient_quantity,
                action_to_take = ModifyDictsAction.SUBTRACT)

def button_remove_from_list(
        cached_ingredients_dict: dict,
        api_ingredient_name: str,
        current_nutrients_i_have_data: dict,
        current_nutrients_i_need_data: dict):
    st.session_state[f'remove_button_{api_ingredient_name}'] = st.button('Remove Ingredient from My List')
    if st.session_state[f'remove_button_{api_ingredient_name}']:
        cached_ingredient_quantity = cached_ingredients_dict[
            api_ingredient_name]['quantity']
        if api_ingredient_name in cached_ingredients_dict.keys():
            modify_dicts(
                current_nutrients = current_nutrients_i_need_data,
                new_nutrients = cached_ingredients_dict[
                    api_ingredient_name]['nutrients'],
                ingredient_quantity = cached_ingredient_quantity,
                action_to_take = ModifyDictsAction.ADD)
            modify_dicts(
                current_nutrients = current_nutrients_i_have_data,
                new_nutrients = cached_ingredients_dict[
                    api_ingredient_name]['nutrients'],
                ingredient_quantity = cached_ingredient_quantity,
                action_to_take = ModifyDictsAction.SUBTRACT)
            del cached_ingredients_dict[api_ingredient_name]

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

def modify_dicts(current_nutrients: dict,
                 new_nutrients: dict,
                 ingredient_quantity: int,
                 action_to_take: ModifyDictsAction):
    current_nutrients, new_nutrients = _normalize_nutrient_names(
        current_nutrients, new_nutrients)
    for key in new_nutrients:
        if key in current_nutrients.keys():
            if action_to_take == ModifyDictsAction.ADD:
                current_nutrients[key]['value'] += (new_nutrients[key]['value'] * ingredient_quantity)
            elif action_to_take == ModifyDictsAction.SUBTRACT:
                current_nutrients[key]['value'] -= (new_nutrients[key]['value'] * ingredient_quantity)
        else:
            current_nutrients[key] = new_nutrients[key]
    return current_nutrients

def print_my_nutrients_list_with_dropdown_lists(cached_ingredients: dict):
    list_of_my_ingredients = cached_ingredients.keys()
    for item in list_of_my_ingredients:
        st.write(item)
        st.session_state[f'st_selectbox_{item}'] = st.selectbox(
            'Please select how many of this food item you would like:',
            ['Remove ingredient from list'] + [number for number in range(1, 11)],
            index = 1,
            key = item)
        # button_remove_from_list(
        #     cached_ingredients_dict = cached_ingredients,
        #     api_ingredient_name = item,
        #     current_nutrients_i_have_data = st.session_state['nutrients_i_have_dict'],
        #     current_nutrients_i_need_data = st.session_state['nutrients_i_need_dict'])
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

def update_list_to_remove(
    list_to_remove: list,
    cached_ingredients: list
):
    list_to_remove.clear()
    for key in cached_ingredients:
        if cached_ingredients[key]['quantity'] == 0:
            list_to_remove.append(key)
    return list_to_remove
    

def delete_removed_dict_items(
    cached_ingredients: dict,
    list_to_delete: list        
):
    # list_to_delete = []
    # # breakpoint()
    # for key in cached_ingredients:
    #     if cached_ingredients[key]['quantity'] == 0:
    #         list_to_delete.append(key)
    # breakpoint()
    for item in list_to_delete:
        del cached_ingredients[item]
    # breakpoint()

def update_ingredient_quantities(
    cached_ingredients: dict,
    current_nutrients_i_have: dict,
    current_nutrients_i_need: dict
    # list_to_delete: list
):
    ingredients_list = st.container()
    with ingredients_list:
        list_of_my_nutrients = list(cached_ingredients.keys()) # <-- Does that solve the problem?
        for item in list_of_my_nutrients:
            dropdown_option = st.session_state[f'st_selectbox_{item}']
            cached_ingredient_quantity = cached_ingredients[item]['quantity']
            cached_ingredient_nutrients = cached_ingredients[item]['nutrients']
            if dropdown_option != cached_ingredient_quantity:
                if dropdown_option == 'Remove ingredient from list':
                    dropdown_ingredient_quantity = 0
                    quantity_difference = -1 * cached_ingredient_quantity
                    # Add to a new list called ingredients_to_delete, NEEDS TO BE FIRST DEFINED AS BLANK
                    # del cached_ingredients[item]
                else:
                    dropdown_ingredient_quantity = dropdown_option
                    quantity_difference = dropdown_ingredient_quantity - cached_ingredient_quantity
                modify_dicts(
                    current_nutrients = current_nutrients_i_have,
                    new_nutrients = cached_ingredient_nutrients,
                    ingredient_quantity = quantity_difference,
                    action_to_take = ModifyDictsAction.ADD
                )
                modify_dicts(
                    current_nutrients = current_nutrients_i_need,
                    new_nutrients = cached_ingredient_nutrients,
                    ingredient_quantity = quantity_difference,
                    action_to_take = ModifyDictsAction.SUBTRACT
                )
                cached_ingredients[item]['quantity'] = dropdown_ingredient_quantity
    # _delete_removed_dict_items(
    #     cached_ingredients = cached_ingredients,
    #     list_to_delete = list_to_delete
    # )

if __name__ == '__main__':

    st.title('Nutrient Guide')
    st.write('Copyright © 2024 Anschel Burk. All rights reserved.')

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
                st.session_state['search'], SEARCH_ENDPOINT, USDA_API_KEY)

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
            # button_remove_from_list(
            #         cached_ingredients_dict = st.session_state[
            #             'cached_ingredient_names_and_nutrients'],
            #         api_ingredient_name = st.session_state[
            #             'api_search_results_name'],
            #         current_nutrients_i_have_data = st.session_state[
            #             'nutrients_i_have_dict'],
            #         current_nutrients_i_need_data = st.session_state[
            #             'nutrients_i_need_dict']
            #     ) 
            draw_table_daily_values(
                format_json_data_as_dict(
                    st.session_state['api_search_results_nutrients']
                )
            )

        else:
            st.write(f'No results yet. Need help getting started? Try searching **sweet potato**.')

    with my_ingredients_list:
        st.subheader('My Ingredients List')
        update_list_to_remove(
            list_to_remove = st.session_state['dict_items_to_delete'],
            cached_ingredients = st.session_state['cached_ingredient_names_and_nutrients']
        )
        # breakpoint()
        delete_removed_dict_items(
            cached_ingredients = st.session_state['cached_ingredient_names_and_nutrients'],
            list_to_delete = st.session_state['dict_items_to_delete']
        )
        # breakpoint()
        print_my_nutrients_list_with_dropdown_lists(
                st.session_state['cached_ingredient_names_and_nutrients']
        )
        update_ingredient_quantities(
            cached_ingredients = st.session_state['cached_ingredient_names_and_nutrients'],
            current_nutrients_i_have = st.session_state['nutrients_i_have_dict'],
            current_nutrients_i_need = st.session_state['nutrients_i_need_dict']
            # list_to_delete = st.session_state['dict_items_to_delete']
        )


    with nutrients_i_have:
        st.subheader('Nutrients I Have')
        draw_table_daily_values(st.session_state['nutrients_i_have_dict'])

    with nutrients_i_need:
        st.subheader('Nutrients I Need')
        draw_table_daily_values(
            st.session_state['nutrients_i_need_dict']
        )
