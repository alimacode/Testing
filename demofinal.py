import streamlit as st
import pandas as pd
import plotly.express as px
 
# Loading the csv file containing our data into a Pandas dataframe
df=pd.read_csv(r"C:\Users\cmacedo\demobase.csv")
 
# Reviewing the Data Load
print(df.head())
print(df.dtypes)
 
# Converting Dates
# Convert the ReportingDate column from string format to a datetime object
# This allows for sorting, filtering, and visualizing the data chronologically
df['ReportingDate_dt'] = pd.to_datetime(df['ReportingDate'], format='%d%b%Y')
 
 
# Maintaining Session State
# Allows perisitence of variables across user interactions during a single session
# Initializing these variables in st.session_state only if they don't exist
 
# A placeholder for the unfiltered data (empty at the start)
if 'blank_df' not in st.session_state:
    st.session_state['blank_df'] = pd.DataFrame()
 
# Tracking data added by the user
if "added_df" not in st.session_state:
    st.session_state['added_df'] = pd.DataFrame()
 
# Using a boolean flag to control logic for displaying updated data
if "flag" not in st.session_state:
    st.session_state['flag'] = False
 
# Using a counter to generate unique identifiers for filtered data
if 'counter' not in st.session_state:
    st.session_state['counter'] = 1
 
# Creating a list to track user-selected ProductGroups
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []
 
# Filter by ProductGroup
# Display a dropdown for users to select a ProductGroup
clist = df['ProductGroup'].unique().tolist()
selected_productgroup = st.selectbox("Select ProductGroup:", clist, key="selected_productgroup")
 
# In order to use a button, we have to use it within a form, which group UI elements
# The button triggers logic to add the filtered data to the session_state
with st.form('my_form'):
    add = st.form_submit_button('Add')
 
# We created a function to append the selected ProductGroups' data to the added_df dataframe in session state
# Tracking the addition of these selections using a flag and a counter
def add_to_main():
    if add:
        # Filtering the data based on the selected ProductGroup
        filtered_df = df.loc[(df['ProductGroup'] == selected_productgroup)]
       
        # Creating a unique identifier for the ProductGroup using a counter
        unique_id =f"{selected_productgroup} {st.session_state['counter']}"
        filtered_df['ProductGroup'] = unique_id
 
        # Keeping track of each user selection by adding each unique_id generated to a list
        st.session_state.selected_options.append(unique_id)
       
        # Appending the filtered data to the added_df dataframe in session_state
        if st.session_state['added_df'].empty == True:
            st.session_state['added_df'] = pd.concat(
                [st.session_state['blank_df'], filtered_df2], axis=0)
        elif st.session_state['added_df'].empty == False:
            st.session_state['added_df'] = pd.concat(
                [st.session_state['added_df'], filtered_df2], axis=0)
       
        # Updating the flag and incrementing the counter
        # At the start of the session, the flag is initialized to False to indicate no user action has occured yet.
        # Here we are updating the flag to True to signal that data has been modified by the user.
        st.session_state['flag'] = True
        st.session_state['counter'] += 1
 
# Call the Function                    
add_to_main()
 
# Based on the state of blank_df or added_df, the app dynamically updates the visualization
# Here the app checks the value of Flag to decide which DataFrame (blank_df or added_df) should be used to update
# the visualization and display the data.
# If flag is False, it means no new data has been added, so the app uses the original blank_df for the visualization
if st.session_state['blank_df'].empty == False and st.session_state['flag'] == False:
    fig1 = px.bar(st.session_state['blank_df'], x=st.session_state['blank_df']['ReportingDate'], y=st.session_state['blank_df']['pretaxincome'],
    color=st.session_state['blank_df']['ProductGroup'], title='2024 PTI by ProductGroup')
    st.plotly_chart(fig1)
    st.dataframe(st.session_state['blank_df'])
 
# If flag is True, it means new data has been added, so the app uses the updated added_df for visualization:
elif st.session_state['added_df'].empty == False and st.session_state['flag'] == True:
    fig2 = px.bar(st.session_state['added_df'], x=st.session_state['added_df']['ReportingDate'], y=st.session_state['added_df']['pretaxincome'],
    color=st.session_state['added_df']['ProductGroup'], title='2024 Pre-TaxIncome by ProductGroup')
    st.plotly_chart(fig2)
    st.dataframe(st.session_state['added_df'])
# The flag acts as a signal to the app.
# The flag helps differentiate between the initial state (with no user actions) and the modified state (after the data has been added).
# By checking the flag the appy dynamically updates the display charts and data tables without resetting the session.