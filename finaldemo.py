import streamlit as st
import pandas as pd
import plotly.express as px
 
df=pd.read_csv(r"C:\Users\cmacedo\demobase.csv")
 
print(df.head())
print(df.dtypes)
 
df['ReportingDate_dt'] = pd.to_datetime(df['ReportingDate'], format='%d%b%Y')
 
print(df.head())
print(df.dtypes)
 
fig = px.bar(df.sort_values('ReportingDate_dt'), x="ReportingDate", y="pretaxincome", color="ProductGroup", title="2024 Pre-TaxIncome by ProductGroup")
 
st.subheader("2024 Pre-TaxIncome by ProductGroup")
st.plotly_chart(fig)
 
if 'blank_df' not in st.session_state:
    st.session_state['blank_df'] = pd.DataFrame()
    
if "added_df" not in st.session_state:
    st.session_state['added_df'] = pd.DataFrame()
 
if "flag" not in st.session_state:
    st.session_state['flag'] = False
    
if 'counter' not in st.session_state:
    st.session_state['counter'] = 1
 
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []
 
clist = df['ProductGroup'].unique().tolist()
selected_productgroup = st.selectbox("Select ProductGroup:", clist, key="selected_productgroup")
 
filtered_df = df.loc[(df['ProductGroup'] == selected_productgroup)]
fig2 = px.bar(filtered_df.sort_values('ReportingDate_dt'), x="ReportingDate", y="pretaxincome", color="ProductGroup", title="2024 Pre-TaxIncome by ProductGroup")
st.plotly_chart(fig2)
 
with st.form('my_form'):
    add = st.form_submit_button('Add')
 
def add_to_main():
    if add:
        filtered_df2 = df.loc[(df['ProductGroup'] == selected_productgroup)]
        unique_id =f"{selected_productgroup} {st.session_state['counter']}" 
        filtered_df2['ProductGroup'] = unique_id
 
        st.session_state.selected_options.append(unique_id)
        
        if st.session_state['added_df'].empty == True:
            st.session_state['added_df'] = pd.concat(
                [st.session_state['blank_df'], filtered_df2], axis=0)
        elif st.session_state['added_df'].empty == False:
            st.session_state['added_df'] = pd.concat(
                [st.session_state['added_df'], filtered_df2], axis=0)
        
        st.session_state['flag'] = True 
        st.session_state['counter'] += 1
                    
add_to_main()
 
if st.session_state['blank_df'].empty == False and st.session_state['flag'] == False: 
    fig3 = px.bar(st.session_state['blank_df'], x=st.session_state['blank_df']['ReportingDate'], y=st.session_state['blank_df']['pretaxincome'],
    color=st.session_state['blank_df']['ProductGroup'], title='2024 Pre-TaxIncome by ProductGroup')
    st.plotly_chart(fig3)
    st.dataframe(st.session_state['blank_df'])
 
elif st.session_state['added_df'].empty == False and st.session_state['flag'] == True:
    fig4 = px.bar(st.session_state['added_df'], x=st.session_state['added_df']['ReportingDate'], y=st.session_state['added_df']['pretaxincome'],
    color=st.session_state['added_df']['ProductGroup'], title='2024 Pre-TaxIncome by ProductGroup')
    st.plotly_chart(fig4)
    st.dataframe(st.session_state['added_df'])
 
 
