import pandas as pd
import streamlit as st
import numpy as np
from math import trunc
from datetime import datetime
# df=pd.read_parquet(r"C:\Users\amalik\ProjectDash\Data\dashbase.parquet")
# df=pd.read_parquet(r"C:\Users\cmacedo\Data\vcr_base_24.parquet")
if 'KPI_DF' not in st.session_state:
     st.session_state['KPI_DF'] = pd.DataFrame()
 
if 'counter' not in st.session_state:
    st.session_state['counter'] = 1
 
def convert_date(date_str):
   date_obj = datetime.strptime(date_str, "%d%b%Y")
   return date_obj.strftime("%b-%y")
 
def formatPct(pivTable, list):
    for col in list:
        if col in pivTable.index and not pivTable.loc[col].empty:
            pivTable.loc[col] = pivTable.loc[col].apply(lambda x: '{:.1%}'.format(x))
 
    return pivTable
 
def formatInt(pivTable, list):
    for col in list:
        if col in pivTable.index and not pivTable.loc[col].empty:
            pivTable.loc[col] = pivTable.loc[col].apply(lambda x:f'{int(x):,}'.format(x))
    return pivTable
 
def formatFloat(pivTable, list):
    for col in list:
        if col in pivTable.index and not pivTable.loc[col].empty:
            pivTable.loc[col] = pivTable.loc[col].apply(lambda x: '{:.2f}'.format(x))
 
    return pivTable
 
