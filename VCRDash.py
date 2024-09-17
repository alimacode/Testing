import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import saspy
import time

#this pulls the filtering function 
from dfWriterFunction import filter_dataframe
# from dfWriterFunction import VantageBarChart
# from dfWriterFunction import VantageLineChart
# from dfWriterFunction import NewVantageRange
from io import StringIO
from pandas.tseries.offsets import DateOffset 
from typing import List
from dateutil.parser import parse
pd.options.mode.chained_assignment = None 
css='''
<style>
   .remove-font {
       font-size: 20px !important;
       height: 3em;
       width: 3em;
   }
   /* Button styling (if needed) */
   /* .stButton > button {
       height: 4em;
       width: 8em;
       background-color: #0A5EC0;
       color: white;
       border: 1px solid #fff;
       border-radius: 25px;
   }
   .stButton > button:hover {
       background-color: #0E4594;
       color: white;
   } */
   [data-testid=stDecoration] {
       background-image: linear-gradient(90deg, rgb(26, 117, 209), rgb(206, 230, 255));
   }
   [data-testid=stForm] {
       border-color: #f0f2f6;
   }
   /* Flex container adjustments for responsiveness */
   .css-uf99v8 {
       display: flex;
       flex-direction: column;
       width: 100%;
       overflow: auto;
       align-items: center; /* Fixed: Changed from flex-center to center */
   }
   .css-b0wffi {
       display: flex;
       flex-direction: column;
       align-items: end; /* Adjusted alignment */
   }
   .css-j503o6 {
       display: flex;
       align-items: flex-start;
   }
   /* Block container adjustments */
   .block-container {
       width: 100%; /* Changed from min-width to width */
       max-width: 1100px; /* Max width to keep it responsive */
       margin: 0 auto;
       padding: 1rem; /* Add some padding */
   }
   .custom_container {
       max-width: 800px;
       width: 100%; /* Ensure it takes full width on smaller screens */
       margin: 0 auto;
       padding: 1rem; /* Add padding for better spacing */
   }
   /* Media queries for better responsiveness on mobile devices */
   @media (max-width: 768px) {
       .block-container, .custom_container {
           width: 90%; /* Use most of the screen width on smaller devices */
           padding: 0.5rem; /* Adjust padding */
       }
       .css-b0wffi, .css-uf99v8 {
           align-items: center; /* Center align for smaller screens */
           width: 100%; /* Ensure full width */
       }
       .remove-font {
           font-size: 16px !important; /* Adjust font size on smaller screens */
       }
   }
</style>

'''
st.markdown(css, unsafe_allow_html=True)


