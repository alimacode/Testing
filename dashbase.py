import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import calendar

#this pulls the filtering function 
from dfWriterFunction import filter_dataframe
from io import StringIO
from pandas.tseries.offsets import DateOffset 
from typing import List
from dateutil.parser import parse

#doing this in another file, but it recreates the basetable with year and month columns added from reporting dates. 
# preDateddf=pd.read_parquet(r"C:\Users\amalik\ProjectDash\Data\DASHBASE36MOB.parquet")


# preDateddf['DDMONTHYEAR'] = pd.to_datetime(preDateddf['ReportingDate'], format='%d%b%Y')
# # Separating the date into 'ReportingDate', 'Month', and 'Year' columns
# preDateddf['Month'] = preDateddf['DDMONTHYEAR'].dt.month
# preDateddf['Year'] = preDateddf['DDMONTHYEAR'].dt.year

# preDateddf.to_parquet('datedDf.parquet')

#reading in base table
# df is used for filtering, gdf is a copy for when filters are chosen     
df=pd.read_parquet(r"C:\Users\cmacedo\adhoc\SampleTest_Dates.parquet")


#Replace any NaN values with a string "None"
#Graph won't render otherwise


dfFixNone = df.replace(np.nan, 'None')
df= dfFixNone

#increasing container size that holds all filters
st.markdown(
'''
<style>
    .block-container{
        min-width: 1500px; 
    }
    
</style>
''', 
 unsafe_allow_html=True
)


#Unique list for Vintage
clist = df['Year'].unique().tolist()

st.title("Portfolio Dashboard")
st.divider()


#function that returns selected filters 
@st.experimental_fragment()
def filterMaker():
    #all selections are chosen, each selection filters and creates a unique list based on previous selection, function returns all selections as string variables 
    with st.container(border=True):
        st.subheader('Filters')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            selected_year = st.selectbox("Select Year", clist, key="selected_year")
            filtered_df = df[df["Year"] == selected_year]
            selected_interval = 'All'

            clist0 = filtered_df['TimeonBooks'].unique().tolist()
            clist0.insert(0, 'All')
            selected_data= st.selectbox("Select Data:", clist0, key="selected_data")
            if selected_data == 'All':
                filtered_df_data = filtered_df
            else:
                filtered_df_data = filtered_df[filtered_df['TimeonBooks'] == selected_data]
            
            clist1 = filtered_df_data['AccountNumber'].unique().tolist()
            clist1.insert(0, 'All')
            selected_firstsecond = st.selectbox("Select AccountNumber:", clist1, key="selected_firstsecond")

            #handling of 'All' selections, when all is selected the DF is not changed at all based on previous selection
            if selected_firstsecond == 'All':
                #filtered DF doesn't change from previous selection if all
                filtered_df_firstsecond = filtered_df_data
            else:
                #if not, make it the selected variable
                filtered_df_firstsecond = filtered_df_data[filtered_df_data['AccountNumber'] == selected_firstsecond]

        with col2:
            clist2 = filtered_df_firstsecond['Branding'].unique().tolist()
            clist2.insert(0, 'All') 
            selected_branding = st.selectbox("Select Branding:", clist2, key="selected_branding")
        
            if selected_branding == 'All':
                filtered_df_branding = filtered_df_firstsecond
            else:
                filtered_df_branding = filtered_df_firstsecond[filtered_df_firstsecond['Branding'] == selected_branding]


            clist3 = filtered_df_branding['AnnualFeeGroup'].unique().tolist()
            clist3.insert(0, 'All')
            selected_annualfeegroup = st.selectbox("Select Annual Fee Group: ", clist3, key="selected_annualfeegroup")
            
            if selected_annualfeegroup == 'All':
                filtered_df_annualfeegroup = filtered_df_branding
            else:
                filtered_df_annualfeegroup = filtered_df_branding[filtered_df_branding['AnnualFeeGroup'] == selected_annualfeegroup]
    with col3:
            clist4 = filtered_df_annualfeegroup['Association'].unique().tolist()
            clist4.insert(0, 'All')
            selected_association = st.selectbox("Select Association: ", clist4, key="selected_association")
            
            if selected_association == 'All':
                filtered_df_association = filtered_df_annualfeegroup
            else:
                filtered_df_association = filtered_df_annualfeegroup[filtered_df_annualfeegroup['Association'] == selected_association]


            clist5 = filtered_df_association['RetainedBusiness'].unique().tolist()
            clist5.insert(0, 'All')
            selected_retained = st.selectbox("Retained Business: ", clist5, key="selected_retained")

            if selected_retained == 'All':
                filtered_df_retained = filtered_df_association
            else:
                filtered_df_retained = filtered_df_association[filtered_df_association['RetainedBusiness'] == selected_retained]                

    with col4:
        clist6 = filtered_df_retained['ProductGroup'].unique().tolist()
        clist6.insert(0, 'All')
        selected_productgroup = st.selectbox("Select Product Group: ", clist6, key='selected_productgroup')

        if selected_productgroup == 'All':
            filtered_df_productgroup = filtered_df_retained
        else:
            filtered_df_productgroup = filtered_df_retained[filtered_df_retained['ProductGroup'] == selected_productgroup]


        clist8 = filtered_df_productgroup['OriginalCreditLineRange'].unique().tolist()
        clist8.sort()
        clist8.insert(0, 'All')
        selected_OriginalCreditLine = st.selectbox("Select OriginalCreditLine:", clist8, key="selected_OriginalCreditLine")
        if selected_OriginalCreditLine == 'All':
            filtered_df_OriginalCreditLine = filtered_df_productgroup
        else:
            filtered_df_OriginalCreditLine = filtered_df_productgroup[filtered_df_productgroup['OriginalCreditLineRange'] == selected_OriginalCreditLine]


        
    return selected_year, selected_data, selected_firstsecond, selected_branding, selected_annualfeegroup, selected_association,  selected_productgroup, selected_retained, selected_OriginalCreditLine

