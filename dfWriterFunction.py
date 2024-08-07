import pandas as pd
import streamlit as st
import numpy as np
import calendar
df=pd.read_parquet(r"SampleTest_Dates.parquet")



def filter_dataframe(df, sel_vin = ' ', sel_data = ' ', sel_fs = ' ', sel_brand = ' ', sel_pg = ' ', sel_assc = ' ', 
            sel_mob = ' ', sel_channel = ' ', sel_source = ' ', sel_sub = ' ', 
           sel_acq = ' ', sel_ogcl = ' ', sel_annfee = ' ', sel_ret = ' '):
    
    
    #conditions is for the actual filtering, added selections is to display all the choices on legend of graph
    conditions = []
    addedSelections = []
    #if selection is not empty or all, add it to the list of conditions
    if sel_vin != ' ' and sel_vin != 'All':
        conditions.append(df['Year'] == sel_vin)
        addedSelections.append(sel_vin)

    if sel_data != ' ' and sel_data != 'All':
        conditions.append(df['TimeonBooks'] == sel_data)
        addedSelections.append(sel_data)
        
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
        conditions.append(df['Source'] == sel_source)
        addedSelections.append(sel_source)

    if sel_sub != ' ' and sel_sub != 'All':
        conditions.append(df['Subchannel'] == sel_sub)
        addedSelections.append(sel_sub)

    if sel_acq != ' ' and sel_acq != 'All':
        conditions.append(df['Acquisitions'] == sel_acq)
        addedSelections.append(sel_acq)

    if sel_ogcl != ' ' and sel_ogcl != 'All':
        conditions.append(df['OriginalCreditLineRange'] == sel_ogcl)
        addedSelections.append(sel_ogcl)
        
    if sel_annfee != ' ' and sel_annfee != 'All':
        conditions.append(df['AnnualFeeGroup'] == sel_annfee)
        addedSelections.append(sel_annfee)

    if sel_ret != ' ' and sel_ret != 'All':
        conditions.append(df['RetainedBusiness'] == sel_ret)
        addedSelections.append(sel_ret)

    if sel_mob != ' ' and sel_mob != 'All':
        addedSelections.append(sel_mob)



    filtered_df = pd.DataFrame()

    # Combine all conditions using the & operator, filters actual dataframe
    if conditions:
        combined_conditions = conditions[0]

        for condition in conditions[1:]:
            combined_conditions &= condition
        

        
        filtered_df = df[combined_conditions]


    else:
        filtered_df = df

    
    filtered_df = filtered_df.sort_values(by=['Year', 'Month'], ascending=[True, True])
    #aggregates data by chosen vintage and by MOB
    result = filtered_df.groupby(['ReportingDate', 'Year', 'Month']).agg(
         NewAccInd = ('NewAccountIndicator', 'sum')
        , ActiveAccInd = ('ActiveAccountIndicator', 'sum')
        , TotalPayments = ('TotalPayments', 'sum')
        , TotalPaymentsAdj = ('TotalPaymentAdjustments', 'sum')
        , TotalNetSales = ('TotalNetSales', 'sum')
        , EndingReceivable=('EndingReceivable', 'sum')
        , CreditLine = ('CreditLine', 'sum')
        , PreTaxIncome=('PreTaxIncome', 'sum')
        , ChargeOffs=('ChargeOffIndicator', 'sum')
        , Unwinds = ('UnwindIndicator', 'sum')
        , ChargeOffPrcbl = ('ChargeOffPrincipalAmount', 'sum')
        , FraudAmt = ('FraudAmount', 'sum')
        , FraudCnt = ('FraudCount', 'sum')
        , GrsRev = ('GrossRevenue', 'sum')
        , TotalFinCharge = ('TotalFinanceCharges', 'sum')).reset_index()
    
    result = result.sort_values(by=['Year', 'Month'], ascending=[True, True])

    # result['avgReceivable'] = result['EndingReceivable'] / result['Month']

    result['NetChargeOff'] = result["ChargeOffPrcbl"] - result["FraudAmt"]
    result['netPayments'] = result['TotalPayments'] + result['TotalPaymentsAdj']
    result['UnitChargeOffRate'] = np.where(result['ChargeOffs'] == 0, 0, (result['ChargeOffs'] / result['ActiveAccInd'] * 100))
    result['PaymentsPerActive'] = result['netPayments'] / result['ActiveAccInd']
    result['AvgEndBalPerBookedAcct'] = result['EndingReceivable'] / result['NewAccInd']
    result['avgBalPActive'] = result['EndingReceivable'] / result['ActiveAccInd']
    result['AvgPmtPerActive'] = result['netPayments'] / result['ActiveAccInd']
    #need to add a data pull where we only pull the credit line of active accounts for utlization rate
    # result['UtilRate'] = result['EndingReceivable'] / result['CreditLine'] 
    # result['AvgCLPerActive'] = result['CreditLine'] / result['ActiveAccInd']

    result['avgBalPActive'] = result['EndingReceivable'] / result['ActiveAccInd']
    #ROA CALCULATIONS
    result['AnnualizedROA'] = np.where(result['EndingReceivable'] == 0, 0, ((result["PreTaxIncome"] / result['EndingReceivable']*12)))
    # result['Annual12MRollROA'] = np.where(result['EndingReceivable'] == 0, 0, (result["PreTaxIncome"] / result['EndingReceivable'] / 12) * 100)


    #CumlFraudRate = CumlFraudCount / (CumlNewAccountIndicator - CumlUnwinds);
    
    # Combine year and month into a single column
    result['YearMonth'] = pd.to_datetime(result[['Year', 'Month']].assign(day=1)).dt.strftime('%Y-%b')
    melted_df = pd.melt(result, id_vars=['YearMonth'], value_vars=['NewAccInd', 'ActiveAccInd', 'Unwinds', 'PaymentsPerActive', 'ChargeOffs'], var_name='Metrics', value_name='Date')
    # melted_df['Date'] = pd.to_datetime(melted_df['Date'], format='ISO8601')
    # Pivot the DataFrame
    pivoted_df = melted_df.pivot_table(index='Metrics', columns='YearMonth', values=['Date'])
    st.write(pivoted_df)


    result = result.sort_values(by=['Year', 'Month'], ascending=[True, True])
    return result, addedSelections

# Example usage

#filtered_df, selList = filter_dataframe(df = df, sel_vin = '2022-01', sel_fs="FirstAccount")