sourcesDict = {
   "All": "All",
   "AMEX DCO": "AMEX DCO",
   "BDOE": "Bulldog - Email",
   "BDOW": "Bulldog - Affiliates",
   "CCDC": "CreditCards.com",
   "CRCM": "Credit.com",
   "GOGS": "Google",
   "KRMA": "Credit Karma",
   "EXPX": "Experian",
   "CSOX": "Credit Sesame",
   "WWE": "WWE",
   "GOGP": "Google (Adwords)",
   "PDYS": "Yahoo / Bing",
   "GOON": "Nascar Paid",
   "NSRM": "PQ Abandon NASCAR",
   "PREE": "DM-Overlap (Fulfill)",
   "PQEQ": "PQ Abandon (MONTHLY)",
   "PCEG": "Closed Acct ReMkt",
   "PCHO": "Charge-Off Declines",
   "PQSD": "App Score Declines",
   "PQEF": "PQ Abandon (DAILY)",
   "FBRM": "Facebook (ReMkt)",
   "FBPS": "Facebook (Prospecting)",
   "NSFB": "FB NASCAR (Prospecting)",
   "GDRM": "Google Ad Banners",
   "NSCN": "NASCAR ITA Email",
   "VS500": "VS3 500-529",
   "VS53": "VS3 530-549",
   "VS455": "VS4 550-639",
   "VS464": "VS4 640-700",
   "VS470": "VS4 701-730",
   "VS55": "VS3 550-600",
   "VS60": "VS3 601-639",
   "VS64": "VS3 640-700",
   "VS70": "VS3 701-730",
   "FC55": "FICO 550-639",
   "FC64": "FICO 640-700",
   "EQUI": "Equifax 651-700",
   "EQUJ": "Equifax 550-650",
   "TU55": "Transunion 550-600",
   "TU60": "Transunion 601-639",
   "TU64": "Transunion 640-700",
   "TU70": "Transunion 701-730",
   "TUABDN": "Transunion PQ Abandon",
   "TUCO": "Transunion Charge Off",
   "TUPD": "Transunion PQ Declines",
   "TUPC": "Transunion Prior Closure",
   "EMCS": "Emerging Consumer",
   "PACLS": "Closed Remarket",
   "PADCL": "PQ Declines",
   "PAABN": "PQ Abandon",
   "PAPC": "Closed Remarket 5 Yr+",
   "PACO": "Charge-Offs",
   "remail": "Remail",
   "PQRMKT": "PQ Abandon(Daily)",
   "DRMT": "Remarket",
   "EFXABDN": "Equifax Abandon",
   "EFXCO": "Equifax Prior Charge-offs",
   "EFXPC": "Equifax Prior Closure",
   "None": "Organic",
   "SECA": "Multiple Account",
   "PITA": "3rd Party ITA",
   "PCEG": "Closed Remarket Email",
   "PDYN": "PDYN",
   "PQEP": "PQEP",
   "PQES": "PQES",
   "0":"Nothing"
}
st.title("vintage Comparison")
# df=pd.read_csv(r"\\fnbmcorp\share\Risk\Enterprise Risk\PortfolioManagement\vintageComparisonGraphs\Data\columns.csv")
# df.to_parquet(r"\\fnbmcorp\share\Risk\Enterprise Risk\PortfolioManagement\vintageComparisonGraphs\Data\columns.parquet")
# df=pd.read_parquet(r"C:\Users\amalik\ProjectDash\Data\DASHBASE36MOB.parquet")
# df=pd.read_parquet(r"C:\Users\cmacedo\Data\vcr_base_24.parquet")
# df=pd.read_parquet(r"C:\Users\amalik\VCRDashCURRENT\vcr_base_24.parquet")
# df=pd.read_parquet(r"C:\Users\cmacedo\FinalVCRDash\vcr_base_24.parquet")
# df=pd.read_parquet(r"C:\Users\cmacedo\FinalVCRDash\test1\testvcr2.parquet")
df=pd.read_parquet(r"testVCR3.parquet")
# df['vintage'] =  df['vintage']
# df['vintage'] = pd.to_datetime(df['vintage'])
# df['vintage'] = df['vintage'].dt.strftime('%Y-%m')
# df['vintage'] = df['vintage']

# df['MonthsOnBooks'] = df['MonthsOnBooks']
#Replace any NaN values with a string "None"
#Graph won't render otherwise
#df = df.replace(np.nan, 'None')
df.replace(regex = "nan", value = "", inplace = True)
df.replace(regex = "None", value = "", inplace = True)

#Unique list for vintage
clist = df['vintage'].unique().tolist()
maxvintage = clist[-1]


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

if 'KPI_DF' not in st.session_state:
    st.session_state['KPI_DF'] = pd.DataFrame()

if 'counter' not in st.session_state:
    st.session_state['counter'] = 1

if 'csvCounter' not in st.session_state:
    st.session_state.csvCounter = 1

if 'expanderAmt' not in st.session_state:
    st.session_state.expanderAmt = 0

if 'expanderList' not in st.session_state:
    st.session_state.expanderList = []

if 'prevSelList' not in st.session_state:
    st.session_state.prevSelList = []

