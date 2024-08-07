import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import saspy
import time
import calendar

#this pulls the filtering function 
from dfWriterFunction2 import filter_dataframe
from io import StringIO
from pandas.tseries.offsets import DateOffset 
from typing import List
from dateutil.parser import parse

css='''
<style>
    .remove-font {
        font-size:20px !important;
        height:3em;
        width: 3em;
    }
    
    .stButton > button {
        height:3em;
        width: 7em;
       background-color: #0A5EC0;
       color: white;
         border: 1px solid #fff;
        border-radius: 20px;
    }
    .stButton > button:hover {
       background-color: #0E4594;
       color: white;
  
    }
    [data-testid=stDecoration]{
        background-image: linear-gradient(90deg, rgb(26, 117, 209), rgb(206, 230, 255));
    }
    [data-testid=stForm]{
        border-color:#f0f2f6;
    }
    
   .css-uf99v8 {
       
        display: flex;
        flex-direction: column;
        width: 100%;
        overflow: auto;
        -webkit-box-align: center;
        align-items: flex-center;
    }

    .css-b0wffi {
        display: flex;
        flex-direction: column;
        
        -webkit-box-align: end;
        align-items: end;
    }
    
    css-j503o6 {
      -webkit-box-align: start;
      align-items: flex-start;
     }
    
   
</style>
'''
st.markdown(css, unsafe_allow_html=True)


# df=pd.read_csv(r"\\fnbmcorp\share\Risk\Enterprise Risk\PortfolioManagement\VintageComparisonGraphs\Data\columns.csv")
# df.to_parquet(r"\\fnbmcorp\share\Risk\Enterprise Risk\PortfolioManagement\VintageComparisonGraphs\Data\columns.parquet")
# df=pd.read_parquet(r"C:\Users\amalik\ProjectDash\Data\DASHBASE36MOB.parquet")
# df=pd.read_parquet(r"C:\Users\cmacedo\Data\vcr_base_24.parquet")

# df=pd.read_parquet(r"C:\Users\cmacedo\Data\dashbase.parquet")


#doing this in another file, but it recreates the basetable with year and month columns added from reporting dates. 
# preDateddf=pd.read_parquet(r"C:\Users\cmacedo\Data\test.parquet")

# preDateddf['DDMONTHYEAR'] = pd.to_datetime(preDateddf['ReportingDate'], format='%d%b%Y')
# # Separating the date into 'ReportingDate', 'Month', and 'Year' columns
# preDateddf['Month'] = preDateddf['DDMONTHYEAR'].dt.month
# preDateddf['Year'] = preDateddf['DDMONTHYEAR'].dt.year

# preDateddf.to_parquet(r"C:\Users\cmacedo\Data\datedDf2.parquet")

#reading in base table
# df is used for filtering, gdf is a copy for when filters are chosen     
df=pd.read_parquet(r"C:\Users\cmacedo\Data\datedDf2.parquet")



gdf = df

#Replace any NaN values with a string "None"
#Graph won't render otherwise
dfFixNone = df.replace(np.nan, 'None')
df= dfFixNone


col1000, col2000, col3000 = st.columns([1,82,1], gap="Small")

#Unique list for Vintage

