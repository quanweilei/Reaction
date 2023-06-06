# Quanwei Lei University of Arizona
# https://github.com/quanweilei/Reaction/tree/master
# This is a streamlit app for University of Arizona Reaction Database,
# for Dr. Florian Goeltl

import streamlit as st
import pandas as pd
import numpy as np
import pip
pip.main(["install", "openpyxl"])

# create style to center align the title
style = "<style> h1 { text-align: center; color: #000000; } </style>"
st.markdown(style, unsafe_allow_html=True)

# create style to center align the text
style = "<style> div { text-align: center; color: #000000; } </style>"
st.markdown(style, unsafe_allow_html=True)


# create a title for the app, center the title
st.title('U of A Reaction Database')
st.text('This is a streamlit app for University of Arizona Reaction Database')

# first open UAR-v1.0xlsx using pandas
# then create a dataframe with the data
df = pd.read_excel('UAR-v1.0.xlsx')
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

# create selection box for 'delta E [eV]', 'activation barrier [eV]', 'metal', 'surface', 'reactants', 'reagent B', 'product A', 'product B'
dE = st.slider("delta E [eV]", min(dE_U), max(dE_U), value = (float(min(dE_U)), float(max(dE_U))), step=0.01)
act = st.slider("activation barrier [eV]", min(act_U), max(act_U), value = (float(min(act_U)), float(max(act_U))), step=0.01)
metal = st.selectbox('metal', metal_U)
surface = st.selectbox('surface', surface_U)
reactants = st.selectbox('reactants', reactants_U)
reagentB = st.selectbox('reagent B', reagentB_U)
productA = st.selectbox('product A', productA_U)
productB = st.selectbox('product B', productB_U)

pressed = st.button('Search')

if pressed:
    print("The button was pressed!")
    # parse df with the selections
    # if selection is none, then select all
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
    print(df_display)
    st.write(df_display)