@st.experimental_fragment()
def filterSelector():
    with st.container(border=True):
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        st.header('Getting Started:')
        st.write("Use the filters to create and save unlimited custom selections.")
        st.write("Your selections are saved throughout your session; allowing you to build, modify, and compare unlimited combinations on the same graphs.")
        
    with st.container(border=True):
        col1, col2, col3, col4, col5= st.columns(5)
        addedSelections = []
        with col1:
            st.subheader("Filter and Button Use:", divider=False)
            st.write("To select one vintage at a time, choose your filter selections and click the :blue['Add'] button below")
            st.write("To select multiple vintages at a time, choose your start vintage and input how many vintages to increase it by. Then click the :blue['Multiple vintages'] button below")
            st.write("To start from scratch click :blue['Clear All']")    
        with col2:
            selected_vintage = st.selectbox("Select Start vintage:", clist, key="selected_vintage")
            
            addedSelections.append(selected_vintage)

            #gets next 12 vintages/years to calculate for multiple vintages/years functionality
            maxVinRange = pd.to_datetime(selected_vintage, format='%Y-%m')
            maxYrRange = pd.to_datetime(selected_vintage, format='%Y-%m') 

            dateRange=pd.date_range(maxVinRange, periods=12, freq='ME')
            dateRangeYears=pd.date_range(maxYrRange, periods=12, freq=pd.DateOffset(years=1))

            rangeList=dateRange.strftime('%Y-%m').tolist()
            yrList = dateRangeYears.strftime('%Y-%m').tolist()

            yrList2 = []
            
            #getting available years
            for date in clist:
                if date in yrList:
                    yrList2.append(date)
            maxVinRange = rangeList[-1]
            maxYrRange  = yrList[-1]


            #filter df based on selected vintage
            filtered_df = df[(df['vintage'] >= selected_vintage) & (df['vintage'] <= maxVinRange) | (df['vintage'].isin(yrList2))]
            
        with col3:
            clist1 = filtered_df['AccountNumber'].unique().tolist()
            #have to remove and reinsert as first becasue of how the current base pull is coded 
            clist1.insert(0, 'All')
            fsString = 'SecondAccount'
            if fsString in clist1:
                clist1.remove(fsString)
                clist1.insert(2, 'MAP')

            selected_firstsecond = st.selectbox("Select MAP:", clist1, key="selected_firstsecond")
            #handling of 'All' selections, when all is selected the DF is not changed at all based on previous selection
            if selected_firstsecond == 'All':
                #filtered DF doesn't change from previous selection if 'all'
                filtered_df_firstsecond = filtered_df
            elif selected_firstsecond == 'FirstAccount':
                #if not, make it the selected variable
                filtered_df_firstsecond = filtered_df[filtered_df['AccountNumber'] == selected_firstsecond]
                addedSelections.append(selected_firstsecond)
            elif selected_firstsecond == 'MAP':
                selected_firstsecond = 'SecondAccount'
                filtered_df_firstsecond = filtered_df[filtered_df['AccountNumber'] == selected_firstsecond]
                addedSelections.append(selected_firstsecond)
                
            clist2 = filtered_df_firstsecond['Branding'].unique().tolist()
            clist2.insert(0, 'All')
            selected_branding = st.selectbox("Select Branding:", clist2, key="selected_branding")
            if selected_branding == 'All':
                filtered_df_branding = filtered_df_firstsecond
            else:
                filtered_df_branding = filtered_df_firstsecond[filtered_df_firstsecond['Branding'] == selected_branding]
                addedSelections.append(selected_branding)
            
            clist2a = filtered_df_branding['AccountNumber'].unique().tolist()
            clist2a.insert(0, 'All')
            selected_accountnumber = st.selectbox("Select Account Number: ", clist2a, key='selected_accountnumber')
            if selected_accountnumber == 'All':
                filtered_df_accountnumber = filtered_df_branding
            else:
                filtered_df_accountnumber = filtered_df_branding[filtered_df_branding['AccountNumber'] == selected_accountnumber]
                addedSelections.append(selected_accountnumber)

        with col4:
            
            clist3 = filtered_df_accountnumber['Subchannel'].unique().tolist()
            clist3.insert(0, 'All')
            selected_subchannel = st.selectbox("Select Subchannel:", clist3, key="selected_subchannel")
            if selected_subchannel == 'All':
                filtered_df_subchannel = filtered_df_accountnumber
            else:
                filtered_df_subchannel = filtered_df_accountnumber[filtered_df_accountnumber['Subchannel'] == selected_subchannel]
                addedSelections.append(selected_subchannel)
            
            clist4 = filtered_df_subchannel['Acquisitions'].unique().tolist()
            clist4.insert(0, 'All')
            selected_acquisitions = st.selectbox("Select Acquisitions:", clist4, key="selected_acquisitions")
            if selected_acquisitions == 'All':
                filtered_df_acquisitions = filtered_df_subchannel
            else:
                filtered_df_acquisitions = filtered_df_subchannel[filtered_df_subchannel['Acquisitions'] == selected_acquisitions]
                addedSelections.append(selected_acquisitions)

            clist5 = filtered_df_acquisitions['Source'].unique().tolist()
            clist5spelled = [sourcesDict.get(abbr, "Unknown") for abbr in clist5]
            clist5spelled.insert(0, 'All')
            selected_source = st.selectbox("Select Source:", clist5spelled, key="selected_source")
            selected_sourceSpelled = selected_source
            if selected_source == 'All':
                filtered_df_source = filtered_df_acquisitions
            else:
                selected_source = list(sourcesDict.keys())[list(sourcesDict.values()).index(selected_source)]
                filtered_df_source = filtered_df_acquisitions [filtered_df_acquisitions ['Source'] == selected_source]
                addedSelections.append(selected_sourceSpelled)
        with col5:
            
            clist6 = filtered_df_source['Association'].unique().tolist()
            clist6.insert(0, 'All')
            selected_association = st.selectbox("Select Association:", clist6, key="selected_association")
            if selected_association == 'All':
                filtered_df_association = filtered_df_source
            else:
                filtered_df_association = filtered_df_source[filtered_df_source['Association'] == selected_association]
                addedSelections.append(selected_association)
                
            clist7 = filtered_df_association['AnnualFeeGroup'].unique().tolist()
            clist7.insert(0, 'All')
            selected_annualfeegroup = st.selectbox("Select AnnualFeeGroup:", clist7, key="selected_annualfeegroup")
            if selected_annualfeegroup == 'All':
                filtered_df_annualfeegroup = filtered_df_association
            else:
                filtered_df_annualfeegroup = filtered_df_association[filtered_df_association['AnnualFeeGroup'] == selected_annualfeegroup]
                addedSelections.append(selected_annualfeegroup)

            clist8 = filtered_df_annualfeegroup['OriginalCreditLine'].unique().tolist()
            clist8.insert(0, 'All')
            selected_OriginalCreditLine = st.selectbox("Select OriginalCreditLine:", clist8, key="selected_OriginalCreditLine")
            if selected_OriginalCreditLine == 'All':
                filtered_df_OriginalCreditLine = filtered_df_annualfeegroup
            else:
                filtered_df_OriginalCreditLine = filtered_df_annualfeegroup[filtered_df_annualfeegroup['OriginalCreditLine'] == selected_OriginalCreditLine]
                addedSelections.append(selected_OriginalCreditLine)

        buff, col, buff2 = st.columns([1,1,1])
        vintageAmt = col.number_input(label="vintages/Years to be added?", min_value=2, max_value=12, step=1, value=4)
        
        finalDf = filtered_df_OriginalCreditLine
        
    return [selected_vintage, finalDf, addedSelections, vintageAmt]