clist_a = df['TimeonBooks'].unique().tolist()
clist_test = df['Vintage'].unique().tolist()
clist = clist_test[-18:]
# clist_1 = df['AccountNumber'].unique().tolist()
# clist1 = clist_1.insert(0, 'All')
@st.experimental_fragment()
def filterSelector():
        st.header('Filters')
        
        selected_group = st.selectbox("Select ALL Vintages or PPQ:", clist_a, key="selected_group")
        filtered_df = df[df["TimeonBooks"] == selected_group]
        # selected_interval = 'All'
    
        # if selected_group == 'All':
        #     filtered_df_group = filtered_df
        # else:
        #     filtered_df_group = filtered_df[filtered_df['TimeonBooks'] == "selected_group"]
        
        # clist = filtered_df['Vintage'].unique().tolist()
        
        # clist.insert(0, ' ')
        selected_vintage = st.selectbox("Select Vintage:", clist, key="selected_vintage")
        #filter df based on selected vintage
        if selected_vintage == ' ':
            filtered_df_vintage= filtered_df
        else:
            filtered_df_vintage = filtered_df[filtered_df['Vintage'] == selected_vintage]
        
        # clist1 = filtered_df['FirstSecond'].unique().tolist()
        clist1 = filtered_df_vintage['AccountNumber'].unique().tolist()
        clist1.insert(0, 'All')
        #have to remove and reinsert as first becasue of how the current base pull is coded 
        selected_firstsecond = st.selectbox("Select Account Number:", clist1, key="selected_firstsecond")

        #handling of 'All' selections, when all is selected the DF is not changed at all based on previous selection
        if selected_firstsecond == 'All':
            filtered_df_firstsecond = filtered_df_vintage
        else:
            filtered_df_firstsecond = filtered_df_vintage[filtered_df_vintage['AccountNumber'] == selected_firstsecond]


        clist2 = filtered_df_firstsecond['Branding'].unique().tolist()

        clist2.insert(0, 'All')
        selected_branding = st.selectbox("Select Branding:", clist2, key="selected_branding")

        if selected_branding == 'All':
            filtered_df_branding = filtered_df_firstsecond
        else:
            filtered_df_branding = filtered_df_firstsecond[filtered_df_firstsecond['Branding'] == selected_branding]


        clist3 = filtered_df_branding['RetainedBusiness'].unique().tolist()

        clist3.insert(0, 'All')
        selected_subchannel = st.selectbox("Select Retained Business:", clist3, key="selected_subchannel")
        
        if selected_subchannel == 'All':
            filtered_df_subchannel = filtered_df_branding
        else:
            filtered_df_subchannel = filtered_df_branding[filtered_df_branding['RetainedBusiness'] == selected_subchannel]

        clist4 = filtered_df_subchannel['ProductGroup'].unique().tolist()

        clist4.insert(0, 'All')
        selected_acquisitions = st.selectbox("Select ProductGroup:", clist4, key="selected_acquisitions")

        if selected_acquisitions == 'All':
            filtered_df_acquisitions = filtered_df_subchannel
        else:
            filtered_df_acquisitions = filtered_df_subchannel[filtered_df_subchannel['ProductGroup'] == selected_acquisitions]

        
        clist5 = filtered_df_acquisitions['dimBucketID'].unique().tolist()

        clist5.insert(0, 'All')
        selected_source = st.selectbox("Select dimBucketID:", clist5, key="selected_source")

        if selected_source == 'All':
            filtered_df_source = filtered_df_acquisitions
        else:
            filtered_df_source = filtered_df_acquisitions [filtered_df_acquisitions ['dimBucketID'] == selected_source]

        clist6 = filtered_df_source['Association'].unique().tolist()

        clist6.insert(0, 'All')
        selected_association = st.selectbox("Select Association:", clist6, key="selected_association")
        
        if selected_association == 'All':
            filtered_df_association = filtered_df_source
        else:
            filtered_df_association = filtered_df_source[filtered_df_source['Association'] == selected_association]

        
        clist7 = filtered_df_association['AnnualFeeGroup'].unique().tolist()

        clist7.insert(0, 'All')
        selected_annualfeegroup = st.selectbox("Select AnnualFeeGroup:", clist7, key="selected_annualfeegroup")
        
        if selected_annualfeegroup == 'All':
            filtered_df_annualfeegroup = filtered_df_association
        else:
            filtered_df_annualfeegroup = filtered_df_association[filtered_df_association['AnnualFeeGroup'] == selected_annualfeegroup]
            
        clist8 = filtered_df_annualfeegroup['OriginalCreditLineRange'].unique().tolist()

        clist8.insert(0, 'All')
        selected_OriginalCreditLine = st.selectbox("Select OriginalCreditLine:", clist8, key="selected_OriginalCreditLine")

        if selected_OriginalCreditLine == 'All':
            filtered_df_OriginalCreditLine = filtered_df_annualfeegroup
        else:
            filtered_df_OriginalCreditLine = filtered_df_annualfeegroup[filtered_df_annualfeegroup['OriginalCreditLineRange'] == selected_OriginalCreditLine]
            
        return selected_group, selected_vintage, selected_firstsecond, selected_branding, selected_subchannel, selected_acquisitions, selected_source, selected_association, selected_annualfeegroup, selected_OriginalCreditLine



