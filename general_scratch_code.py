import streamlit as st

st.write('ORANGE')
st.selectbox(
    'Please select how many of this ingredient you would like to include:',
    list(range(0,11)),
    index=1,
    key='Text goes here'
)
st.write('\n')
st.write('APPLE')
st.selectbox(
    'Please select how many of this ingredient you would like to include:',
    list(range(0,11)),
    index=1,
    key='More text goes here'
)