selected_vintage, filterDf, selList, vintageAmt = filterSelector()

with st.form("my_form"):
    col10, col11, col9, col12 = st.columns(4)
    with col10:
        add = st.form_submit_button('Add')
    with col12:
        clear = st.form_submit_button('Clear All')
    with col9:
        add4 = st.form_submit_button('Multiple vintages')
    with col11:
        add4_yrs = st.form_submit_button('Multiple Years')




def plot(df, xCol, yCol, lineGroup, labels, plcHolder, title):
        fig = px.line(df, x=xCol, y=yCol, line_group=lineGroup, labels=labels, color=lineGroup)
        with plcHolder.container():
            st.subheader(title)
            st.plotly_chart(fig)
        
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

@st.experimental_fragment()
def downloadButton(dfString, csv):
        st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"{dfString}{selected_vintage}.csv",
        mime="text/csv",
        key=f"{dfString}{st.session_state.csvCounter}"
        )  
        st.session_state.csvCounter += 1


def addExpander(title):
    global maxvintage
    if str(title[0]) <= maxvintage:
        st.session_state.expanderAmt += 1
        st.session_state.expanderList.append(f"{title}")
    expanders = [st.expander(title) for title in st.session_state.expanderList]
    return expanders


tabTitles = ["Graphs", "Metrics"]
tabs = st.tabs(tabTitles)

