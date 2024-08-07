import pandas as pd
import streamlit as st
import numpy as np
from collections import deque

# df=pd.read_parquet(r"C:\Users\cmacedo\Data\vcr_base_24.parquet")
# df=pd.read_parquet(r"C:\Users\cmacedo\Data\test.parquet")
df=pd.read_parquet(r"C:\Users\cmacedo\Data\datedDf2.parquet")

def filter_dataframe(df, sel_group = ' ', sel_vin = ' ', sel_fs = ' ', sel_brand = ' ', sel_pg = ' ', sel_assc = ' ', 
            sel_mob = ' ', sel_channel = ' ', sel_source = ' ', sel_sub = ' ', 
           sel_acq = ' ', sel_ogcl = ' ', sel_annfee = ' '):
    
    #conditions is for the actual filtering, added selections is to display all the choices on legend of graph
    conditions = []
    addedSelections = []
    #if selection is not empty or all, add it to the list of conditions
    if sel_group != ' ' and sel_group != 'All':
        conditions.append(df['TimeonBooks'] == sel_group)
        addedSelections.append(sel_group)
    
    if sel_vin != ' ' and sel_vin != 'All':
        conditions.append(df['Vintage'] == sel_vin)
        addedSelections.append(sel_vin)

    if sel_fs != ' ' and sel_fs != 'All':
        conditions.append(df['AccountNumber'] == sel_fs)
        addedSelections.append(sel_fs)

    if sel_brand != ' ' and sel_brand != 'All':
        conditions.append(df['Branding'] == sel_brand)
        addedSelections.append(sel_brand)

    if sel_pg != ' ' and sel_pg != 'All':
        conditions.append(df['ProductGroup'] == sel_pg)
        addedSelections.append(sel_pg) 

    if sel_assc != ' ' and sel_assc != 'All':
        conditions.append(df['Association'] == sel_assc)
        addedSelections.append(sel_assc)    

    if sel_channel != ' ' and sel_channel != 'All':
        conditions.append(df['Channel'] == sel_channel)
        addedSelections.append(sel_channel)

    if sel_source != ' ' and sel_source != 'All':
        conditions.append(df['dimBucketID'] == sel_source)
        addedSelections.append(sel_source)

    if sel_sub != ' ' and sel_sub != 'All':
        conditions.append(df['RetainedBusiness'] == sel_sub)
        addedSelections.append(sel_sub)

    if sel_acq != ' ' and sel_acq != 'All':
        conditions.append(df['ProductGroup'] == sel_acq)
        addedSelections.append(sel_acq)

    if sel_ogcl != ' ' and sel_ogcl != 'All':
        conditions.append(df['OriginalCreditLineRange'] == sel_ogcl)
        addedSelections.append(sel_ogcl)
        
    if sel_annfee != ' ' and sel_annfee != 'All':
        conditions.append(df['AnnualFeeGroupGroup'] == sel_annfee)
        addedSelections.append(sel_annfee)

    if sel_mob != ' ' and sel_mob != 'All':
        addedSelections.append(sel_mob)

    # Combine all conditions using the & operator, filters actual dataframe
    if conditions:
        combined_conditions = conditions[0]

        for condition in conditions[1:]:
            combined_conditions &= condition

        filtered_df = df[combined_conditions]

    else:
        filtered_df = df
    
    # filtered_df['Months'] = range(1, len(filtered_df) + 1)
    
    # filtered_df = filtered_df.sort_values(by=['Month'], ascending=[True])
    # result = filtered_df.groupby(['Vintage', 'Month']).agg(
    
    # filtered_df= filtered_df.groupby(['Vintage', 'ReportingDate'])
    # filtered_df['Months'] = range(1, len(filtered_df) + 1)
    # filtered_df = filtered_df.sort_values(by=['Months'], ascending=[True])
    filtered_df = filtered_df.sort_values(by=['Year', 'Month'], ascending=[True, True])
    # filtered_df = filtered_df.sort_values(by=['ReportingDate'], ascending=[True])
    # result['MOBS'] = result.index+1
    # filtered_df['MOBS'] = filtered_df.index+1
    filtered_df['Current'] = np.where(filtered_df['dimBucketID'] == 0, filtered_df['ActiveAccountIndicator'], 0)
    filtered_df['Five'] = np.where(filtered_df['dimBucketID'] == 5, filtered_df['ActiveAccountIndicator'], 0)
    filtered_df['Thirty'] = np.where(filtered_df['dimBucketID'] == 30, filtered_df['ActiveAccountIndicator'], 0)
    filtered_df['Sixty'] = np.where(filtered_df['dimBucketID'] == 60, filtered_df['ActiveAccountIndicator'], 0)
    filtered_df['Ninety'] = np.where(filtered_df['dimBucketID'] == 60, filtered_df['ActiveAccountIndicator'], 0)
    

        
    result = filtered_df.groupby(['Year', 'Month', 'Vintage']).agg(
        
        # Months = ('Vintage', 'count')
         NewAccInd = ('NewAccountIndicator', 'sum')
        , ActiveAccInd = ('ActiveAccountIndicator', 'sum')
        , TotalPayments = ('TotalPayments', 'sum')
        , TotalPaymentsAdj = ('TotalPaymentAdjustments', 'sum')
        , TotalNetSales = ('TotalNetSales', 'sum')
        # , Ace2 = ('Ace2Score', 'sum')
        # , Ace2Ind = ('Ace2ScoreIndicator', 'sum')
        , EndingReceivable=('EndingReceivable', 'sum')
        , CreditLine = ('ActiveCreditLine', 'sum')
        , PreTaxIncome=('PreTaxIncome', 'sum')
        , ChargeOffs=('ChargeOffIndicator', 'sum')
        , ChargeOffPrcbl = ('ChargeOffPrincipalAmount', 'sum')
        , FraudAmt = ('FraudAmount', 'sum')
        , Unwinds = ('UnwindIndicator', 'sum')
        , ChargeOffPr_NoFraud = ('ChargeOffPrincipalAmountNoFraud', 'sum')
        , FraudCnt = ('FraudCount', 'sum')
        , GrsRev = ('GrossRevenue', 'sum')
        , Curr = ('Current', 'sum')
        , Fiv = ('Five', 'sum')
        , TotalFinCharge = ('TotalFinanceCharges', 'sum')).reset_index()
    
    # result = result.sort_values(by=['MOBS'], ascending=[True])
    result['MOBS'] = result.index+1
    
    
    
    
    
    result = result.sort_values(by=['Year', 'Month', 'Vintage'], ascending=[True, True, True])
    
    result['C-5'] = np.where(result['Fiv'] == 0, 0, result['Fiv'] / result['Curr'].shift(1))
    
    result['ChargeOffCt_NoFraud'] = result['ChargeOffs'] - result['FraudCnt']
    result['netPayments'] = result['TotalPayments'] + result['TotalPaymentsAdj']
    #getting cumulative sums of all data
    result['cumlNewAcc'] = result.groupby('Vintage')['NewAccInd'].cumsum()
    result['cumlActiveAcc'] = result.groupby('Vintage')['ActiveAccInd'].cumsum()
    result['cumlPTI'] = result.groupby('Vintage')['PreTaxIncome'].cumsum()
    result['cumlER'] = result.groupby('Vintage')['EndingReceivable'].cumsum()
    result['cumlCO'] = result.groupby('Vintage')['ChargeOffs'].cumsum()
    result['cumlCONoFraud'] = result.groupby('Vintage')['ChargeOffCt_NoFraud'].cumsum()
    result['cumlUnwind'] = result.groupby('Vintage')['Unwinds'].cumsum()
    result['CumlNetChargeOffs'] = result.groupby('Vintage')['ChargeOffPr_NoFraud'].cumsum()
    result['cumlNetPayments'] = result.groupby('Vintage')['netPayments'].cumsum()
    result['cumlTtlNetSales'] = result.groupby('Vintage')['TotalNetSales'].cumsum()
    result['cumlFraudCnt'] = result.groupby('Vintage')['FraudCnt'].cumsum()
    result['cumlGrsRev'] = result.groupby('Vintage')['GrsRev'].cumsum()
    result['cumlFraudAmt'] = result.groupby('Vintage')['FraudAmt'].cumsum()
    result['cumlTtlFinCharge'] = result.groupby('Vintage')['TotalFinCharge'].cumsum()
    

    result['avgActives'] = result['cumlActiveAcc'] / result['MOBS']
    result['avgReceivable'] = result['cumlER'] / result['MOBS']

    result['avgReceivable2'] = result['cumlER'] / result['Month']

    last_12_months_pti = deque(maxlen=12)
    last_12_months_er = deque(maxlen=12)
    
    cumlPTI_list = []
    cumlER_list = []
    cumlER2_list = []
    annualized12mrollROA_list = []
    
    for index, row in result.iterrows():
        last_12_months_pti.append(row['PreTaxIncome'])
        
        last_12_months_er.append(row['EndingReceivable'])
        
        r_cumlPTI = sum(last_12_months_pti)
        r_cumlER = sum(last_12_months_er)
        
        r_cumlER2 = r_cumlER / 12
        annualized12mrollROA = r_cumlPTI / r_cumlER2 if r_cumlER2 !=0 else 0
        
        cumlPTI_list.append(r_cumlPTI)
        cumlER_list.append(r_cumlER)
        cumlER2_list.append(r_cumlER2)
        annualized12mrollROA_list.append(annualized12mrollROA)
        
    result['r_cumlPTI'] = cumlPTI_list
    result['r_cumlER'] = cumlER_list
    result['r_cumlER2'] = cumlER2_list
    result['annualized12mrollROA'] = annualized12mrollROA_list
    
    
   
    
    #ROA CALCULATIONS
    
    result['CumlROA'] = np.where(result['avgReceivable'] == 0, 0, ((result["cumlPTI"] / result['avgReceivable'])))
    result['AnnualizedROA'] = result['PreTaxIncome'] / result['EndingReceivable'] * 12
    # result['CumlROAAnnual'] = np.where(result['avgReceivable2'] == 0, 0, (result["cumlPTI"] / result['avgReceivable2'] / (result['Month'] / 12) * 100))

    #CHARGE OFF CALCULATIONS
    
    result['UnitChargeOffRate'] = np.where(result['ChargeOffs'] == 0, 0, (result['ChargeOffs'] / result['ActiveAccInd'] * 100))
    result['CumlUnitChargeOffRate'] = np.where(result['cumlCO'] == 0,0, (result['cumlCO'] / (result['cumlNewAcc'] - result['cumlUnwind']) * 100))

    #NetChargeOffRate
    
    result['CumlNetChargeOffRate'] = (result['CumlNetChargeOffs'] / result['avgReceivable'] * 100)
    result['cumlPmtsPerBookedAcct'] = result['cumlNetPayments'] / result['cumlNewAcc']

    #ENDING BAL
    
    result['AvgEndBalPerBookedAcct'] = result['EndingReceivable'] / result['cumlNewAcc']
    result['cumlPurPBookedAcct'] = result['cumlTtlNetSales'] / result['cumlNewAcc']
    # result['AvgAce2Score'] = result['Ace2'] / result['Ace2Ind']

    result['avgBalPActive'] = result['EndingReceivable'] / result['ActiveAccInd']
    
    #ACE 2 Scores


    result['cumlPTIPerBooked'] = result['cumlPTI'] / result['cumlNewAcc']
    result['cumlGrossRevpBooked'] = result['cumlGrsRev'] / result['cumlNewAcc']

    result['cumlFraudRate'] = result['cumlFraudCnt'] / (result['cumlNewAcc'] - result['cumlUnwind'])

    result['AvgPmtPerActive'] = result['cumlNetPayments'] / result['cumlActiveAcc']

    result['CumlNetFraudDollRate'] = result['cumlFraudAmt'] / result['avgReceivable']
    
    
    result['UtilRate'] = result['EndingReceivable'] / result['CreditLine'] 

    result['AvgCLPerActive'] = result['CreditLine'] / result['ActiveAccInd']
    
    result['cumlFinChargePBooked'] = result['cumlTtlFinCharge'] / result['cumlNewAcc']
    
    #keeps monthsonbooks to selected interval, returned from filterdataframe function

    # result['YearMonth'] = pd.to_datetime(result[['Year', 'Month']].assign(day=1)).dt.strftime('%Y-%b')
    # melted_df = pd.melt(result, id_vars=['YearMonth'], value_vars=['NewAccInd', 'ActiveAccInd', 'PreTaxIncome'], var_name='Metrics', value_name='Date')
    
    
    # melted_df['Date'] = pd.to_datetime(melted_df['Date'], format='ISO8601')
    # Pivot the DataFrame
    
    # pivoted_df = melted_df.pivot_table(index='Metrics', columns='YearMonth', values=['Date'])
    # st.write(pivoted_df)


    # result = result.sort_values(by=['Year', 'Month'], ascending=[True, True])
    
    return result, addedSelections


# Example usage

# filtered_df, selList = filter_dataframe(df = df, sel_vin= '2023-01', sel_fs="FirstAccount")