#takes all returned variables and makes them global vars
[selected_year, selected_data, selected_firstsecond, selected_branding, 
 selected_annualfeegroup, selected_association,  
 selected_productgroup, selected_retained, selected_OriginalCreditLine] = filterMaker()



# initializing blank dataframe to hold First df created from user filters
if 'blank_df' not in st.session_state:
    st.session_state['blank_df'] = pd.DataFrame()

# initialize dataframe to be add multiple plots
if "added_df" not in st.session_state:
    st.session_state['added_df'] = pd.DataFrame()

if "isDfAdded" not in st.session_state:
    st.session_state['isDfAdded'] = False

if 'add_counter' not in st.session_state:
    st.session_state['add_counter'] = 1

if 'selected_vintages_list' not in st.session_state:
    st.session_state.selected_vintages_list = []  

if 'datasets' not in st.session_state:
    st.session_state.datasets =[]


#button form 
# with st.form("dataForm"):
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         add1 = st.form_submit_button('Add Reporting Year')
#     with col2:
#         add4 = st.form_submit_button('Add 4 Vintages')
#     with col3:
#          add4years = st.form_submit_button('Add 4 Years')
#     with col4:
#         clear = st.form_submit_button('Clear All')
        
        
with st.form("dataForm"):
    col1, col3, col4 = st.columns(3)
    with col1:
        add1 = st.form_submit_button('Add Reporting Year')
    with col3:
         add4years = st.form_submit_button('Add 4 Years')
    with col4:
        clear = st.form_submit_button('Clear All')        

#this is where graphs start to be displayed
st.header("Data")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Account Purchase and Payment Metrics", "Income", "Balance Metrics", "CashFlow Metrics", "ACE Reserves", "CSV"])

@st.experimental_fragment()
def plot(df, xCol, yCol, lineGroup, labels, plcHolder, title):
    df['Months'] = df['Month'].apply(lambda x: calendar.month_abbr[x])
    xCol = 'Months'  # Use the new 'MonthName' column for plotting
    fig = px.line(df, x=xCol, y=yCol, line_group=lineGroup, labels=labels, color=lineGroup, markers=True)
    with plcHolder.container():
        st.subheader(title)
        st.plotly_chart(fig)

