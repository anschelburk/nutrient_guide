import os
import pandas as pd
import requests
import streamlit as st

from daily_values import daily_values as dv, dailyvalues_blank as dv_blank
    
st.set_page_config(layout='wide')

def add_daily_value_dicts(dict1: dict, dict2: dict): # <-- not used yet
    final_added_dict = {}
    for key in dict1:
        if key in dict2:
            final_added_dict[key] = {
                'value' : dict1[key]['value'] - dict2[key]['value'],
                'unit' : dict1[key]['unit']
            }    
    return(final_added_dict)

def button_add_to_list(item_name, list_name):
    st_button_add_to_list = st.button('Add Ingredient to My List')
    if st_button_add_to_list:
        list_name.append(item_name)
    
def button_remove_from_list(item_name, list_name):
    st_button_remove_from_list = st.button('Remove Ingredient from My List')
    if st_button_remove_from_list:
        list_name.remove(item_name)

def draw_table_daily_values(data_source: dict):
    st.write(
        pd.DataFrame
            .from_dict(data_source, orient='index')
            .rename(columns={'value': 'Amount', 'unit': 'Units'})
        )

def draw_table_json_data(json_data):
    st.session_state['filtered_json_data'] = []
    for item in json_data:
        # filtered_item = {'nutrientName', 'value': item['value'], 'unit': item['unitName']}
        filtered_item = {'nutrientName': item['nutrientName'], 'value': item['value'], 'unit': item['unitName']}
        st.session_state['filtered_json_data'].append(filtered_item)
    # st.write(
    #     pd.DataFrame
    #         .from_dict(st.session_state['filtered_json_data'], orient='index')
    #         .rename(columns={'value': 'Amount', 'unit': 'Units'})
    # )
    st.write(pd.DataFrame(st.session_state['filtered_json_data'])
             .rename(
                 columns={
                     'nutrientName': 'Nutrient',
                     'value': 'Amount',
                     'unit': 'Units'
                 }
             ))
            #  .style.hide(axis='index'))
            #  .to_string(index=False))

def format_daily_values_dict(dailyvalues_dict: dict):
    st.session_state['formatted_daily_values_dict'] = {key: {"nutrient": value} for key, value in dailyvalues_dict.items()}

def get_search_results_data(searchbar_input):
        return(requests.get(
            st.session_state['search_endpoint'],
            params={"query": searchbar_input, "api_key": st.session_state['DEMO_KEY']}
        ))
    # results = requests.get(
    #     st.session_state.['search_endpoint'],
    #     params={"query" : searchbar_input, "api_key" : st.session_state.['DEMO_KEY']}
    #     )
    # return(results)

# def initialize_once(): # <-- alphabetize
#     return {'initialized': False}

# def perform_initialization(data: dict): # <-- alphabetize
#     if not data['initialized']:
#         print('Initializing once...')
#         data['initialized'] = True

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
    # return(
    #     get_search_results_data(searchbar_input).json().get('foods')[0].get('description')
    # )
    # results = get_search_results_data(searchbar_input)
    # results_name = results.json().get('foods')[0].get('description')
    # return(results_name)

def update_search_results_nutrients(searchbar_input):
    st.session_state['results_nutrients'] = get_search_results_data(searchbar_input).json().get('foods')[0].get('foodNutrients')
    # return(
        # get_search_results_data(searchbar_input).json().get('foods')[0].get('foodNutrients')
    # )
    # results = get_search_results_data(searchbar_input)
    # results_nutrients = results.json().get('foods')[0].get('foodNutrients')
    # return(results_nutrients)

if __name__ == '__main__':

    st.session_state['DEMO_KEY'] = os.getenv('DEMO_KEY', "") # <-- change to 'search_key'
    st.session_state['search_endpoint'] = 'https://api.nal.usda.gov/fdc/v1/foods/search'
    st.session_state['dailyvalues_full'] = dv
    st.session_state['dailyvalues_blank'] = dv_blank

    if not 'formatted_daily_values_dict_full' in st.session_state:
        st.session_state['formatted_daily_values_dict_full'] = format_daily_values_dict(dv)
    if not 'mylist_ingredients' in st.session_state:
        st.session_state['mylist_ingredients'] = []
    if not 'mylist_nutrients' in st.session_state:
        st.session_state['mylist_nutrients'] = {}
    if not 'results_name' in st.session_state:
        st.session_state['results_name'] = ''
    if not 'results_nutrients' in st.session_state:
        st.session_state['results_nutrients'] = ''

    # print('this prints just after the __main__ statement')

    # print('BEGINNING OF MAIN SECTION')

    # st.session_state['mylist_ingredients'] = [] # <-- was previously mylist_ingredients
    # print('Just after st.session_state['mylist_ingredients']')
    # print(f'st.session_state['mylist_ingredients'] = {st.session_state['mylist_ingredients']}')

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
            # st.session_state['search'] = search
            # st.write('Showing results for:' + get_search_results_name(st.session_state['search']))
            update_search_results_name(st.session_state['search'])
            update_search_results_nutrients(st.session_state['search'])
            st.write('Showing results for:', st.session_state['results_name'])
            # st.write('Showing results for:' + get_search_results_name(st.session_state['search']))
            
            # print('Just before add button')
            # print(f'st.session_state['mylist_ingredients'] = {st.session_state['mylist_ingredients']}')
            button_add_to_list(
                st.session_state['results_name'],
                st.session_state['mylist_ingredients']
                )
            # print('Just after add button')
            # print(f'st.session_state['mylist_ingredients'] = {st.session_state['mylist_ingredients']}')
            # print('Just before remove button')
            # print(f'st.session_state['mylist_ingredients'] = {st.session_state['mylist_ingredients']}')
            button_remove_from_list(
                st.session_state['results_name'],
                st.session_state['mylist_ingredients']
                )
            # print('Just after remove button.')
            # print(f'st.session_state['mylist_ingredients'] = {st.session_state['mylist_ingredients']}')
            draw_table_json_data(
                st.session_state['results_nutrients']
            )
            
        else:
            #st.write() doesn't seem to be able to recognize '\n'?
            st.write(f'No results yet. Need help getting started? Try searching **sweet potato**.')

    with my_ingredients_list:
        st.subheader('My Ingredients List')
        print_list_as_bullets(st.session_state['mylist_ingredients'])

    with nutrients_i_have:
        st.subheader('Nutrients I Have')
        nutrients_i_have_dict = st.session_state['dailyvalues_blank']
        draw_table_daily_values(nutrients_i_have_dict)

    with nutrients_i_need:
        st.subheader('Nutrients I Need')
        nutrients_i_need_dict = subtract_daily_value_dicts(
            st.session_state['dailyvalues_full'], nutrients_i_have_dict
            )
        draw_table_daily_values(nutrients_i_need_dict)