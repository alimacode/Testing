Give a presentation that walks the audience through this code: import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import numpy as np
 
 
df =pd.read_csv(r"\\fnbm.corp\share\Risk\Enterprise Risk\PortfolioManagement\Personal Folders\Camila Macedo\Notes\demobase.csv")
df = df.replace(np.nan, 'None')
               
st.header("Demo Example")
 
df['ReportingDate'] = pd.to_datetime(df['ReportingDate'], format='%d%b%Y')
 
df['ReportingMonth'] = df['ReportingDate'].dt.strftime('%b')
 
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
 
df['ReportingMonth'] = pd.Categorical(df['ReportingMonth'], categories=month_order, ordered=True)
 
df = df.sort_values(by='ReportingMonth').reset_index(drop=True)
 
st.scatter_chart(df, x="ReportingMonth", y="pretaxincome", color="ProductGroup", size="pretaxincome")
fig = px.bar(df, x="ReportingMonth", y="pretaxincome", color="ProductGroup", title="2024 Pre-TaxIncome by ProductGroup")
with st.container():
    st.subheader("2024 Pre-TaxIncome by ProductGroup")
    st.plotly_chart(fig)
 
 
if 'blank_df' not in st.session_state:
    st.session_state['blank_df'] = pd.DataFrame()
   
# initialize dataframe to be added to the main dataframe
if "added_df" not in st.session_state:
    st.session_state['added_df'] = pd.DataFrame()
 
if "isDfAdded" not in st.session_state:
    st.session_state['isDfAdded'] = False
 
if 'add_counter' not in st.session_state:
    st.session_state['add_counter'] = 1
 
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []
 
with st.container():
    st.header('Filters')
    col1= st.columns(1)
    addedSelections = []
             
clist = df['ProductGroup'].unique().tolist()
 
with st.container():
    selected_productgroup = st.selectbox("Select ProductGroup:", clist, key="selected_productgroup")
    with st.form('my_form'):
        add = st.form_submit_button('Add')
       
def add_to_main():
   
        if add:
            filtered_df = df.loc[(df['ProductGroup'] == selected_productgroup)]
            unique_id =f"{selected_productgroup} {st.session_state['add_counter']}"
            st.session_state['add_counter'] += 1
            filtered_df['ProductGroup'] = unique_id
 
            st.session_state.selected_options.append(unique_id)
 
            if 'add_counter' not in st.session_state:
                st.session_state['add_counter'] = 1
            #IF THE ADDED DF IS EMPTY
            #User has not yet added another dataframe to the initial dataframe, this runs if the Add button is hit for the First time
            if st.session_state['added_df'].empty == True:
                st.session_state['added_df'] = pd.concat(
                    [st.session_state['blank_df'], filtered_df], axis=0)
            #IF THE ADDED DF IS NOT EMPTY
            #User has added a df before, just take the previous df and concat with new one
            elif st.session_state['added_df'].empty == False:
                st.session_state['added_df'] = pd.concat(
                    [st.session_state['added_df'], filtered_df], axis=0)
            st.session_state['isDfAdded'] = True
           
if __name__ == "__main__":
    add_to_main()
   
if st.session_state['blank_df'].empty == False and st.session_state['isDfAdded'] == False:
    fig1 = px.bar(st.session_state['blank_df'], x=st.session_state['blank_df']['ReportingMonth'], y=st.session_state['blank_df']['pretaxincome'],
    color=st.session_state['blank_df']['ProductGroup'], title='2024 Pre-TaxIncome by ProductGroup')
    st.plotly_chart(fig1)
    st.dataframe(st.session_state['blank_df'])
 
elif st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == True:
    fig3a = px.bar(st.session_state['added_df'], x=st.session_state['added_df']['ReportingMonth'], y=st.session_state['added_df']['pretaxincome'],
    color=st.session_state['added_df']['ProductGroup'], title='2024 Pre-TaxIncome by ProductGroup')
    st.plotly_chart(fig3a)
    st.dataframe(st.session_state['added_df'])