import streamlit as st
# import numpy as np
import pandas as pd
from daily_values import daily_values as dv

# map_data = pd.DataFrame(
#     np.random.randn(1000,2) / [50,50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)

st.title('Nutrition Guide')
search = st.text_input('Search an ingredient:')
st.write(f'You searched: {search}')

st.title('Results:')
results = pd.DataFrame.query(selfexpr=search.lower(), )
# results = dv.get(search.lower())
# st.write(results)