with tabs[0]:
    plotPlaceHolder1 = st.empty()  
    plotPlaceHolder1a = st.empty() 
    plotPlaceHolder1b = st.empty() 
    plotPlaceHolder1c = st.empty() 
    plotPlaceHolder1d = st.empty() 
    plotPlaceHolder2 = st.empty()  
    plotPlaceHolder2a = st.empty() 
    plotPlaceHolder2b = st.empty() 
    plotPlaceHolder2c = st.empty()
    plotPlaceHolder4 = st.empty()
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
    plotPlaceHolder21a = st.empty()
    plotPlaceHolder21b = st.empty()
    plotPlaceHolder21c = st.empty()
    plotPlaceHolder22 = st.empty()
    plotPlaceHolder23 = st.empty()
    plotPlaceHolder24 = st.empty()

#function that displays each graph
def showGraph(df2):
    
    #THE FIRST FILTERED DF WILL DISPLAY, this case happens on first click of "Display vintage"
    dfUsed = df2
    if st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == False:
        dfUsed = df2
    elif st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == True:
        dfUsed = st.session_state['added_df']
    
 
    plot(dfUsed, 'MonthsOnBooks', 'ActiveAccInd', 'vintage', {'ActiveAccInd': 'Active Accounts', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder1, "Active Accounts")
    plot(dfUsed, 'MonthsOnBooks', 'CumlROAAnnual', 'vintage', {'CumlROAAnnual': 'Annualized 12M Rolling ROA', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder1a, "Cumulative ROA Annualized")
    plot(dfUsed, 'MonthsOnBooks', 'cumlPTI', 'vintage', {'cumlPTI': 'Cumulative PreTaxIncome', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder1b, "Cumulative PreTax Income")
    plot(dfUsed, 'MonthsOnBooks', 'EndingReceivable', 'vintage', {'EndingReceivable': 'Gross Receivables', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder1c, "Gross Receivables")
    plot(dfUsed, 'MonthsOnBooks', 'cumlCO', 'vintage', {'cumlCO': 'Cumulative ChargeOffs', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder1d, "Cumulative ChargeOffs")
    plot(dfUsed, 'MonthsOnBooks', 'CumlUnitChargeOffRate', 'vintage', {'CumlUnitChargeOffRate': 'Cumulative Unit Charge-Off Rate', 'MonthsOnBooks': 'Months on Book', 'suffix': '%'}, plotPlaceHolder4, "Cumulative Unit Charge-Off Rate")
    plot(dfUsed, 'MonthsOnBooks', 'UnitChargeOffRate', 'vintage', {'UnitChargeOffRate': 'Unit Charge-Off Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder2, "Unit ChargeOff Rate")
    plot(dfUsed, 'MonthsOnBooks', 'avgReceivable', 'vintage', {'avgReceivable': 'Average Receivable Per Month', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder2, "Average Ending Receivable Per Month")
    plot(dfUsed,'MonthsOnBooks', 'AvgEndBalPerBookedAcct', 'vintage', {'AvgEndBalPerBookedAcct': 'Average Ending Balance Per Month', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder2a, "Average Ending Balance Per Month")
    # plot(dfUsed,'MonthsOnBooks', 'UtilRate', 'vintage', {'UtilRate': 'Utilization Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder2b, "Utilization Rate")

    plot(dfUsed, 'MonthsOnBooks', 'CumlNetChargeOffRate', 'vintage', {'CumlNetChargeOffRate': 'Cumlulative Net Charge-Off Rate', 'MonthsOnBooks': 'Months on Book', 'suffix': '%'}, plotPlaceHolder11, "Cumulative Net Charge-Off Dollar Rate (Before Recoveries)")
    # plot(dfUsed, 'MonthsOnBooks', 'AvgAce2Score', 'vintage', {'AvgAce2Score': 'Average ACE2 Score', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder12, "Average ACE2 Score")
    plot(dfUsed, 'MonthsOnBooks', 'avgBalPActive', 'vintage', {'avgBalPActive': 'Average Balance per Active', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder13, "Average Balance Per Active")
    plot(dfUsed, 'MonthsOnBooks', 'cumlPTIPerBooked', 'vintage', {'cumlPTIPerBooked': 'Cumulative PTI per Booked', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder14, "Cumulative Pre-Tax Income Per Booked")
    #plot(dfUsed, 'MonthsOnBooks', 'cumlGrossRevpBooked', 'vintage', {'cumlGrossRevpBooked': 'Cumlulative Gross Revenue per Booked', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder15, "Cumulative Gross Revenue Per Booked")
    plot(dfUsed, 'MonthsOnBooks', 'cumlFraudRate', 'vintage', {'cumlFraudRate': 'Cumulative Fraud Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder16, "Cumulative Fraud Rate")
    plot(dfUsed, 'MonthsOnBooks', 'AvgPmtPerActive', 'vintage', {'AvgPmtPerActive': 'Average Payment per Active', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder17, "Average Payment Per Active")
    plot(dfUsed, 'MonthsOnBooks', 'cumlPmtsPerBookedAcct', 'vintage', {'cumlPmtsPerBookedAcct': 'Cumulative Payments per Booked Account', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder18, "Cumulative Payments Per Booked Account")
    plot(dfUsed, 'MonthsOnBooks', 'AvgEndBalPerBookedAcct', 'vintage', {'AvgEndBalPerBookedAcct': 'Average Ending Balance per Booked Account', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder19, "Average Ending Balance Per Booked Account")
    plot(dfUsed, 'MonthsOnBooks', 'cumlPurPBookedAcct', 'vintage', {'cumlPurPBookedAcct': 'Cumulative Purchase per Booked Account', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder20, "Cumulative Purchases Per Booked Account")
    plot(dfUsed, 'MonthsOnBooks', 'CumlNetFraudDollRate', 'vintage', {'CumlNetFraudDollRate': 'Cumulative Net Fraud Dollar Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder21, "Cumulative Net Fraud Dollar Rate")
    
    # plot(dfUsed, 'MonthsOnBooks', 'unitRate30+', 'vintage', {'30+ Dollar Rate': '30+ Unit Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder21a, "30+ Unit Rate")
    # plot(dfUsed, 'MonthsOnBooks', 'unitRate60+', 'vintage', {'60+ Dollar Rate': '60+ Unit Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder21b, "60+ Unit Rate")
    # plot(dfUsed, 'MonthsOnBooks', 'unitRate90+', 'vintage', {'90+ Dollar Rate': '90+ Unit Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder21c, "90+ Unit Rate")
    
    plot(dfUsed, 'MonthsOnBooks', '30DollRate', 'vintage', {'30+ Dollar Rate': '30+ Dollar Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder22, "30+ Dollar Rate")
    plot(dfUsed, 'MonthsOnBooks', '60DollRate', 'vintage', {'60+ Dollar Rate': '60+ Dollar Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder23, "60+ Dollar Rate")
    plot(dfUsed, 'MonthsOnBooks', '90DollRate', 'vintage', {'90+ Dollar Rate': '90+ Dollar Rate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder24, "90+ Dollar Rate")
    # plot(dfUsed, 'MonthsOnBooks', 'UtilRate', 'vintage', {'UtilRate': 'UtilizationRate', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder22, "Utilization Rate")
    # plot(dfUsed, 'MonthsOnBooks', 'AvgCLPerActive', 'vintage', {'AvgCLPerActive': 'Average CreditLine Per Active', 'MonthsOnBooks': 'Months on Book'}, plotPlaceHolder23, "Average CreditLine Per Active")

def addDf(result, KPIDF, selList):
    df_add = result 
    unique_id =f"{selList} {st.session_state['add_counter']}" 
    st.session_state['add_counter'] += 1
    df_add['vintage'] = unique_id
    st.session_state.selected_vintages_list.append(unique_id)


    #User has not yet added another dataframe to the initial dataframe, this runs if the Add button is hit for the First time
    if st.session_state['added_df'].empty == True:
        st.session_state['added_df'] = pd.concat([st.session_state['blank_df'], result], axis=0)
        st.session_state['isDfAdded'] = False

        showGraph(result)

    
    #User has added a df before, just take the previous df and concat with new one
    elif st.session_state['added_df'].empty == False:
        st.session_state['added_df'] = pd.concat([st.session_state['added_df'], df_add], axis=0)
        st.session_state['isDfAdded'] = True

        showGraph(result)

   
@st.experimental_fragment
def add_to_main():
    if add:
        #calls filter dataframe function (dfWriterFunction.py file)
        result, KPIDF, KPIDF2 = filter_dataframe(filterDf, selected_vintage, selList)
        #this is how it separates each plot line

        addDf(result, KPIDF, selList)

        with tabs[1]:
            placeHolder = st.empty()
            expanders = addExpander(selList)

            with placeHolder.container():
                st.write(KPIDF)
                csv1 = convert_df(KPIDF)
                downloadButton("KPI", csv1)
                st.write(KPIDF2)

            i = 0               
            for i,  expander in enumerate(expanders):               
                with expander:
                    st.dataframe(st.session_state['added_df'])
                    csv2 = convert_df(st.session_state['added_df'])
                    downloadButton("result", csv2)
                i+=1

def add_4_vintages():

    if add4:
        start_vintage = pd.to_datetime(selected_vintage, format='%Y-%m')
        start_next_vintage = start_vintage + pd.DateOffset(months=1)
        
        # date_range=pd.date_range(start_vintage + pd.DateOffset(months=1), periods=4, freq='M')
        if st.session_state['added_df'].empty == True:
            date_range=pd.date_range(start_vintage, periods=vintageAmt, freq='ME')
        elif st.session_state['added_df'].empty == False:
            if selList in st.session_state.prevSelList:
                date_range=pd.date_range(start_next_vintage, periods=vintageAmt, freq='ME')
            else:
                date_range = date_range=pd.date_range(start_vintage, periods=vintageAmt, freq='ME')
        
        formatted_dates=date_range.strftime('%Y-%m').tolist()


        i=0
        for date in formatted_dates:
            result, KPIDF = filter_dataframe(filterDf, sel_vin=formatted_dates[i])
            selList[0] = formatted_dates[i]

            addDf(result, KPIDF, selList)

            with tabs[1]:
                placeHolder = st.empty()
                expanders = addExpander(selList)
            i+=0

        
        with tabs[1]:
            with placeHolder.container():
                st.write(KPIDF)
                csv1 = convert_df(KPIDF)
                downloadButton("KPI", csv1)
            i=0
            for i,  expander in enumerate(expanders):               
                with expander:
                    st.dataframe(st.session_state['added_df'])
                    csv2 = convert_df(st.session_state['added_df'])
                    downloadButton("result", csv2)
                i+=1 


def add_4_yrs():
    if add4_yrs:
        parsed_date = parse(selected_vintage)

        date_range=pd.date_range(start=parsed_date, periods=4, freq='YS-' + parsed_date.strftime('%b').upper())
        date_range2=pd.date_range(start=parsed_date.strftime('%Y-%m'), periods=vintageAmt, freq=pd.DateOffset(years=1))

        formatted_dates=date_range2.strftime('%Y-%m').tolist()
        j = 0 
        for date in formatted_dates:
            result, KPIDF = filter_dataframe(filterDf, sel_vin=formatted_dates[j])
            selList[0] = formatted_dates[j]

            addDf(result, KPIDF, selList)

            with tabs[1]:
                placeHolder = st.empty()
                expanders = addExpander(selList)

        i=0
        with tabs[1]:
            with placeHolder.container():
                st.write(KPIDF)
                csv1 = convert_df(KPIDF)
                downloadButton("KPI", csv1)
        
            for i,  expander in enumerate(expanders):               
                with expander:
                    st.dataframe(st.session_state['added_df'])
                    csv2 = convert_df(st.session_state['added_df'])
                    downloadButton("result", csv2)
                i+=1


def clear_from_main():
        if clear:
            st.session_state.selected_vintages_list.clear()
            st.session_state['add_counter'] = 1
            df_clear = df.loc[(df['vintage'] == None)
                                    & (df['FirstSecond'] == None)
                                    & (df['Branding'] == None)
                                    & (df['AccountNumber'] == None)
                                    & (df['Subchannel'] == None)
                                    & (df['Acquisitions'] == None)
                                    & (df['Source'] == None)
                                    & (df['Association'] == None)
                                    & (df['AnnualFeeGroup'] == None)
                                    & (df['OriginalCreditLine'] == None)]
            st.session_state['added_df'] = pd.concat([st.session_state['blank_df'], df_clear], axis=0)
            st.session_state['KPI_DF'] = df_clear 
            st.session_state['counter'] = 0
            st.session_state.csvCounter = 1
            st.session_state.expanderAmt = 0
            st.session_state.expanderList = []
            st.session_state['added_df'] = pd.concat([st.session_state['blank_df'], df_clear], axis=0)

    


if __name__ == "__main__":
    # addDf()
    add_to_main()
    clear_from_main()
    add_4_vintages()
    add_4_yrs()    

def remove_selected_vintage(vintage_to_remove):
        
    if f"{vintage_to_remove}" in st.session_state['added_df']['vintage'].values:
        df = st.session_state['added_df'].drop(st.session_state['added_df'][st.session_state['added_df']['vintage'] ==  f"{vintage_to_remove}"].index)
        st.session_state['added_df'] = df
        st.session_state['isDfAdded'] = not st.session_state['added_df'].empty
        st.session_state.selected_vintages_list.remove(vintage_to_remove)
        if st.session_state['added_df'].empty:
            st.session_state['isDfAdded'] = False
        st.experimental_rerun()
    
  
#with col3000:          
    for i, vintage in enumerate(st.session_state.selected_vintages_list):
        if st.button(f"Remove {vintage}", key=f"remove_{i}"):
            remove_selected_vintage(vintage)
            
