import streamlit as st
import openai as ai
from streamlit_extras.mandatory_date_range import date_range_picker

def get_date_range():
    st.write("""Choose a date range.""")
    date_range = date_range_picker()
    return date_range

def main():
    date_range = get_date_range()

st.write("Here's our first attempt at using data to create a table:")
st.write()