with st.sidebar:
    [selected_group, selected_vintage, selected_firstsecond, selected_branding, 
    selected_subchannel, selected_acquisitions, selected_source, 
    selected_association, selected_annualfeegroup, selected_OriginalCreditLine] = filterSelector()
    
    with st.form('my_form'):
        col1, col2= st.columns([1,1])
        col3, col4= st.columns([1,1])

        with col1:
            add = st.form_submit_button('Add')
        with col2:
            clear = st.form_submit_button('Clear All')
        with col3:
            add4 = st.form_submit_button('+4 Vintages')
        with col4:
            add12 = st.form_submit_button('+12 Vintages')

with col2000:
    st.header("Vintage Comparison")



    # initialize blank dataframe to hold First df created from user filters
    if 'blank_df' not in st.session_state:
        st.session_state['blank_df'] = pd.DataFrame()

    # initialize dataframe to be added to the main dataframe
    if "added_df" not in st.session_state:
        st.session_state['added_df'] = pd.DataFrame()


    if "isDfAdded" not in st.session_state:
        st.session_state['isDfAdded'] = False

    if 'add_counter' not in st.session_state:
        st.session_state['add_counter'] = 1

    if 'selected_vintages_list' not in st.session_state:
        st.session_state.selected_vintages_list = []


    #originalCreditLine = str(selected_OriginalCreditLine)

    
    @st.experimental_fragment()
    def plot(df, xCol, yCol, lineGroup, labels, plcHolder, title):
        # df['Months'] = df['Month'].apply(lambda x: calendar.month_abbr[x])
        # df['Months'] = range(1, len(df) + 1)
        # xCol = 'Months'  # Use the new 'MonthName' column for plotting
        fig = px.line(df, x=xCol, y=yCol, line_group=lineGroup, labels=labels, color=lineGroup, markers=True)
        with plcHolder.container():
            st.subheader(title)
            st.plotly_chart(fig)
    
    # def plot(df, xCol, yCol, lineGroup, labels, plcHolder, title):

    #     fig = px.line(df, x=xCol, y=yCol, line_group=lineGroup, labels=labels, color=lineGroup)
    #     with plcHolder.container():
    #         st.subheader(title)
    #         st.plotly_chart(fig)
    
    plotPlaceHolder1 = st.empty()  
    plotPlaceHolder2 = st.empty()  
    plotPlaceHolder2a = st.empty()  
    plotPlaceHolder3 = st.empty()  
    plotPlaceHolder4 = st.empty()  
    plotPlaceHolder5 = st.empty()  
    plotPlaceHolder6 = st.empty()  
    plotPlaceHolder7 = st.empty()  
    plotPlaceHolder7a = st.empty()  
    plotPlaceHolder8 = st.empty()  
    plotPlaceHolder9 = st.empty()  
    plotPlaceHolder10 = st.empty()  
    plotPlaceHolder11 = st.empty()  
    plotPlaceHolder12 = st.empty()  
    plotPlaceHolder13 = st.empty()  
    plotPlaceHolder14 = st.empty()  
    plotPlaceHolder15 = st.empty()  
    plotPlaceHolder16 = st.empty()  
    plotPlaceHolder17 = st.empty()  
    plotPlaceHolder18 = st.empty()  
    plotPlaceHolder19 = st.empty()  
    plotPlaceHolder20 = st.empty()  
    plotPlaceHolder21 = st.empty() 
    plotPlaceHolder22 = st.empty()   
    plotPlaceHolder23 = st.empty() 
    plotPlaceHolder24 = st.empty() 


    
    
    # plotPlaceHolder1a = st.empty() 
    # plotPlaceHolder1b = st.empty() 
    # plotPlaceHolder1c = st.empty() 
    # plotPlaceHolder1d = st.empty() 
    # plotPlaceHolder2 = st.empty()  
    # plotPlaceHolder2a = st.empty() 
    # plotPlaceHolder2b = st.empty() 
    # plotPlaceHolder2c = st.empty()
    # plotPlaceHolder4 = st.empty()
    # plotPlaceHolder11 = st.empty()
    # plotPlaceHolder12 = st.empty()
    # plotPlaceHolder13 = st.empty()
    # plotPlaceHolder14 = st.empty() 
    # plotPlaceHolder15 = st.empty()
    # plotPlaceHolder16 = st.empty() 
    # plotPlaceHolder17 = st.empty() 
    # plotPlaceHolder18 = st.empty()
    # plotPlaceHolder19 = st.empty()
    # plotPlaceHolder20 = st.empty()
    # plotPlaceHolder21 = st.empty()
    # plotPlaceHolder22 = st.empty()
    # plotPlaceHolder23 = st.empty()

    #function that displays each graph
    def showGraph(df2):
            #THE FIRST FILTERED DF WILL DISPLAY, this case happens on first click of "Display Vintage"
        dfUsed = df2
        if st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == False:
            dfUsed = df2
        elif st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == True:
            dfUsed = st.session_state['added_df']
        
        # plot(dfUsed, 'Month', 'NewAccInd', 'Year', {'NewAccInd': 'Booked Accounts', 'x': 'Month'}, plotPlaceHolder1a, "Booked Accounts")
        # plot(dfUsed,'Month', 'PreTaxIncome', 'Year', {'PreTaxIncome': 'PreTaxIncome', 'x': 'Month'}, plotPlaceHolder2a, "PreTaxIncome")
        plot(dfUsed, 'MOBS', 'PreTaxIncome', 'Vintage', {'PreTaxIncome': 'PreTaxIncome', 'MOBS': 'Months on Book'}, plotPlaceHolder1, "PreTax Income")
        plot(dfUsed, 'MOBS', 'cumlCO', 'Vintage', {'cumlCO': 'Cumulative ChargeOffs', 'MOBS': 'Months on Book'}, plotPlaceHolder2, "Cumulative ChargeOffs")
        plot(dfUsed, 'MOBS', 'cumlCONoFraud', 'Vintage', {'cumlCONoFraud': 'Cumulative ChargeOffs - No Fraud', 'MOBS': 'Months on Book'}, plotPlaceHolder2a, "Cumulative ChargeOffs - No Fraud")
        plot(dfUsed, 'MOBS', 'CumlUnitChargeOffRate', 'Vintage', {'CumlUnitChargeOffRate': 'Cumulative Unit Charge-Off Rate', 'MOBS': 'Months on Book', 'suffix': '%'}, plotPlaceHolder3, "Cumulative Unit Charge-Off Rate")
        plot(dfUsed, 'MOBS', 'UnitChargeOffRate', 'Vintage', {'UnitChargeOffRate': 'Unit Charge-Off Rate', 'MOBS': 'Months on Book'}, plotPlaceHolder4, "Unit ChargeOff Rate")
        plot(dfUsed, 'MOBS', 'C-5', 'Vintage', {'C-5': 'C-5 Roll Rate', 'MOBS': 'Months on Book', 'suffix': '%'}, plotPlaceHolder5, "C-5 Roll Rate")

    
        plot(dfUsed, 'MOBS', 'ActiveAccInd', 'Vintage', {'ActiveAccInd': 'Active Accounts', 'MOBS': 'Months on Book'}, plotPlaceHolder6, "Active Accounts")
        plot(dfUsed, 'MOBS', 'AnnualizedROA', 'Vintage', {'AnnualizedROA': 'Annualized ROA', 'MOBS': 'Months on Book'}, plotPlaceHolder7, "Annualized ROA")
        plot(dfUsed, 'MOBS', 'annualized12mrollROA', 'Vintage', {'annualized12mrollROA': 'Annualized 12M Rolling ROA', 'MOBS': 'Months on Book'}, plotPlaceHolder7a, "Annualized 12M Rolling ROA")
        plot(dfUsed, 'MOBS', 'cumlPTI', 'Vintage', {'cumlPTI': 'Cumulative PreTaxIncome', 'MOBS': 'Months on Book'}, plotPlaceHolder8, "Cumulative PreTax Income")
        plot(dfUsed, 'MOBS', 'EndingReceivable', 'Vintage', {'EndingReceivable': 'Gross Receivables', 'MOBS': 'Months on Book'}, plotPlaceHolder8, "Gross Receivables")
        plot(dfUsed, 'MOBS', 'cumlCO', 'Vintage', {'cumlCO': 'Cumulative ChargeOffs', 'MOBS': 'Months on Book'}, plotPlaceHolder8, "Cumulative ChargeOffs")
        plot(dfUsed, 'MOBS', 'CumlUnitChargeOffRate', 'Vintage', {'CumlUnitChargeOffRate': 'Cumulative Unit Charge-Off Rate', 'MOBS': 'Months on Book', 'suffix': '%'}, plotPlaceHolder9, "Cumulative Unit Charge-Off Rate")
        plot(dfUsed, 'MOBS', 'UnitChargeOffRate', 'Vintage', {'UnitChargeOffRate': 'Unit Charge-Off Rate', 'MOBS': 'Months on Book'}, plotPlaceHolder10, "Unit ChargeOff Rate")
        plot(dfUsed, 'MOBS', 'avgReceivable', 'Vintage', {'avgReceivable': 'Average Receivable Per Month', 'MOBS': 'Months on Book'}, plotPlaceHolder11, "Average Ending Receivable Per Month")
        plot(dfUsed,'MOBS', 'AvgEndBalPerBookedAcct', 'Vintage', {'AvgEndBalPerBookedAcct': 'Average Ending Balance Per Month', 'MOBS': 'Months on Book'}, plotPlaceHolder12, "Average Ending Balance Per Month")
        plot(dfUsed,'MOBS', 'UtilRate', 'Vintage', {'UtilRate': 'Utilization Rate', 'MOBS': 'Months on Book'}, plotPlaceHolder13, "Utilization Rate")

        plot(dfUsed, 'MOBS', 'CumlNetChargeOffRate', 'Vintage', {'CumlNetChargeOffRate': 'Cumlulative Net Charge-Off Rate', 'MOBS': 'Months on Book', 'suffix': '%'}, plotPlaceHolder14, "Cumulative Net Charge-Off Dollar Rate (Before Recoveries)")
        plot(dfUsed, 'MOBS', 'avgBalPActive', 'Vintage', {'avgBalPActive': 'Average Balance per Active', 'MOBS': 'Months on Book'}, plotPlaceHolder15, "Average Balance Per Active")
        plot(dfUsed, 'MOBS', 'cumlPTIPerBooked', 'Vintage', {'cumlPTIPerBooked': 'Cumulative PTI per Booked', 'MOBS': 'Months on Book'}, plotPlaceHolder16, "Cumulative Pre-Tax Income Per Booked")
        plot(dfUsed, 'MOBS', 'cumlGrossRevpBooked', 'Vintage', {'cumlGrossRevpBooked': 'Cumlulative Gross Revenue per Booked', 'MOBS': 'Months on Book'}, plotPlaceHolder17, "Cumulative Gross Revenue Per Booked")
        plot(dfUsed, 'MOBS', 'cumlFraudRate', 'Vintage', {'cumlFraudRate': 'Cumulative Fraud Rate', 'MOBS': 'Months on Book'}, plotPlaceHolder18, "Cumulative Fraud Rate")
        plot(dfUsed, 'MOBS', 'AvgPmtPerActive', 'Vintage', {'AvgPmtPerActive': 'Average Payment per Active', 'MOBS': 'Months on Book'}, plotPlaceHolder19, "Average Payment Per Active")
        plot(dfUsed, 'MOBS', 'cumlPmtsPerBookedAcct', 'Vintage', {'cumlPmtsPerBookedAcct': 'Cumulative Payments per Booked Account', 'MOBS': 'Months on Book'}, plotPlaceHolder20, "Cumulative Payments Per Booked Account")
        plot(dfUsed, 'MOBS', 'cumlPurPBookedAcct', 'Vintage', {'cumlPurPBookedAcct': 'Cumulative Purchase per Booked Account', 'MOBS': 'Months on Book'}, plotPlaceHolder21, "Cumulative Purchases Per Booked Account")
        plot(dfUsed, 'MOBS', 'CumlNetFraudDollRate', 'Vintage', {'CumlNetFraudDollRate': 'Cumulative Net Fraud Dollar Rate', 'MOBS': 'Months on Book'}, plotPlaceHolder22, "Cumulative Net Fraud Dollar Rate")
        plot(dfUsed, 'MOBS', 'AvgCLPerActive', 'Vintage', {'AvgCLPerActive': 'Average CreditLine Per Active', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder23, "Average CreditLine Per Active")
        
        
        
        
        # plot(dfUsed, 'ReportingDate', 'ActiveAccInd', 'Vintage', {'ActiveAccInd': 'Active Accounts', 'ReportingDate': 'Reporting Date'}, plotPlaceHolder1, "Active Accounts")
        # plot(dfUsed, 'MonthsOnBooks', 'CumlROAAnnual', 'Vintage', {'CumlROAAnnual': 'Annualized 12M Rolling ROA', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder1a, "Annualized 12M Rolling ROA")
        # plot(dfUsed, 'MonthsOnBooks', 'cumlPTI', 'Vintage', {'cumlPTI': 'Cumulative PreTaxIncome', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder1b, "Cumulative PreTax Income")
        # plot(dfUsed, 'MonthsOnBooks', 'EndingReceivable', 'Vintage', {'EndingReceivable': 'Gross Receivables', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder1c, "Gross Receivables")
        # plot(dfUsed, 'MonthsOnBooks', 'cumlCO', 'Vintage', {'cumlCO': 'Cumulative ChargeOffs', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder1d, "Cumulative ChargeOffs")
        # plot(dfUsed, 'MonthsOnBooks', 'CumlUnitChargeOffRate', 'Vintage', {'CumlUnitChargeOffRate': 'Cumulative Unit Charge-Off Rate', 'MonthsOnBooks': 'Months on Book', 'suffix': '%'}, plotPlaceHolder4, "Cumulative Unit Charge-Off Rate")
        # plot(dfUsed, 'MonthsOnBooks', 'UnitChargeOffRate', 'Vintage', {'UnitChargeOffRate': 'Unit Charge-Off Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder2, "Unit ChargeOff Rate")
        # plot(dfUsed, 'MonthsOnBooks', 'avgReceivable', 'Vintage', {'avgReceivable': 'Average Receivable Per Month', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder2, "Average Ending Receivable Per Month")
        # plot(dfUsed,'MonthsOnBooks', 'AvgEndBalPerBookedAcct', 'Vintage', {'AvgEndBalPerBookedAcct': 'Average Ending Balance Per Month', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder2a, "Average Ending Balance Per Month")
        # plot(dfUsed,'MonthsOnBooks', 'UtilRate', 'Vintage', {'UtilRate': 'Utilization Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder2b, "Utilization Rate")

        # plot(dfUsed, 'MonthsOnBooks', 'CumlNetChargeOffRate', 'Vintage', {'CumlNetChargeOffRate': 'Cumlulative Net Charge-Off Rate', 'MonthsOnBooks': 'Months on Book', 'suffix': '%'}, plotPlaceHolder11, "Cumulative Net Charge-Off Dollar Rate (Before Recoveries)")
        # plot(dfUsed, 'MonthsOnBooks', 'AvgAce2Score', 'Vintage', {'AvgAce2Score': 'Average ACE2 Score', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder12, "Average ACE2 Score")
        # plot(dfUsed, 'MonthsOnBooks', 'avgBalPActive', 'Vintage', {'avgBalPActive': 'Average Balance per Active', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder13, "Average Balance Per Active")
        # plot(dfUsed, 'MonthsOnBooks', 'cumlPTIPerBooked', 'Vintage', {'cumlPTIPerBooked': 'Cumulative PTI per Booked', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder14, "Cumulative Pre-Tax Income Per Booked")
        # plot(dfUsed, 'MonthsOnBooks', 'cumlGrossRevpBooked', 'Vintage', {'cumlGrossRevpBooked': 'Cumlulative Gross Revenue per Booked', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder15, "Cumulative Gross Revenue Per Booked")
        # plot(dfUsed, 'MonthsOnBooks', 'cumlFraudRate', 'Vintage', {'cumlFraudRate': 'Cumulative Fraud Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder16, "Cumulative Fraud Rate")
        # plot(dfUsed, 'MonthsOnBooks', 'AvgPmtPerActive', 'Vintage', {'AvgPmtPerActive': 'Average Payment per Active', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder17, "Average Payment Per Active")
        # plot(dfUsed, 'MonthsOnBooks', 'cumlPmtsPerBookedAcct', 'Vintage', {'cumlPmtsPerBookedAcct': 'Cumulative Payments per Booked Account', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder18, "Cumulative Payments Per Booked Account")
        # plot(dfUsed, 'MonthsOnBooks', 'AvgEndBalPerBookedAcct', 'Vintage', {'AvgEndBalPerBookedAcct': 'Average Ending Balance per Booked Account', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder19, "Average Ending Balance Per Booked Account")
        # plot(dfUsed, 'MonthsOnBooks', 'cumlPurPBookedAcct', 'Vintage', {'cumlPurPBookedAcct': 'Cumulative Purchase per Booked Account', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder20, "Cumulative Purchases Per Booked Account")
        # plot(dfUsed, 'MonthsOnBooks', 'CumlNetFraudDollRate', 'Vintage', {'CumlNetFraudDollRate': 'Cumulative Net Fraud Dollar Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder21, "Cumulative Net Fraud Dollar Rate")
        # plot(dfUsed, 'MonthsOnBooks', 'UtilRate', 'Vintage', {'UtilRate': 'UtilizationRate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder22, "Utilization Rate")
        # plot(dfUsed, 'MonthsOnBooks', 'AvgCLPerActive', 'Vintage', {'AvgCLPerActive': 'Average CreditLine Per Active', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder23, "Average CreditLine Per Active")

        st.dataframe(st.session_state['added_df'])
   
    @st.experimental_fragment
    def add_to_main():
        if add:
            #calls filter dataframe function (dfWriterFunction.py file)
            result, selList = filter_dataframe(gdf, sel_group=selected_group, sel_vin=selected_vintage, sel_fs=selected_firstsecond, 
                                        sel_brand=selected_branding, sel_sub=selected_subchannel, sel_acq=selected_acquisitions, sel_source=selected_source, 
                                        sel_assc=selected_association, sel_annfee=selected_annualfeegroup, sel_ogcl=selected_OriginalCreditLine)
            #this is how it separates each plot line


            df_add = result 
            unique_id =f"{selList} {st.session_state['add_counter']}" 
            st.session_state['add_counter'] += 1
            df_add['Vintage'] = unique_id
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


    def add_4_vintages():
        if add4:
            start_vintage = pd.to_datetime(selected_vintage, format='%Y-%m')
            
            # date_range=pd.date_range(start_vintage + pd.DateOffset(months=1), periods=4, freq='M')
            date_range=pd.date_range(start_vintage, periods=4, freq='ME')
            formatted_dates=date_range.strftime('%Y-%m').tolist()
            i = 0
            for date in formatted_dates:
            
                result, selList = filter_dataframe(gdf, sel_group=selected_group, sel_vin=formatted_dates[i], sel_fs=selected_firstsecond, 
                                        sel_brand=selected_branding, sel_sub=selected_subchannel, sel_acq=selected_acquisitions, sel_source=selected_source, 
                                        sel_assc=selected_association, sel_annfee=selected_annualfeegroup, sel_ogcl=selected_OriginalCreditLine)

                df_add = result 
                unique_id =f"{selList} {st.session_state['add_counter']}" 
                st.session_state['add_counter'] += 1
                df_add['Vintage'] = unique_id
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

                i+=1
                
    def add_12_vintages():
        if add12:
            start_vintage = pd.to_datetime(selected_vintage, format='%Y-%m')
            
            # date_range=pd.date_range(start_vintage + pd.DateOffset(months=1), periods=4, freq='M')
            date_range=pd.date_range(start_vintage, periods=12, freq='ME')
            formatted_dates=date_range.strftime('%Y-%m').tolist()
            j = 0
            for date in formatted_dates:
            
                result, selList = filter_dataframe(gdf, sel_group=selected_group, sel_vin=formatted_dates[j], sel_fs=selected_firstsecond, 
                                        sel_brand=selected_branding, sel_sub=selected_subchannel, sel_acq=selected_acquisitions, sel_source=selected_source, 
                                        sel_assc=selected_association, sel_annfee=selected_annualfeegroup, sel_ogcl=selected_OriginalCreditLine)

                df_add = result 
                unique_id =f"{selList} {st.session_state['add_counter']}" 
                st.session_state['add_counter'] += 1
                df_add['Vintage'] = unique_id
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
                               
    # def add_4_yrs():
    #     if add4_yrs:
    #         parsed_date = parse(selected_vintage)

    #         date_range=pd.date_range(start=parsed_date, periods=4, freq='YS-' + parsed_date.strftime('%b').upper())
    #         date_range2=pd.date_range(start=parsed_date.strftime('%Y-%m'), periods=4, freq=pd.DateOffset(years=1))

    #         formatted_dates=date_range2.strftime('%Y-%m').tolist()
    #         j = 0 
    #         for date in formatted_dates:
    #             result, selList = filter_dataframe(gdf, sel_group=selected_group, sel_vin=formatted_dates[j], sel_fs=selected_firstsecond, 
    #                                     sel_brand=selected_branding, sel_sub=selected_subchannel, sel_acq=selected_acquisitions, sel_source=selected_source, 
    #                                     sel_assc=selected_association, sel_annfee=selected_annualfeegroup, sel_ogcl=selected_OriginalCreditLine)
    

    #             df_add = result 
    #             unique_id =f"{selList} {st.session_state['add_counter']}" 
    #             st.session_state['add_counter'] += 1
    #             df_add['Vintage'] = unique_id
    #             st.session_state.selected_vintages_list.append(unique_id)

    #             if 'add_counter' not in st.session_state:
    #                 st.session_state['add_counter'] = 1

    #             #User has not yet added another dataframe to the initial dataframe, this runs if the Add button is hit for the First time
    #             if st.session_state['added_df'].empty == True:
    #                 st.session_state['added_df'] = pd.concat(
    #                     [st.session_state['blank_df'], result], axis=0)
    #                 st.session_state['isDfAdded'] = False
    #                 showGraph(result)

    #             #User has added a df before, just take the previous df and concat with new one
    #             elif st.session_state['added_df'].empty == False:
    #                 st.session_state['added_df'] = pd.concat(
    #                     [st.session_state['added_df'], df_add], axis=0)
    #                 st.session_state['isDfAdded'] = True
    #                 showGraph(result)
                
    #             j+=1
                   
            
    def clear_from_main():
            if clear:
                st.session_state.selected_vintages_list.clear()
                st.session_state['add_counter'] = 1
                df_clear = df.loc[(df['Vintage'] == None)
                                        & (df['AccountNumber'] == None)
                                        & (df['Branding'] == None)
                                        & (df['RetainedBusiness'] == None)
                                        & (df['ProductGroup'] == None)
                                        & (df['dimBucketID'] == None)
                                        & (df['Association'] == None)
                                        & (df['AnnualFeeGroup'] == None)
                                        & (df['OriginalCreditLineRange'] == None)]
                st.session_state['added_df'] = pd.concat([st.session_state['blank_df'], df_clear], axis=0)

    


    if __name__ == "__main__":
        add_to_main()
        clear_from_main()
        add_4_vintages()
        add_12_vintages()
        # add_4_yrs()    


    def convert_df_to_csv(df):
        output = StringIO()
        df.to_csv(output, index=False)
        return output.getvalue()

    if not st.session_state['added_df'].empty:
            csv = convert_df_to_csv(st.session_state['added_df'])
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='vintage_data.csv',
                        mime='text/csv',
            )


def remove_selected_vintage(vintage_to_remove):
        
    if f"{vintage_to_remove}" in st.session_state['added_df']['Vintage'].values:
        df = st.session_state['added_df'].drop(st.session_state['added_df'][st.session_state['added_df']['Vintage'] ==  f"{vintage_to_remove}"].index)
        st.session_state['added_df'] = df
        st.session_state['isDfAdded'] = not st.session_state['added_df'].empty
        st.session_state.selected_vintages_list.remove(vintage_to_remove)
        if st.session_state['added_df'].empty:
            st.session_state['isDfAdded'] = False
        st.experimental_rerun()
    
  
with col3000:          
    for i, vintage in enumerate(st.session_state.selected_vintages_list):
        if st.button(f"Remove {vintage}", key=f"remove_{i}"):
            remove_selected_vintage(vintage)
            