#empty place holders, necessary to be able to show each add4Vintages/add4Years iteration, 
# without it, the whole screen refreshes with each iteration and it looks choppy
with tab1:
    plotPlaceHolder1a = st.empty()  # Booked accts (New accounts?) g
    plotPlaceHolder1b = st.empty() # Payments / Active g
    plotPlaceHolder1c = st.empty() # active accts g
    plotPlaceHolder1d = st.empty() # Unwinds g
    plotPlaceHolder1e = st.empty() # avg vantage 3 score
    plotPlaceHolder1f = st.empty() # ChargeOffs/month g 
    # plotPlaceHolder1g = st.empty() # FraudRate 
with tab2:
    plotPlaceHolder2a = st.empty()  #PreTaxIncome g
    plotPlaceHolder2b = st.empty() #Ending Receivables g
    # plotPlaceHolder2c = st.empty() #Total Net Revenuee 
    # plotPlaceHolder2c = st.empty() #Gross Revenue 
    # plotPlaceHolder2d = st.empty() #ptiperactiveacct 
    # plotPlaceHolder3 = st.empty()  #CumlROA b
    # plotPlaceHolder3a = st.empty() #CumlROAAnnualized b
with tab3:
    plotPlaceHolder3a = st.empty() #avgBalancePerActiveAcct g
    # plotPlaceHolder3b = st.empty() #avgCLPerActiveAcct g
    # plotPlaceHolder3c = st.empty() #Net Charge Off g
# with tab4:
#     plotPlaceHolder4 = st.empty()  #chargeOffs per Month
#     plotPlaceHolder4a = st.empty() #UnitChargeOffRate
#     plotPlaceHolder4b = st.empty() #CumlUnitChargeOffRate
#     plotPlaceHolder4c = st.empty() #CumlNetChargeOffRate
# with tab5:
#     plotPlaceHolder5 = st.empty() #fraudRate
#     plotPlaceHolder5a = st.empty() #CumlFraudNetDollarRate

#function that displays each graph
@st.experimental_fragment()
def showGraph(df2):
        #THE FIRST FILTERED DF WILL DISPLAY, this case happens on first click of "Display Vintage"
    dfUsed = df2
    if st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == False:
        dfUsed = df2
    elif st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == True:
        dfUsed = st.session_state['added_df']


    with tab1:
        plot(dfUsed, 'Month', 'NewAccInd', 'Year', {'NewAccInd': 'Booked Accounts', 'x': 'Month'}, plotPlaceHolder1a, "Booked Accounts")
        plot(dfUsed, 'Month', 'Unwinds', 'Year', {'Unwinds': 'Unwinds', 'x': 'Month'}, plotPlaceHolder1b, "Unwinds")
        plot(dfUsed, 'Month', 'ActiveAccInd', 'Year', {'ActiveAccInd': 'Active Accounts / Month', 'x': 'Month'}, plotPlaceHolder1c, "Active Accounts")
        plot(dfUsed, 'Month', 'ChargeOffs', 'Year', {'ChargeOffs': 'ChargeOffs', 'x': 'Month'}, plotPlaceHolder1d, "ChargeOffs")
        plot(dfUsed, 'Month', 'PaymentsPerActive', 'Year', {'PaymentsPerActive': 'Payments Per Active', 'x': 'Month'}, plotPlaceHolder1e, "Payments Per Active")
        plot(dfUsed, 'Month', 'netPayments', 'Year', {'netPayments': 'Net Payments', 'x': 'Month'}, plotPlaceHolder1f, "Net Payments")
    with tab2:
         plot(dfUsed,'Month', 'PreTaxIncome', 'Year', {'PreTaxIncome': 'PreTaxIncome', 'x': 'Month'}, plotPlaceHolder2a, "PreTaxIncome")
         plot(dfUsed, 'Month', 'AnnualizedROA', 'Year', {'AnnualizedROA': 'Annualized ROA', 'x': 'Month'}, plotPlaceHolder2b, "Annualized ROA")
        #  plot(dfUsed, 'Month', 'Annual12MRollROA', 'Year', {'Annual12MRollROA': 'Annualized 12M Rolling ROA', 'x': 'Months on Book'}, plotPlaceHolder3a,  "Annualized 12M Rolling ROA")
    with tab3:
         plot(dfUsed,'Month', 'avgBalPActive', 'Year', {'avgBalPActive': 'Average Ending Balance Per Active', 'x': 'Month'}, plotPlaceHolder3a, "Average Ending Balance Per Active")
        #  plot(dfUsed,'Month', 'UtilRate', 'Year', {'UtilRate': 'UtilizationRate', 'x': 'Month'}, plotPlaceHolder3b, "Utilization Rate")
        #  plot(dfUsed, 'Month', 'AvgCLPerActive', 'Year', {'AvgCLPerActive': 'Average CreditLine Per Active', 'x': 'Month'}, plotPlaceHolder3c, "Average CreditLine Per Active")
         
        
    # with tab4:
    #      plot(dfUsed, 'Month', 'ChargeOffs', 'Year', {'y': 'Charge Off Count', 'x': 'Months on Book'}, plotPlaceHolder4, "ChargeOffs Per Month")
    #      plot(dfUsed, 'Month', 'UnitChargeOffRate', 'Year', {'y': 'Unit ChargeOff Rate', 'x': 'Months on Book'}, plotPlaceHolder4a, "Unit ChargeOff Rate")
    #      plot(dfUsed, 'Month', 'CumlUnitChargeOffRate', 'Year', {'y': 'Cumulative Unit ChargeOff Rate', 'x': 'Months on Book'}, plotPlaceHolder4b, "Cumulative Unit ChargeOff Rate")
    #      plot(dfUsed, 'Month', 'CumlNetChargeOffRate', 'Year', {'y': 'Cumulative Net ChargeOff Rate', 'x': 'Months on Book'}, plotPlaceHolder4c, "Cumulative Net ChargeOff Rate")
    # with tab5:
    #      plot(dfUsed, 'Month', 'cumlFraudRate', 'Year', {'y': 'Cumulative Fraud Rate', 'x': 'Months on Book'}, plotPlaceHolder5, "Cumulative Fraud Rate")
    #      plot(dfUsed, 'Month', 'CumlNetFraudDollRate', 'Year', {'y': 'Cumulative Net Fraud Dollar Rate', 'x': 'Months on Book'}, plotPlaceHolder5a, "Cumulative Net Fraud Dollar Rate")
    #with tab6:
    #     st.dataframe(dfUsed)