def filter_dataframe(filtered_df, sel_vin = ' '):
    # #conditions is for the actual filtering, added selections is to display all the choices on legend of graph
    # #if selection is not empty or all, add it to the list of conditions
    filtered_df = filtered_df[filtered_df['Vintage'] == sel_vin]
 
    #bucketCounts
    filtered_df['Current'] = np.where(filtered_df['dimBucketID'] == 0, filtered_df['ActiveAccountIndicator'], 0)
    filtered_df['5-Day'] = np.where(filtered_df['dimBucketID'] == 5, filtered_df['DimbuckIDcount'], 0)
    filtered_df['thirtyCount'] = np.where(filtered_df['dimBucketID'] == 30, filtered_df['DimbuckIDcount'], 0)
    filtered_df['sixtyCount'] = np.where(filtered_df['dimBucketID'] == 60, filtered_df['DimbuckIDcount'], 0)
    filtered_df['ninetyCount'] = np.where(filtered_df['dimBucketID'] == 90, filtered_df['DimbuckIDcount'], 0)
    filtered_df['120Count'] = np.where(filtered_df['dimBucketID'] == 120, filtered_df['DimbuckIDcount'], 0)
    filtered_df['150plus'] = np.where(filtered_df['dimBucketID'] >= 150, filtered_df['DimbuckIDcount'], 0)
 
    #unit rates
    filtered_df['thirtyPlus'] = np.where(filtered_df['dimBucketID'] >= 30, filtered_df['DimbuckIDcount'], 0)
    filtered_df['sixtyPlus'] = np.where(filtered_df['dimBucketID'] >= 60, filtered_df['DimbuckIDcount'], 0)
    filtered_df['ninetyPlus'] = np.where(filtered_df['dimBucketID'] >= 90, filtered_df['DimbuckIDcount'], 0)
 
    #bucketCounts
    filtered_df['currentReceivable'] = np.where(filtered_df['dimBucketID'] == 0, filtered_df['EndingReceivable'], 0)
    filtered_df['fivedayReceivable'] = np.where(filtered_df['dimBucketID'] == 5, filtered_df['EndingReceivable'], 0)
    filtered_df['30dayReceivable'] = np.where(filtered_df['dimBucketID'] == 30, filtered_df['EndingReceivable'], 0)
    filtered_df['60dayReceivable'] = np.where(filtered_df['dimBucketID'] == 60, filtered_df['EndingReceivable'], 0)
    filtered_df['90dayReceivable'] = np.where(filtered_df['dimBucketID'] == 90, filtered_df['EndingReceivable'], 0)
    filtered_df['120dayReceivable'] = np.where(filtered_df['dimBucketID'] == 120, filtered_df['EndingReceivable'], 0)
    filtered_df['150dayReceivable'] = np.where(filtered_df['dimBucketID'] == 150, filtered_df['EndingReceivable'], 0)
    
 
        #aggregates data by chosen vintage and by MOB
    result = filtered_df.groupby([ 'Vintage', 'MonthsOnBooks', 'ReportingDate' ]).agg(
          NewAccInd = ('NewAccountIndicator', 'sum')
        , ActiveAccInd = ('ActiveAccountIndicator', 'sum')
        , TotalPayments = ('TotalPayments', 'sum')
        , TotalPaymentsAdj = ('TotalPaymentAdjs', 'sum')
        , TotalNetSales = ('TotalNetSales', 'sum')
        , Ace2 = ('Ace2Score', 'sum')
        , Ace2Ind = ('Ace2ScoreIndicator', 'sum')
        , EndingReceivable=('EndingReceivable', 'sum')
        , CreditLine = ('CreditLine', 'sum')
        , PreTaxIncome=('PTI', 'sum')
        , ChargeOffs=('ChargeOffs', 'sum')
        , Unwinds = ('Unwinds', 'sum')
        , ChargeOffPrcbl = ('ChargeOffPrincAmt', 'sum')
        , FraudAmt = ('FraudAmount', 'sum')
        , Fraud = ('FraudCount', 'sum')
        , GrsRev = ('GrossRevenue', 'sum')
        , TotalFinCharge = ('TotalFinanceCharges', 'sum')
        , Current = ('Current', 'sum')
        , fiveDay = ('5-Day', 'sum')
        , ThirtyCount = ('thirtyCount', 'sum')
        , SixtyCount = ('sixtyCount', 'sum')
        , NinetyCount = ('ninetyCount', 'sum')
        , Count120 = ('120Count', 'sum')
        , Count150 = ('150plus', 'sum')
        , ThirtyPlusCount = ('thirtyPlus', 'sum')
        , SixtyPlusCount = ('sixtyPlus', 'sum')
        , NinetyPlusCount = ('ninetyPlus', 'sum')
        , currRcvbl = ('currentReceivable', 'sum')
        , fiveRcvbl = ('fivedayReceivable', 'sum')
        , thirtyRcvbl = ('30dayReceivable', 'sum')
        , sixtyRcvbl = ('60dayReceivable', 'sum')
        , ninetyRcvbl = ('90dayReceivable', 'sum')
        , oneTwentyRcvbl = ('120dayReceivable', 'sum')
        , oneFiftyRcvbl = ('150dayReceivable', 'sum')).reset_index()
    
  
    result['Booked Accounts'] = result['NewAccInd']
    result['Active Accounts - End of Period'] = result['ActiveAccInd']
    result['5-Day'] = result['fiveDay']
    result['30-Day'] = result['ThirtyCount']
    result['60-Day'] = result['SixtyCount']
    result['90-Day'] = result['NinetyCount']
    result['120-Day'] = result['Count120']
    result['150-Day+'] = result['Count150']
    result['Current Dollar'] = result['currRcvbl']
    result['5-Day Dollar'] = result['fiveRcvbl']
    result['30-Day Dollar'] = result['thirtyRcvbl']
    result['60-Day Dollar'] = result['sixtyRcvbl']
    result['90-Day Dollar'] = result['ninetyRcvbl']
    result['120-Day Dollar'] = result['oneTwentyRcvbl']
    result['150-Day+ Dollar'] = result['oneFiftyRcvbl']
    result['Charged-Off Accounts'] = result['ChargeOffs']   
    result['Pre-Tax Income'] = result['PreTaxIncome']
    result['Gross Revenue'] = result['GrsRev']
 
    
    result['ChargeOff+BK'] = result['Charged-Off Accounts'] - result['Fraud']
    result['ChargeOffRate'] = result['ChargeOff+BK'] / result['Active Accounts - End of Period']
    result['Attrition'] = result['Active Accounts - End of Period'].shift(1, fill_value = 0) + result['Booked Accounts'] 
    result['Attrition'] = result['Attrition'] - result['ChargeOff+BK'] - result['Active Accounts - End of Period'] 
    result['Attrition Rate'] = result['Attrition'] / result['Active Accounts - End of Period']
 
    result['30+ Unit Rate'] = result["ThirtyPlusCount"] / result["Active Accounts - End of Period"] 
    result['60+ Unit Rate'] = result["SixtyPlusCount"] / result["Active Accounts - End of Period"] 
    result['90+ Unit Rate'] = result["NinetyPlusCount"] / result["Active Accounts - End of Period"]
    
    result['30+UnitM3'] = np.where(result['MonthsOnBooks'] == 3, result['30+ Unit Rate'], None)
    result['30+UnitM4'] = np.where(result['MonthsOnBooks'] == 4, result['30+ Unit Rate'], None)
 
    result['30+rcvbl'] = result['thirtyRcvbl'] + result['sixtyRcvbl'] + result['ninetyRcvbl'] + result['oneTwentyRcvbl'] + result['oneFiftyRcvbl']
    result['60+rcvbl'] = result['sixtyRcvbl'] + result['ninetyRcvbl'] + result['oneTwentyRcvbl'] + result['oneFiftyRcvbl']
    result['90+rcvbl'] = result['ninetyRcvbl'] + result['oneTwentyRcvbl'] + result['oneFiftyRcvbl']
 
    result['$ 30+ Rate'] = result['30+rcvbl'] / result['EndingReceivable']
    result['$ 60+ Rate'] = result['60+rcvbl'] / result['EndingReceivable']
    result['$ 90+ Rate'] = result['90+rcvbl'] / result['EndingReceivable']
 
    result['prevCurrent'] = result['Current'].shift(1)
    result['Curr-5'] = result["5-Day"] / result['prevCurrent']
 
    result['prevFive'] = result['5-Day'].shift(1)
    result['5-30'] = result['30-Day'] / result['prevFive']
 
    result['prevThirty'] = result['30-Day'].shift(1)
    result['30-60'] = result['60-Day'] / result['prevThirty']
    
    result['prevSixty'] = result['60-Day'].shift(1)
    result['60-90'] = result['90-Day'] / result['prevSixty']
 
    result['prevNinety'] = result['90-Day'].shift(1)
    result['90-120'] = result['120-Day'] / result['prevNinety']
 
    result['prev120'] = result['120-Day'].shift(1)
    result['120-150+'] = result['150-Day+'] / result['prev120']
 
    result['prev150'] = result['150-Day+'].shift(1)
    result['150+ to C/O'] = result['Charged-Off Accounts'] / result['prev150']
 
    result['$ Net Charge-Off Rate before Recoveries'] = result["ChargeOffPrcbl"] - result["FraudAmt"]
    result['Net Payments'] = result['TotalPayments'] + result['TotalPaymentsAdj']
    
    #getting cumulative sums of all data
    result['cumlNewAcc'] = result.groupby('Vintage')['Booked Accounts'].cumsum()
    result['cumlActiveAcc'] = result.groupby('Vintage')['Active Accounts - End of Period'].cumsum()
    result['Cumul. Pre-Tax Income'] = result.groupby('Vintage')['Pre-Tax Income'].cumsum()
    result['cumlER'] = result.groupby('Vintage')['EndingReceivable'].cumsum()
    result['Cumulative Charge Offs'] = result.groupby('Vintage')['Charged-Off Accounts'].cumsum()
    result['Cumulative Unwinds'] = result.groupby('Vintage')['Unwinds'].cumsum()
    result['Cumul. $ Net Charge-Off Rate before Recoveries'] = result.groupby('Vintage')['$ Net Charge-Off Rate before Recoveries'].cumsum()
    result['cumlNetPayments'] = result.groupby('Vintage')['Net Payments'].cumsum()
    result['cumlTtlNetSales'] = result.groupby('Vintage')['TotalNetSales'].cumsum()
    result['cumlFraud'] = result.groupby('Vintage')['Fraud'].cumsum()
    result['cumlGrsRev'] = result.groupby('Vintage')['Gross Revenue'].cumsum()
    result['Cumul. Fraud'] = result.groupby('Vintage')['FraudAmt'].cumsum()
    result['Cumul. Total Finance Charges'] = result.groupby('Vintage')['TotalFinCharge'].cumsum()
 
    result['avgActives'] = result['cumlActiveAcc'] / result['MonthsOnBooks']
    #result['Average Receivable'] = np.where(result['cumlER'] == 0, 0, result['cumlER'] / result['MonthsOnBooks'])
    result['Average Receivable'] = result['cumlER'] / result['MonthsOnBooks']
    result['Cumul. PTI  -  Per Booked Account'] = result['Cumul. Pre-Tax Income'] / result['cumlNewAcc']
    #calculations for more other graphs, creates columns in dataframe for each new 
    result['MonthsOnBooks'] = pd.to_numeric(result['MonthsOnBooks'])
    #running calculations for plotting
 
    # #ROA CALCULATIONS
    result['Cumulative ROA'] = ((result['Pre-Tax Income'] / result['EndingReceivable']) * 12)
    result['PTIAnnualized'] = np.where(result['Pre-Tax Income'] == 0, 0, result['Cumul. Pre-Tax Income'] /(result['MonthsOnBooks']))
    result['Cumulative ROA - Annualized'] = result['Cumul. Pre-Tax Income'] / (result['Average Receivable']) / (result['MonthsOnBooks'] / 12)
    # result['Cumulative ROA - Annualized'] = np.where(result['Average Receivable'] == 0, 0,( result['PTIAnnualized'] / (result['Average Receivable']) / (result['MonthsOnBooks'] / 12)))
 
    #CHARGE OFF CALCULATIONS
    result['Unit Charge-Off Rate'] = np.where(result['Charged-Off Accounts'] == 0, 0, (result['Charged-Off Accounts'] / result['Active Accounts - End of Period']))
    result['Cumul. Unit Charge-Off Rate'] = np.where(result['Cumulative Charge Offs'] == 0,0, (result['Cumulative Charge Offs'] / (result['cumlNewAcc'] - result['Cumulative Unwinds'])))
 
    #NetChargeOffRate
    result['Cumul. Net Charge Off Rate'] = (result['Cumul. $ Net Charge-Off Rate before Recoveries'] / result['Average Receivable'])
    result['Cumul. Payments Per Booked Account'] = result['cumlNetPayments'] / result['cumlNewAcc']
 
    #ENDING BAL
    result['Average End Balance per Booked Account'] = result['EndingReceivable'] / result['cumlNewAcc']
    result['Cumul. Purchases Per Booked Account'] = result['cumlTtlNetSales'] / result['cumlNewAcc']
    result['Average ACE Score'] = result['Ace2'] / result['Ace2Ind']
 
    result['Average Balance per Active'] = result['EndingReceivable'] / result['Active Accounts - End of Period']
 
    result['Cumul. Gross Revenue Per Booked'] = result['cumlGrsRev'] / result['cumlNewAcc']
 
    result['Cumulative Fraud Rate'] = result['cumlFraud'] / (result['cumlNewAcc'] - result['Cumulative Unwinds'])
 
    result['Average Payment Per Active'] = result['cumlNetPayments'] / result['cumlActiveAcc']
 
    result['$ Net Fraud Rate'] = result['Cumul. Fraud'] / result['Average Receivable']
    # result['UtilRate'] = result['EndingReceivable'] / result['CreditLine'] 
 
    # result['AvgCLPerActive'] = result['CreditLine'] / result['Active Accounts - End of Period']
    result['Cumul. Finance Charge Per Booked '] = result['Cumul. Total Finance Charges'] / result['cumlNewAcc']
    # Convert YearMonth to datetime for sorting
    result['YearMonth'] = result['ReportingDate'].apply(convert_date)
    result['YearMonth'] = pd.to_datetime(result['YearMonth'], format='%b-%y')
    result['YearMonth'] = pd.to_datetime(result['YearMonth'], format='%b-%y')
    
    
 
    #doesn't have fraudrate, unwindrate, percent active and active account indicator doesn't match spreadsheet, 
    accMelt = pd.melt(result, id_vars=['YearMonth'], value_vars=['Booked Accounts', 'Average ACE Score', 'Cumulative Unwinds', 'Active Accounts - End of Period', 'Curr-5', 
    '5-30', '30-60','60-90', '90-120','120-150+', '150+ to C/O', '30+ Unit Rate', '60+ Unit Rate', '90+ Unit Rate',
    '150+ to C/O',  'Unit Charge-Off Rate','Cumul. Unit Charge-Off Rate','Attrition Rate', 'Cumulative Fraud Rate' ], var_name='Account Metrics', value_name='Met')
 
    accPiv = accMelt.pivot_table(index='Account Metrics', columns='YearMonth', values='Met')
 
    accDesiredOrder = ['Booked Accounts', 'Average ACE Score', 'Cumulative Unwinds', 'Active Accounts - End of Period', 'Curr-5', 
    '5-30', '30-60','60-90', '90-120','120-150+', '150+ to C/O', '30+ Unit Rate', '60+ Unit Rate', '90+ Unit Rate',
    'Unit Charge-Off Rate','Cumul. Unit Charge-Off Rate','Attrition Rate', 'Cumulative Fraud Rate']
 
    accPiv = accPiv.reindex(accDesiredOrder)
 
    accPivToFormatFloat = ['Booked Accounts', 'Average ACE Score', 'Cumulative Unwinds', 'Active Accounts - End of Period']
    accPivColtoFormatPct = ['Curr-5','5-30', '30-60', '60-90','90-120', '120-150+','150+ to C/O',
                        '30+ Unit Rate', '60+ Unit Rate','90+ Unit Rate','Unit Charge-Off Rate', 'Cumul. Unit Charge-Off Rate', 'Attrition Rate', 'Cumulative Fraud Rate']
    
    accPiv = formatPct(accPiv, accPivColtoFormatPct)
    accPiv = formatInt(accPiv, accPivToFormatFloat)
    accPiv.replace(regex = "nan%", value = "", inplace = True)
    accPiv.replace(regex = "inf%", value = "", inplace = True)
  
    balPivColToFormatPercent =[ '$ 30+ Rate','$ 60+ Rate','$ 90+ Rate','Cumulative Fraud Rate','Cumul. Net Charge Off Rate', '$ Net Fraud Rate']
    balpivColtoFormatFloat =   ['Average End Balance per Booked Account','Average Balance per Active']
    balPivColtoFormatInt = ['EndingReceivable','FraudAmt', 'Cumul. Fraud']
    
 
    balMelt = pd.melt(result, id_vars=['YearMonth'], value_vars=['EndingReceivable','Average End Balance per Booked Account', 'Average Balance per Active', 
                                                                 '$ 30+ Rate', '$ 60+ Rate', '$ 90+ Rate', 'Cumul. Net Charge Off Rate',
                                                                 'FraudAmt', 'Cumul. Fraud', 'Cumulative Fraud Rate', '$ Net Fraud Rate'], var_name='Balance Metrics', value_name='Met')
    
    balPiv = balMelt.pivot_table(index='Balance Metrics', columns='YearMonth', values='Met')
 
    balPiv = formatPct(balPiv, balPivColToFormatPercent)
    balPiv = formatFloat(balPiv, balpivColtoFormatFloat)
    balPiv = formatInt(balPiv, balPivColtoFormatInt)
    
 
    chargeMelt = pd.melt(result, id_vars=['YearMonth'], value_vars=['Charged-Off Accounts', '$ Net Charge-Off Rate before Recoveries', 'ChargeOffPrcbl', 'Cumul. $ Net Charge-Off Rate before Recoveries','Unit Charge-Off Rate', 'Cumul. Unit Charge-Off Rate'], var_name='ChargeOff Metrics', value_name='Date')
    chargePiv = chargeMelt.pivot_table(index='ChargeOff Metrics', columns='YearMonth', values='Date')
    chargeMeltIntFormat = ['Charged-Off Accounts', '$ Net Charge-Off Rate before Recoveries', 'ChargeOffPrcbl', 'Cumul. $ Net Charge-Off Rate before Recoveries']
    chargeMeltPctFormat = ['Unit Charge-Off Rate', 'Cumul. Unit Charge-Off Rate']
    
    chargePiv = formatInt(chargePiv, chargeMeltIntFormat)
    chargePiv = formatPct(chargePiv, chargeMeltPctFormat)
    
 
    profitMelt = pd.melt(result, id_vars=['YearMonth'], value_vars=['Cumul. Total Finance Charges', 'Gross Revenue', 'Pre-Tax Income', 'Cumul. Pre-Tax Income', 'Cumulative ROA', 'Cumulative ROA - Annualized', 'Cumul. PTI  -  Per Booked Account', 'Net Payments'
                                                                    ,'Cumul. Payments Per Booked Account',  'Cumul. Purchases Per Booked Account', 'Cumul. Gross Revenue Per Booked', 'Average Payment Per Active', 'Cumul. Finance Charge Per Booked '],
                                                                      var_name='Profitability Metrics', value_name='Date')
    profitPiv = profitMelt.pivot_table(index='Profitability Metrics', columns='YearMonth', values='Date')
    profitPivFloatCharges = ['Cumul. PTI  -  Per Booked Account', 'Cumul. Payments Per Booked Account',  'Cumul. Purchases Per Booked Account'
                             , 'Cumul. Gross Revenue Per Booked', 'Average Payment Per Active', 'Cumul. Finance Charge Per Booked ']
    profitPivPct = ['Cumulative ROA', 'Cumulative ROA - Annualized']
    profitPivInt = ['Cumul. Total Finance Charges', 'Gross Revenue', 'Pre-Tax Income', 'Cumul. Pre-Tax Income' , 'Net Payments']
 
    profitPiv = formatInt(profitPiv, profitPivInt)
    profitPiv = formatFloat(profitPiv, profitPivFloatCharges)
    profitPiv = formatPct(profitPiv, profitPivPct)
 
    balPiv.columns = balPiv.columns.get_level_values('YearMonth').strftime('%b-%y')
    chargePiv.columns = chargePiv.columns.get_level_values('YearMonth').strftime('%b-%y')
    profitPiv.columns = profitPiv.columns.get_level_values('YearMonth').strftime('%b-%y')
    accPiv.columns = accPiv.columns.get_level_values('YearMonth').strftime('%b-%y')
    
    piecedDF = pd.concat([accPiv,balPiv,chargePiv,profitPiv], axis=0, ignore_index=False)
 
    #KPI Chart
    result['Cuml. ROA at M3'] = np.where(result['MonthsOnBooks'] == 3, result['Cumulative ROA'], None)
    result['Cuml. ROA at M6'] = np.where(result['MonthsOnBooks'] == 6, result['Cumulative ROA'], None)
    result['Cuml. ROA at M12'] = np.where(result['MonthsOnBooks'] == 12, result['Cumulative ROA'], None)
    result['Cuml. ROA at M24'] = np.where(result['MonthsOnBooks'] == 24, result['Cumulative ROA'], None)
    result['Cuml. Unit CO at M12'] = np.where(result['MonthsOnBooks'] == 12, result['Cumul. Unit Charge-Off Rate'], None)
    result['Cuml. Unit CO at M24'] = np.where(result['MonthsOnBooks'] == 24, result['Cumul. Unit Charge-Off Rate'], None)
    result['Cuml $ CO at M12'] = np.where(result['MonthsOnBooks'] == 12, result['ChargeOffPrcbl'], None)
    result['Cuml $ CO at M24'] = np.where(result['MonthsOnBooks'] == 24, result['ChargeOffPrcbl'], None)
    result['Cuml. PTI Per Booked at M12'] = np.where(result['MonthsOnBooks'] == 12, result['Cumul. PTI  -  Per Booked Account'], None)
    result['Cuml. PTI Per Booked at M24'] = np.where(result['MonthsOnBooks'] == 24, result['Cumul. PTI  -  Per Booked Account'], None)
 
   
    KPIMelt = pd.melt(result, id_vars=["Vintage"], value_vars=['Cuml. ROA at M3', 'Cuml. ROA at M6', 'Cuml. ROA at M12', 'Cuml. ROA at M24', 
                                                               'Cuml. Unit CO at M12', 'Cuml. Unit CO at M24', 'Cuml $ CO at M12',
                                                                'Cuml $ CO at M24', 'Cuml. PTI Per Booked at M12', 'Cuml. PTI Per Booked at M24'], var_name='Metrics', value_name='Date')
 
    KPIPiv = KPIMelt.pivot_table(index='Metrics', columns="Vintage", values="Date")
 
    desiredOrder = ['Cuml. ROA at M3', 'Cuml. ROA at M6', 'Cuml. ROA at M12', 'Cuml. ROA at M24', 
                    'Cuml. Unit CO at M12', 'Cuml. Unit CO at M24', 'Cuml $ CO at M12',
                    'Cuml $ CO at M24', 'Cuml. PTI Per Booked at M12', 'Cuml. PTI Per Booked at M24']
    
    columns_to_format_percent = ['Cuml. ROA at M3', 'Cuml. ROA at M6', 'Cuml. ROA at M12', 'Cuml. ROA at M24', 
                    'Cuml. Unit CO at M12', 'Cuml. Unit CO at M24']
    KPIPivInt = ['Cuml $ CO at M12', 'Cuml $ CO at M24']
    columns_to_format_decimal = ['Cuml. PTI Per Booked at M12', 'Cuml. PTI Per Booked at M24']
    # Loop over percentage columns
    KPIPiv = formatInt(KPIPiv, KPIPivInt)
    KPIPiv = formatPct(KPIPiv, columns_to_format_percent)
    KPIPiv = formatFloat(KPIPiv, columns_to_format_decimal) 
    # Reindex the pivot table to the desired order
    KPIPiv = KPIPiv.reindex(desiredOrder)
 
    colList = KPIPiv.columns.tolist()
    if len(colList) > 0:
        KPIPivCol = KPIPiv.columns[0] 
 
        if st.session_state['KPI_DF'].empty == False:
            if KPIPivCol in st.session_state['KPI_DF'].columns:
                newName=f"{KPIPivCol} {st.session_state['counter']}"
                st.session_state['counter']+=1
                KPIPiv.columns = [newName]
            else:
                newName = KPIPivCol
 
    compDF = pd.melt(result, id_vars=["MonthsOnBooks"], value_vars=['Cumul. Gross Revenue Per Booked', 'Cumul. PTI  -  Per Booked Account','Average End Balance per Booked Account', 'Average Balance per Active'
                                                                    , 'Cumul. Purchases Per Booked Account', 'Average ACE Score', 'Cumulative ROA'], var_name='Metrics', value_name='Comps')
    compPiv = compDF.pivot_table(index='Metrics', columns="MonthsOnBooks", values="Comps")
 
    if st.session_state['KPI_DF'].empty:
       st.session_state['KPI_DF'] = KPIPiv
    else:
        st.session_state['KPI_DF'] = pd.concat([st.session_state['KPI_DF'], KPIPiv], axis=1)
 
    if result.empty == True:
        accPiv = pd.DataFrame()
        balPiv = pd.DataFrame()
        chargePiv = pd.DataFrame()
        profitPiv = pd.DataFrame()
        profitPiv = pd.DataFrame()
        compPiv = pd.DataFrame()
 
    return result, st.session_state['KPI_DF'], accPiv, balPiv, chargePiv, profitPiv, compPiv,piecedDF
 
 
