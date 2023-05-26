# Quanwei Lei University of Arizona
# https://github.com/quanweilei/Reaction/tree/master
# This is a streamlit app for University of Arizona Reaction Database,
# for Dr. Florian Goeltl

import streamlit as st
import pandas as pd
import numpy as np

# create a title for the app, center the title
st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>")

# first open UAR-v1.0xlsx using pandas
# then create a dataframe with the data
df = pd.read_excel('UAR-v1.0.xlsx')