#this function creates a filtered DF based on the selection and displays graphs
#showGraphs is called from here
#Add4vintages and years are implemented in same function as if statements
@st.experimental_fragment()
def addToMain():

        if add1:
            with tab1: 
                
                    
                    #calls filter dataframe function (dfWriterFunction.py file)
                    result, selList = filter_dataframe(df, sel_vin=selected_year, sel_fs=selected_firstsecond, sel_brand=selected_branding, 
                                                       sel_annfee=selected_annualfeegroup ,sel_pg=selected_productgroup, sel_ogcl=selected_OriginalCreditLine, 
                                                       sel_ret=selected_retained, sel_assc=selected_association)
                    showGraph(result)
                    
                    #this is how it separates each plot line
                    df_add = result 
                    # unique_id =f"{'Year'}{selList}{st.session_state['add_counter']}" 
                    unique_id =f"{selList}{st.session_state['add_counter']}" 
                    st.session_state['add_counter'] += 1
                    # df_add[f"{'Year'}{selList}{st.session_state['add_counter']}"] = unique_id
                    df_add['Year'] = unique_id
                    st.session_state.selected_vintages_list.append(unique_id)

                    if 'add_counter' not in st.session_state:
                        st.session_state['add_counter'] = 1

                    #User has not yet added another dataframe to the initial dataframe, this runs if the Add button is hit for the First time
                    if st.session_state['added_df'].empty == True:
                        st.session_state['added_df'] = pd.concat(
                            [st.session_state['blank_df'], result], axis=0)
                        st.session_state['isDfAdded'] = False
                       
     

                    #User has added a df before, just take the previous df and concat with new one
                    elif st.session_state['added_df'].empty == False:
                        st.session_state['added_df'] = pd.concat(
                            [st.session_state['added_df'], df_add], axis=0)
                        st.session_state['isDfAdded'] = True
                        showGraph(result)
        
        # elif add4:
        #     start_vintage = pd.to_datetime(selected_vintage, format='%Y-%m')
            
        #     # date_range=pd.date_range(start_vintage + pd.DateOffset(months=1), periods=4, freq='M')
        #     date_range=pd.date_range(start_vintage, periods=4, freq='ME')
        #     formatted_dates=date_range.strftime('%Y-%m').tolist()
        #     i = 0
        #     for date in formatted_dates:
            
        #         result, selList = filter_dataframe(gdf, sel_vin=formatted_dates[i], sel_fs=selected_firstsecond, 
        #                                         sel_brand=selected_branding, sel_pg=selected_productgroup, 
        #                                         sel_channel=selected_channel, sel_sub=selected_subchannel, 
        #                                         sel_ogcl=selected_OriginalCreditLine, sel_mob=selected_interval)

        #         df_add = result 
        #         unique_id =f"{selList} {st.session_state['add_counter']}" 
        #         st.session_state['add_counter'] += 1
        #         df_add['Vintage'] = unique_id
        #         st.session_state.selected_vintages_list.append(unique_id)

        #         if 'add_counter' not in st.session_state:
        #             st.session_state['add_counter'] = 1

        #         #User has not yet added another dataframe to the initial dataframe, this runs if the Add button is hit for the First time
        #         if st.session_state['added_df'].empty == True:
        #             st.session_state['added_df'] = pd.concat(
        #                 [st.session_state['blank_df'], result], axis=0)
        #             st.session_state['isDfAdded'] = False
        #             showGraph(result)

        #         #User has added a df before, just take the previous df and concat with new one
        #         elif st.session_state['added_df'].empty == False:
        #             st.session_state['added_df'] = pd.concat(
        #                 [st.session_state['added_df'], df_add], axis=0)
        #             st.session_state['isDfAdded'] = True
        #             showGraph(result)

        #         i+=1
        elif add4years:
            parsed_date = pd.to_datetime(str(selected_year), format='ISO8601')
            # date_range=pd.date_range(start=parsed_date, periods=4, freq='YS-' + parsed_date.strftime('%b').upper())
            date_range2=pd.date_range(start=parsed_date, periods=4, freq=pd.DateOffset(years=1))
            
            formatted_dates = [year.year for year in date_range2]
            # formatted_dates=[int(date_str.split('-'[0]) for date_str in formatted_dates1)]
            print(formatted_dates)
            # formatted_dates=[year.strftime('%Y') for year in date_range2]
            j = 0 
            for date in formatted_dates:
                result, selList = filter_dataframe(df, sel_vin=formatted_dates[j], sel_fs=selected_firstsecond, sel_brand=selected_branding, 
                                                       sel_annfee=selected_annualfeegroup ,sel_pg=selected_productgroup, sel_ogcl=selected_OriginalCreditLine, 
                                                       sel_ret=selected_retained, sel_assc=selected_association)
                
                df_add = result 
                unique_id =f"{selList} {st.session_state['add_counter']}" 
                st.session_state['add_counter'] += 1
                df_add['Year'] = unique_id
                st.session_state.selected_vintages_list.append(unique_id)

                if 'add_counter' not in st.session_state:
                    st.session_state['add_counter'] = 1

                #User has not yet added another dataframe to the initial dataframe, this runs if the Add button is hit for the First time
                if st.session_state['added_df'].empty == True:
                    st.session_state['added_df'] = pd.concat(
                        [st.session_state['blank_df'], result], axis=0)
                    st.session_state['isDfAdded'] = False
                    showGraph(result)

                #User has added a df before, just take the previous df and concat with new one
                elif st.session_state['added_df'].empty == False:
                    st.session_state['added_df'] = pd.concat(
                        [st.session_state['added_df'], df_add], axis=0)
                    st.session_state['isDfAdded'] = True
                    showGraph(result)
                
                j+=1
                 

def clear_from_main():
    if clear:
        st.session_state.selected_vintages_list.clear()
        st.session_state['add_counter'] = 1
        df_clear = df.loc[(df['Year'] == None)
                                & (df['AccountNumber'] == None)
                                & (df['Branding'] == None)
                                & (df['ProductGroup'] == None)
                                & (df['RetainedBusiness'] == None)
                                & (df['Association'] == None)
                                & (df['AnnualFeeGroup'] == None)
                                & (df['OriginalCreditLineRange'] == None)]
        st.session_state['added_df'] = pd.concat([st.session_state['blank_df'], df_clear], axis=0)




if __name__ == "__main__":
    addToMain()
    clear_from_main()

