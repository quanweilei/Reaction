# Quanwei Lei University of Arizona
# https://github.com/quanweilei/Reaction/tree/master
# This is a streamlit app for University of Arizona Reaction Database,
# for Dr. Florian Goeltl

import streamlit as st
import pandas as pd
import numpy as np

import subprocess

# Streamlit config, must be called as the first line of code
st.set_page_config(layout="centered", page_title = "UAR Database", page_icon = "https://cdn.uadigital.arizona.edu/logos/v1.0.0/ua_wordmark_line_logo_white_rgb.min.svg")

# Function to install 'openpyxl' if not already installed
def install_openpyxl():
    try:
        import openpyxl
    except ImportError:
        st.warning("Installing 'openpyxl' library. Please wait...")
        subprocess.check_call(["pip", "install", "openpyxl"])
        st.success("'openpyxl' library has been installed!")

# Call the function to check and install 'openpyxl' if needed
install_openpyxl()
print("openpyxl installed")

html_string = '<head><link rel="stylesheet" href="https://cdn.digital.arizona.edu/lib/arizona-bootstrap/2.0.23/css/arizona-bootstrap.min.css" crossorigin="anonymous"><head>'

st.markdown(html_string, unsafe_allow_html=True)

top = '<body> <header id="region_header_ua" class="l-arizona-header bg-red"> <section class="container l-container"> <div class="row"> <a href="http://www.arizona.edu" title="The University of Arizona homepage" class="arizona-logo"> <img alt="The University of Arizona Wordmark Line Logo White" src="https://cdn.uadigital.arizona.edu/logos/v1.0.0/ua_wordmark_line_logo_white_rgb.min.svg" class="arizona-line-logo"> </a> </div> </section> </header></body>'
st.markdown(top, unsafe_allow_html=True)
st.divider()
# first open UAR-v1.0xlsx using pandas
# then create a dataframe with the data
@st.cache_resource
def loadDF():
    df = pd.read_excel('UAR-v1.0.xlsx')
    # get the unique values for each column
    return df

df = loadDF()
df['surface'] = df['surface'].astype(str)

# rename column that has no name to 'reactants'
df.rename(columns={'Unnamed: 4': 'reactants'}, inplace=True)

# print list of column names
cols = df.columns.tolist()
print(cols)
# get the unique values for each column
dE_U = df['delta E [eV]'].unique()
act_U = df['activation barrier [eV]'].unique()
metal_U = df['metal'].unique()
surface_U = df['surface'].unique()
reactants_U = df['reactants'].unique()
reagentB_U = df['reagent B'].unique()
productA_U = df['product A'].unique()
productB_U = df['product B'].unique()

# add a blank option to the beginning of each list
metal_U = np.insert(metal_U, 0, None)
surface_U = np.insert(surface_U, 0, None)
reactants_U = np.insert(reactants_U, 0, None)
reagentB_U = np.insert(reagentB_U, 0, None)
productA_U = np.insert(productA_U, 0, None)
productB_U = np.insert(productB_U, 0, None)

# create left and right column
left, right = st.columns(2)
with left:
    reactants = st.selectbox('Reactant A', reactants_U)
    productA = st.selectbox('Product A', productA_U)
    metal = st.selectbox('Metal', metal_U)
with right:
    reagentB = st.selectbox('Reactant B', reagentB_U)
    productB = st.selectbox('Product B', productB_U)
    surface = st.selectbox('Facet', surface_U)

# create selection box for 'delta E [eV]', 'activation barrier [eV]', 'metal', 'surface', 'reactants', 'reagent B', 'product A', 'product B'
dE = st.slider("Reaction Energy", min(dE_U), max(dE_U), value = (float(min(dE_U)), float(max(dE_U))), step=0.01)
act = st.slider("Activation Energy", min(act_U), max(act_U), value = (float(min(act_U)), float(max(act_U))), step=0.01)



pressed = st.button('Search')

@st.cache_resource
def updatedVals(reactants, productA, metal, surface, reagentB, productB, dE, act):
    df_display = df.copy()

    # if a column is None, then select all
    # for dE search take in dE, a double tuple and search for all values that are between (inclusive)
    df_display = df_display[(df_display['delta E [eV]'] >= dE[0]) & (df_display['delta E [eV]'] <= dE[1])]
    df_display = df_display[(df_display['activation barrier [eV]'] >= act[0]) & (df_display['activation barrier [eV]'] <= act[1])]

    if pd.isna(metal) == False:
        df_display = df_display[df_display['metal'] == metal]
    if pd.isna(surface) == False:
        df_display = df_display[df_display['surface'] == surface]
    if pd.isna(reactants) == False:
        df_display = df_display[df_display['reactants'] == reactants]
    if pd.isna(reagentB) == False:
        df_display = df_display[df_display['reagent B'] == reagentB]
    if pd.isna(productA) == False:
        df_display = df_display[df_display['product A'] == productA]
    if pd.isna(productB) == False:
        df_display = df_display[df_display['product B'] == productB]
    return df_display

if pressed:
    df_display = updatedVals(reactants, productA, metal, surface, reagentB, productB, dE, act)
    print(df_display)
    st.dataframe(df_display)
