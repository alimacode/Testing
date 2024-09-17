import pandas as pd
import streamlit as st
import numpy as np
from collections import deque
from math import log, exp 
# df=pd.read_parquet(r"C:\Users\amalik\ProjectDash\Data\dashbase.parquet")
# df=pd.read_parquet(r"C:\Users\cmacedo\Data\vcr_base_24.parquet")

if 'KPI_DF' not in st.session_state:
     st.session_state['KPI_DF'] = pd.DataFrame()
    #  st.session_state['Differences'] = 0

if 'counter' not in st.session_state:
    st.session_state['counter'] = 1

    
def filter_dataframe(filtered_df, sel_vin = ' ', selList=[]):
    # #conditions is for the actual filtering, added selections is to display all the choices on legend of graph
    # #if selection is not empty or all, add it to the list of conditions
    filtered_df= filtered_df.fillna(0)
    filtered_df = filtered_df[filtered_df['vintage'] == sel_vin]
    filtered_df= filtered_df.fillna(0)

    

    # #bucketCounts
    # filtered_df['currentCount'] = np.where(filtered_df['dimBucketID'] == 0, filtered_df['ActiveAccountIndicator'], 0)
    # filtered_df['fiveCount'] = np.where(filtered_df['dimBucketID'] == 5, filtered_df['DimbuckIDcount'], 0)
    # filtered_df['thirtyCount'] = np.where(filtered_df['dimBucketID'] == 30, filtered_df['DimbuckIDcount'], 0)
    # filtered_df['sixtyCount'] = np.where(filtered_df['dimBucketID'] == 60, filtered_df['DimbuckIDcount'], 0)
    # filtered_df['ninetyCount'] = np.where(filtered_df['dimBucketID'] == 90, filtered_df['DimbuckIDcount'], 0)
    # filtered_df['120Count'] = np.where(filtered_df['dimBucketID'] == 120, filtered_df['DimbuckIDcount'], 0)
    # filtered_df['150plus'] = np.where(filtered_df['dimBucketID'] >= 150, filtered_df['DimbuckIDcount'], 0)

    # # #unit rates
    # filtered_df['thirtyPlus'] = np.where(filtered_df['dimBucketID'] >= 30, filtered_df['DimbuckIDcount'], 0)
    # filtered_df['sixtyPlus'] = np.where(filtered_df['dimBucketID'] >= 60, filtered_df['DimbuckIDcount'], 0)
    # filtered_df['ninetyPlus'] = np.where(filtered_df['dimBucketID'] >= 90, filtered_df['DimbuckIDcount'], 0)

    # # #bucketCounts
    # filtered_df['currentReceivable'] = np.where(filtered_df['dimBucketID'] == 0, filtered_df['EndingReceivable'], 0)
    # filtered_df['fivedayReceivable'] = np.where(filtered_df['dimBucketID'] == 5, filtered_df['EndingReceivable'], 0)
    # filtered_df['30dayReceivable'] = np.where(filtered_df['dimBucketID'] == 30, filtered_df['EndingReceivable'], 0)
    # filtered_df['60dayReceivable'] = np.where(filtered_df['dimBucketID'] == 60, filtered_df['EndingReceivable'], 0)
    # filtered_df['90dayReceivable'] = np.where(filtered_df['dimBucketID'] == 90, filtered_df['EndingReceivable'], 0)
    # filtered_df['120dayReceivable'] = np.where(filtered_df['dimBucketID'] == 120, filtered_df['EndingReceivable'], 0)
    # filtered_df['150dayReceivable'] = np.where(filtered_df['dimBucketID'] == 150, filtered_df['EndingReceivable'], 0)
    
    # filtered_df['ActiveCreditLine'] = np.where(filtered_df['ActiveAccountIndicator'] == 1, filtered_df['CreditLine'], 0)
    #aggregates data by chosen vintage and by MOB
    result = filtered_df.groupby(['vintage', 'MonthsOnBooks']).agg(
        #Account Indicator Information
        #   NewAccInd = ('NewAccountIndicator', 'sum')
        NewAccInd = ('NewAccounts', 'sum')
        , ActiveAccInd = ('ActiveAccountIndicator', 'sum')
        , InactiveAccInd = ('InactiveAccountIndicator', 'sum')
        , ChargeOffIndicator = ('ChargeOffIndicator', 'sum')
        # , FraudCardIndicator = ('FraudCardIndicator', 'sum')
        # , Unwinds = ('Unwinds', 'sum')
        , Unwinds = ('UnwindCount', 'sum')
        #Purchase Information
        , TotalNetSales = ('TotalNetSales', 'sum')
        , TotalCashAdvances = ('TotalCashAdvances', 'sum')
        # , ReturnAmount = ('ReturnAmount', 'sum')
        #Payment Information
        , TotalPayments = ('TotalPayments', 'sum')
        # , TotalPaymentsAdj = ('TotalPaymentAdjs', 'sum')
        , TotalPaymentsAdj = ('TotalPaymentAdjustments', 'sum')
        , TotalPaymentReturns = ('TotalPaymentReturns', 'sum')
        # , PaymentCount = ('PaymentCount', 'sum')
        # , TotalNetPaymentCount = ('TotalNetPaymentCount', 'sum')
        #Balance Sheet Information
        # , CreditLine = ('CreditLine', 'sum')
        , ActiveCreditLine = ('ActiveCreditLine', 'sum')
        , EndingReceivable=('EndingReceivable', 'sum')
        , PrincipalReceivable=('PrincipalReceivable', 'sum')

        , ChargeOffAmount = ('ChargeOffAmount', 'sum')
        
        # , ChargeOffPrincipalAmount = ('ChargeOffPrincAmt', 'sum')
        
        # , ChargeOffAmountNoFraud = ('ChargeOffAmountNoFraud', 'sum')
        # , ChargeOffPrincipalAmountNoFraud = ('ChargeOffPrincipalAmountNoFraud', 'sum')
        , ChargeOffPrincipalAmountNoFraud = ('ChargeOffPrincipalAmount', 'sum')
         , ChargeOffs=('ChargeOffIndicator', 'sum')
        
        # , FraudCnt = ('FraudCount', 'sum')
        , FraudCnt = ('FraudCount', 'sum')
        , FraudAmt = ('FraudLossAmount', 'sum')
        # , GrossCOAmount = ('GrossCOAmount', 'sum')
        , RecoveriesAmount = ('RecoveriesAmount', 'sum')
        # , BalanceTransferAmount = ('BalanceTransferAmount', 'sum')
        # , BalanceTransferReversalAmount = ('BalanceTransferReversalAmount', 'sum')
        #CashFlow Information
        # , TotalChargeOff = ('TotalChargeOff', 'sum')
        #Income Statement Information
        , FeeEnrollmentAmount = ('FeeEnrollmentAmount', 'sum')
        , FeeOverlimitAmount = ('FeeOverlimitAmount', 'sum')
        # , FeeClosedAccountMaintAmount = ('FeeClosedAccountMaintAmount', 'sum')
        , FeeAnnualChargeAmount = ('FeeAnnualChargeAmount', 'sum')
    
        , TotalFinanceCharges = ('TotalFinanceCharges', 'sum')
        
        , FeeLateAccruedAmount = ('FeeLateAccruedAmount', 'sum')
        , FeeMiscAccruedTtlAmt = ('FeeMiscAccruedTtlAmt', 'sum')
        , FeeDirectCheckAmount = ('FeeDirectCheckAmount', 'sum')
        , FeeCashAdvanceAmount = ('FeeCashAdvanceAmount', 'sum')
        , FeeCrLineIncreaseMiscAmt = ('FeeCrLineIncreaseMiscAmt', 'sum')
        # , FeeBalanceTransferAmount = ('FeeBalanceTransferAmount', 'sum')
        , CreditProtectionAmount = ('CreditProtectionAmount', 'sum')
        , TotalMiscellaneous = ('TotalMiscellaneous', 'sum')
        , TotalFeeAdjustments = ('TotalFeeAdjustments', 'sum')
        , InterchangeRevenue = ('InterchangeRevenue', 'sum')
        , ProvisionExpense = ('ProvisionExpense', 'sum')
        , RewardsAmount = ('RewardsAmount', 'sum')  
        #ACE Reserves Information
        # , Ace2 = ('Ace2Score', 'sum')
        # , Ace2Ind = ('Ace2ScoreIndicator', 'sum')
        , Ace2 = ('ACE2Score', 'sum')
        , Ace2Ind = ('ACE2ScoreIndicator', 'sum')
        # , ReserveBalanceGrossAmount = ('ReserveBalanceGrossAmount', 'sum')
        , ReserveBalGrossAmount2 = ('ReserveBalGrossAmount2', 'sum')
        #Servicing Expenses
        , CustomerServiceExpense = ('CustomerServiceExpense', 'sum')
        , CollectionsExpensePreCalland530 = ('CollectionsExpensePreCalland530', 'sum')
        , CollectionsExpense60Plus = ('CollectionsExpense60Plus', 'sum')
        , SystemExpense = ('SystemsExpense', 'sum')
        , CreditProtectionExpense = ('CreditProtectionExpense', 'sum')
        , OtherOverheadExpense = ('OtherOverheadExpense', 'sum')
        #Other Expenses Information
        , CostofFundsExpense = ('OtherOverheadExpense', 'sum')
        , MarketingCost = ('MarketingCost', 'sum')
        , OneTimeBookingCost = ('OneTimeBookingExpense', 'sum')
        # , RecoveryExpense = ('RecoveryExpense', 'sum')
        , FraudNetAmount52 = ('FraudNetAmount52', 'sum')
        , FraudGrossAmount88 = ('FraudGrossAmount88', 'sum')
        , FraudLossAmount = ('FraudLossAmount', 'sum')
        #Profit Information
        # , GrsRev = ('GrossRevenue', 'sum')
        # , NetRevenue = ('NetRevenue', 'sum')
        , ServicingExpenses = ('ServicingExpenses', 'sum')
        # , OperatingExpenses = ('OperatingExpenses', 'sum')
        , PreTaxIncome=('PreTaxIncome', 'sum')
        
        #Scores
        # , Vantage3Score = ('Vantage3Score', 'sum')
        # , Vantage3ScoreIndicator = ('Vantage3ScoreIndicator', 'sum')
        # , CBScore = ('CBScore', 'sum')
        # , CBScoreIndicator = ('CBScoreIndicator', 'sum')
        
        # , CurrentCount = ('currentCount', 'sum')
        # , FiveCount = ('fiveCount', 'sum')
        # , ThirtyCount = ('thirtyCount', 'sum')
        # , SixtyCount = ('sixtyCount', 'sum')
        # , NinetyCount = ('ninetyCount', 'sum')
        # , Count120 = ('120Count', 'sum')
        # , Count150 = ('150plus', 'sum')
        # , ThirtyPlusCount = ('thirtyPlus', 'sum')
        # , SixtyPlusCount = ('sixtyPlus', 'sum')
        # , NinetyPlusCount = ('ninetyPlus', 'sum')
        # , currRcvbl = ('currentReceivable', 'sum')
        # , fiveRcvbl = ('fivedayReceivable', 'sum')
        # , thirtyRcvbl = ('30dayReceivable', 'sum')
        # , sixtyRcvbl = ('60dayReceivable', 'sum')
        # , ninetyRcvbl = ('90dayReceivable', 'sum')
        # , oneTwentyRcvbl = ('120dayReceivable', 'sum')
        # , oneFiftyRcvbl = ('150dayReceivable', 'sum')).reset_index()
        
        , CurrentCount = ('Bucket0Count', 'sum')
        , FiveCount = ('Bucket5Count', 'sum')
        , ThirtyCount = ('Bucket30Count', 'sum')
        , SixtyCount = ('Bucket60Count', 'sum')
        , NinetyCount = ('Bucket90Count', 'sum')
        , Count120 = ('Bucket120Count', 'sum')
        , Count150 = ('Bucket150Count', 'sum')
        , Count180 = ('Bucket180Count', 'sum')
        # , ThirtyPlusCount = ('thirtyPlus', 'sum')
        # , SixtyPlusCount = ('sixtyPlus', 'sum')
        # , NinetyPlusCount = ('ninetyPlus', 'sum')
        , currRcvbl = ('Bucket0Amount', 'sum')
        , fiveRcvbl = ('Bucket5Amount', 'sum')
        , thirtyRcvbl = ('Bucket30Amount', 'sum')
        , sixtyRcvbl = ('Bucket60Amount', 'sum')
        , ninetyRcvbl = ('Bucket90Amount', 'sum')
        , oneTwentyRcvbl = ('Bucket120Amount', 'sum')
        , oneFiftyRcvbl = ('Bucket150Amount', 'sum')
        , one80Recvbl = ('Bucket180Amount', 'sum')).reset_index()


    # result['AVGVantageScore'] = np.where(result['Vantage3Score'] == 0, None, ((result['Vantage3Score'] / result['Vantage3ScoreIndicator'])))
    # result['AVGCBScore'] = np.where(result['CBScore'] == 0, None, ((result['CBScore'] / result['CBScoreIndicator'])))
    # result['Score'] = np.where((result['Year'] < 2018) & (result['Month'] < 10)), (result['AVGCBScore'], result['AVGVantageScore'])


 
    # result['unitRate30+'] = result["ThirtyPlusCount"] / result["ActiveAccInd"] 
    # result['unitRate60+'] = result["SixtyPlusCount"] / result["ActiveAccInd"] 
    # result['unitRate90+'] = result["NinetyPlusCount"] / result["ActiveAccInd"]
    
    # result['30+UnitM3'] = np.where(result['MonthsOnBooks'] == 3, result['unitRate30+'], None)
    # result['30+UnitM4'] = np.where(result['MonthsOnBooks'] == 4, result['unitRate30+'], None)

    # result['unitRate30+'] = result['unitRate30+'].apply(lambda x:'{:1%}'.format(x))
    # result['unitRate60+'] = result['unitRate60+'].apply(lambda x:'{:1%}'.format(x))
    # result['unitRate90+'] = result['unitRate90+'].apply(lambda x:'{:1%}'.format(x))

    result['30+rcvbl'] = result['thirtyRcvbl'] + result['sixtyRcvbl'] + result['ninetyRcvbl'] + result['oneTwentyRcvbl'] + result['oneFiftyRcvbl']
    result['60+rcvbl'] = result['sixtyRcvbl'] + result['ninetyRcvbl'] + result['oneTwentyRcvbl'] + result['oneFiftyRcvbl']
    result['90+rcvbl'] = result['ninetyRcvbl'] + result['oneTwentyRcvbl'] + result['oneFiftyRcvbl']

    result['30DollRate'] = result['30+rcvbl'] / result['EndingReceivable']
    result['60DollRate'] = result['60+rcvbl'] / result['EndingReceivable']
    result['90DollRate'] = result['90+rcvbl'] / result['EndingReceivable']
                                                  
    # result['30DollRate'] = result['30DollRate'].apply(lambda x:'{:.1%}'.format(x))
    # result['60DollRate'] = result['60DollRate'].apply(lambda x:'{:.1%}'.format(x))
    # result['90DollRate'] = result['90DollRate'].apply(lambda x:'{:.1%}'.format(x))

    #dollar roll rates
    result['prevCurrentR'] = result['currRcvbl'].shift(1)
    result['curr5R'] = result["FiveCount"] / result['prevCurrentR']

    result['prevFiveR'] = result['fiveRcvbl'].shift(1)
    result['fiveThirtyR'] = result['thirtyRcvbl'] / result['prevFiveR']

    result['prevThirtyR'] = result['thirtyRcvbl'].shift(1)
    result['ThirtySixtyR'] = result['sixtyRcvbl'] / result['prevThirtyR']
    
    result['prevSixtyR'] = result['sixtyRcvbl'].shift(1)
    result['SixtyNinetyR'] = result['NinetyCount'] / result['prevSixtyR']

    result['prevNinetyR'] = result['ninetyRcvbl'].shift(1)
    result['Ninety120R'] = result['oneTwentyRcvbl'] / result['prevNinetyR']

    result['prev120R'] = result['oneTwentyRcvbl'].shift(1)
    result['rate120150R'] = result['oneFiftyRcvbl'] / result['prev120R']

    result['prev150R'] = result['oneFiftyRcvbl'].shift(1)
    result['rate150-COR'] = result['ChargeOffs'] / result['prev150R']
    
    #unit roll rates
    result['prevCurrent'] = result['CurrentCount'].shift(1)
    result['curr5'] = result["FiveCount"] / result['prevCurrent']

    result['prevFive'] = result['FiveCount'].shift(1)
    result['fiveThirty'] = result['ThirtyCount'] / result['prevFive']

    result['prevThirty'] = result['ThirtyCount'].shift(1)
    result['ThirtySixty'] = result['SixtyCount'] / result['prevThirty']
    
    result['prevSixty'] = result['SixtyCount'].shift(1)
    result['SixtyNinety'] = result['NinetyCount'] / result['prevSixty']

    result['prevNinety'] = result['NinetyCount'].shift(1)
    result['Ninety120'] = result['Count120'] / result['prevNinety']

    result['prev120'] = result['Count120'].shift(1)
    result['rate120150+'] = result['Count150'] / result['prev120']

    result['prev150'] = result['Count150'].shift(1)
    result['rate150-CO'] = result['ChargeOffs'] / result['prev150']
    
    # result['prod7mobsUnitRate'] = result['curr5'] + result['fiveThirty'] + result['ThirtySixty'] 
    #                             + result['SixtyNinety'] + result['Ninety120'] + result['rate120150+'] + result['rate150-CO']
    
    
    # result['RolltoCO'] = np.where(result['MonthsOnBooks'] < 7, 0, exp(map(log, result['prod7mobsUnitRate'])))
    
    rolltoCO_list = []
    for index, row in result.iterrows():
        if row['curr5'] is not None and row['MonthsOnBooks'] >= 7:
            rolltoCO_list.append(row['curr5'])
        # if row['fiveThirty'] is not None and result['MonthsOnBooks'] >= 7:
        #     rolltoCO_list.append(row['fiveThirty']) 
        # if row['ThirtySixty'] is not None and result['MonthsOnBooks'] >= 7:
        #     rolltoCO_list.append(row['ThirtySixty']) 
        # if row['SixtyNinety'] is not None and result['MonthsOnBooks'] >= 7:
        #     rolltoCO_list.append(row['SixtyNinety']) 
        # if row['Ninety120'] is not None and result['MonthsOnBooks'] >= 7:
        #     rolltoCO_list.append(row['Ninety120']) 
        # if row['rate120150+'] is not None and result['MonthsOnBooks'] >= 7:
        #     rolltoCO_list.append(row['rate120150+']) 
        # if row['rate150-CO'] is not None and result['MonthsOnBooks'] >= 7:
        #     rolltoCO_list.append(row['rate150-CO']) 
        
        
    result['RolltoCO'] = exp(sum(map(log, rolltoCO_list)))
    

    
    result['NetChargeOff'] = result["ChargeOffPrincipalAmountNoFraud"] - result["FraudAmt"]
    result['netPayments'] = result['TotalPayments'] + result['TotalPaymentsAdj']


    # result['curr5'] = result['curr5'].apply(lambda x:'{:.1%}'.format(x))
    # result['fiveThirty'] = result['fiveThirty'].apply(lambda x:'{:.1%}'.format(x))
    # result['ThirtySixty'] = result['ThirtySixty'].apply(lambda x:'{:.1%}'.format(x))
    # result['SixtyNinety'] = result['SixtyNinety'].apply(lambda x:'{:.1%}'.format(x))
    # result['Ninety120'] = result['Ninety120'].apply(lambda x:'{:.1%}'.format(x))
    # result['rate120150+'] = result['rate120150+'].apply(lambda x:'{:.1%}'.format(x))
    # result['rate150-CO'] = result['rate150-CO'].apply(lambda x:'{:.1%}'.format(x))

    result['FraudDolAmt'] = result['FraudNetAmount52'] + result['FraudGrossAmount88']
    
    #getting cumulative sums of all data
    result['cumlNewAcc'] = result.groupby('vintage')['NewAccInd'].cumsum()
    result['cumlActiveAcc'] = result.groupby('vintage')['ActiveAccInd'].cumsum()
    result['cumlPTI'] = result.groupby('vintage')['PreTaxIncome'].cumsum()
    result['cumlER'] = result.groupby('vintage')['EndingReceivable'].cumsum()
    result['cumlCO'] = result.groupby('vintage')['ChargeOffs'].cumsum()
    result['cumlUnwind'] = result.groupby('vintage')['Unwinds'].cumsum()
    result['CumlNetChargeOffs'] = result.groupby('vintage')['NetChargeOff'].cumsum()
    result['cumlNetPayments'] = result.groupby('vintage')['netPayments'].cumsum()
    result['cumlTtlNetSales'] = result.groupby('vintage')['TotalNetSales'].cumsum()
    result['cumlFraudCnt'] = result.groupby('vintage')['FraudCnt'].cumsum()
    # result['cumlGrsRev'] = result.groupby('vintage')['GrsRev'].cumsum()
    result['cumlFraudAmt'] = result.groupby('vintage')['FraudAmt'].cumsum()
    result['cumlTtlFinCharge'] = result.groupby('vintage')['TotalFinanceCharges'].cumsum()
    
    result['cumlFraudDolAmt'] = result.groupby('vintage')['FraudDolAmt'].cumsum()
    

    result['avgActives'] = result['cumlActiveAcc'] / result['MonthsOnBooks']
    result['avgReceivable'] = result['cumlER'] / result['MonthsOnBooks']
    result['cumlPTIPerBooked'] = result['cumlPTI'] / result['cumlNewAcc']
    result['cumlPTIPerActive'] = result['cumlPTI'] / result['cumlActiveAcc']
    #calculations for more other graphs, creates columns in dataframe for each new 
    result['MonthsOnBooks'] = pd.to_numeric(result['MonthsOnBooks'])
    #running calculations for plotting
    
    result['prevActives'] = result['ActiveAccInd'].shift(1)
    
    result['Attrition'] = result['prevActives'] + result['cumlNewAcc'] - result['ChargeOffs'] - result['ActiveAccInd'] 
    
    result['AttritionRate'] = result['Attrition'] / result['ActiveAccInd']
    
    result['cumlAttrition'] = result.groupby('vintage')['Attrition'].cumsum()
    
    result['CumlAttritionRate'] = result['cumlAttrition'] / result['cumlNewAcc']
    
    
    
    
    
    #ROA CALCULATIONS
    # result['CumlROA'] = np.where(result['avgReceivable'] == 0, 0, ((result["cumlPTI"] / result['avgReceivable'])))
    result['ROA'] = np.where(result['avgReceivable'] == 0, 0, ((result["PreTaxIncome"] / result['EndingReceivable']*12)))
    result['CumlROA'] = np.where(result['avgReceivable'] == 0, 0, ((result["cumlPTI"] / (result['cumlER']/ result['MonthsOnBooks']))))
    
    result['CumlROAAnnual'] = np.where(result['avgReceivable'] == 0, 0, (result["cumlPTI"] / result['avgReceivable'] / (result['MonthsOnBooks'] / 12)))

    # result['avgActives'] = result['cumlActiveAcc'] / result['MOBS']
    # result['avgReceivable'] = result['cumlER'] / result['MOBS']
 
    # result['avgReceivable2'] = result['cumlER'] / result['Month']
    
    #rolling 12 month roa
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

    result['Percent_Active'] = np.where(result['ActiveAccInd'] == 0, 0, (result['ActiveAccInd'] / result['cumlNewAcc']))
    result['CumlUnwindsRate'] = np.where(result['cumlUnwind'] == 0, 0, (result['cumlUnwind'] / result['cumlNewAcc']))
    result['FraudRate'] = np.where(result['FraudCnt'] == 0, None, (result['FraudCnt'] / result['ActiveAccInd']))
    
 
    
    
    

    #CHARGE OFF CALCULATIONS
    result['UnitChargeOffRate'] = np.where(result['ChargeOffs'] == 0, 0, (result['ChargeOffs'] / result['ActiveAccInd']))
    result['CumlUnitChargeOffRate'] = np.where(result['cumlCO'] == 0,0, (result['cumlCO'] / (result['cumlNewAcc'] - result['cumlUnwind'])))

    #NetChargeOffRate
    result['CumlNetChargeOffRate'] = (result['CumlNetChargeOffs'] / result['avgReceivable'])
    result['cumlPmtsPerBookedAcct'] = result['cumlNetPayments'] / result['cumlNewAcc']

    #ENDING BAL
    result['AvgEndBalPerBookedAcct'] = result['EndingReceivable'] / result['cumlNewAcc']
    result['cumlPurPBookedAcct'] = result['cumlTtlNetSales'] / result['cumlNewAcc']
    result['AvgAce2Score'] = result['Ace2'] / result['Ace2Ind']

    result['avgBalPActive'] = result['EndingReceivable'] / result['ActiveAccInd']
    result['Average Balance per Booked'] = result['EndingReceivable'] / result['cumlNewAcc']


    # result['cumlGrossRevpBooked'] = result['cumlGrsRev'] / result['cumlNewAcc']

    result['cumlFraudRate'] = result['cumlFraudCnt'] / (result['cumlNewAcc'] - result['cumlUnwind'])

    result['AvgPmtPerActive'] = result['cumlNetPayments'] / result['cumlActiveAcc']

    result['DolNetFraudRate'] = np.where(result['FraudDolAmt'] == 0, 0, (result['FraudDolAmt'] / result['EndingReceivable']))
    
    result['DolGrossFraudRate'] = np.where(result['FraudAmt'] == 0, 0, (result['FraudAmt'] / result['EndingReceivable']) )
    
    result['AvgNetCO'] = np.where(result['NetChargeOff'] == 0, 0, (result['NetChargeOff'] / result['ChargeOffs']))
    
    # result['CumlNetFraudDollRate'] = np.where(result['cumlFraudAmt']== 0, 0, (result['cumlFraudAmt'] / result['avgReceivable']))
    result['CumlNetFraudDollRate'] = np.where(result['cumlFraudDolAmt']== 0, 0, (result['cumlFraudDolAmt'] / result['avgReceivable']))
    # result['UtilRate'] = result['EndingReceivable'] / result['CreditLine'] 

    # result['AvgCLPerActive'] = result['CreditLine'] / result['ActiveAccInd']
    result['cumlFinChargePBooked'] = result['cumlTtlFinCharge'] / result['cumlNewAcc']

  
    result['AVGCreditLinePerActive'] = result['ActiveCreditLine'] / result['ActiveAccInd']
    result['AVGCreditLinePerBooked'] = result['ActiveCreditLine'] / result['cumlNewAcc']
    result['UtilRate'] = result['EndingReceivable'] / result['ActiveCreditLine']

    # result['ROAAnnual'] = result['CumlROAAnnual'].apply(lambda x:'{:.1%}'.format(x))
    # result['Cumul. Unit CO Rate'] = result['CumlUnitChargeOffRate'].apply(lambda x:'{:.1%}'.format(x))
    # result['Unit CO Rate'] = result['UnitChargeOffRate'].apply(lambda x:'{:.1%}'.format(x))
    # result['Cumul. NetCORate'] = result['CumlNetChargeOffRate'].apply(lambda x:'{:.1%}'.format(x))
    # result['Cumul. FraudRate'] = result['cumlFraudRate'].apply(lambda x:'{:.1%}'.format(x))
    # result['Cumul. Net Fraud Dollar Rate'] = result['CumlNetFraudDollRate'].apply(lambda x:'{:.1%}'.format(x))
    
    # result['unitRate30+'] = result['unitRate30+'].apply(lambda x:'{:.1%}'.format(x))
    # result['unitRate60+'] = result['unitRate60+'].apply(lambda x:'{:.1%}'.format(x))
    # result['unitRate90+'] = result['unitRate90+'].apply(lambda x:'{:.1%}'.format(x))
    # result['30DollRate'] = result['30DollRate'].apply(lambda x:'{:.1%}'.format(x))
    # result['60DollRate'] = result['60DollRate'].apply(lambda x:'{:.1%}'.format(x))
    # result['90DollRate'] = result['90DollRate'].apply(lambda x:'{:.1%}'.format(x))
    # result['UtilRate'] = result['UtilRate'].apply(lambda x:'{:.1%}'.format(x))

    #KPI Chart
    # result['CumlROAMonth3'] = np.where(result['MonthsOnBooks'] == 3, result['CumlROA'], 0)
    result['BookedAccountsMOB1'] = np.where(result['MonthsOnBooks'] == 1, result['NewAccInd'], None)
    result['CumlROAMonth3'] = np.where(result['MonthsOnBooks'] == 3, result['CumlROA'], None)
    result['Month6CumulativeROA'] = np.where(result['MonthsOnBooks'] == 6, result['CumlROA'], None)
    result['Month12CumulativeROA'] = np.where(result['MonthsOnBooks'] == 12, result['CumlROA'], None)
    result['Month24CumulativeROA'] = np.where(result['MonthsOnBooks'] == 24, result['CumlROA'], None)
    result['Year2CumlUnitChargeOffRate'] = np.where(result['MonthsOnBooks'] == 12, result['CumlUnitChargeOffRate'], None)
    result['cumlPTIPerBooked12'] = np.where(result['MonthsOnBooks'] == 12, result['cumlPTIPerBooked'], None)
    result['cumlPTIPerBooked24'] = np.where(result['MonthsOnBooks'] == 24, result['cumlPTIPerBooked'], None)
    result['cumlUnitCOM12'] = np.where(result['MonthsOnBooks'] == 12, result['CumlUnitChargeOffRate'], None)
    result['Year2CumlUnitChargeOffRate'] = np.where(result['MonthsOnBooks'] == 24, result['CumlUnitChargeOffRate'], None)
    result['cumlDollarCOY1'] = np.where(result['MonthsOnBooks'] == 12, result['ChargeOffPrincipalAmountNoFraud'], None)
    result['cumlDollarCOY2'] = np.where(result['MonthsOnBooks'] == 24, result['ChargeOffPrincipalAmountNoFraud'], None)

    # KPIMelt = pd.melt(result, id_vars=["vintage"], value_vars=['cumlPTIPerBooked24', 'Month24CumulativeROA','Month12CumulativeROA','Month6CumulativeROA'
    #                                                           ,'CumlROAMonth3','cumlUnitCOM12', 'CumlROAMonth3','cumlDollarCOY1'
    #                                                           ,  'Year2CumlUnitChargeOffRate', 'cumlPTIPerBooked12','cumlDollarCOY2', 'AvgAce2Score', 
    #                                                           'avgBalPActive', 'AvgPmtPerActive', 'AvgEndBalPerBookedAcct', 
    #                                                           'cumlPurPBookedAcct', 'cumlPmtsPerBookedAcct'], var_name='Metrics', value_name='CUMLCO')
   
    # KPIMelt2 = pd.melt(result, id_vars=['vintage', 'MonthsOnBooks'], value_vars=[
    #                                         'NewAccInd',
    #                                         # 'Score',
    #                                         'AvgAce2Score',
    #                                         'cumlUnwind',
    #                                         'CumlUnwindsRate',
    #                                         'ActiveAccInd',
    #                                         'Percent_Active',
    #                                         'CurrentCount',
    #                                         'FiveCount',
    #                                         'ThirtyCount',
    #                                         'SixtyCount',
    #                                         'NinetyCount',
    #                                         'Count120',
    #                                         'Count150',
    #                                         'curr5',
    #                                         'fiveThirty',
    #                                         'ThirtySixty',
    #                                         'SixtyNinety',
    #                                         'Ninety120',
    #                                         'rate120150+',
    #                                         'rate150-CO',
    #                                         'RolltoCO',
    #                                         # 'unitRate30+',
    #                                         # 'unitRate60+',
    #                                         # 'unitRate90+',
    #                                         'UnitChargeOffRate',
    #                                         'CumlUnitChargeOffRate',
    #                                         'Attrition',
    #                                         'AttritionRate',
    #                                         'CumlAttritionRate',
    #                                         'FraudCnt',
    #                                         'FraudRate',
    #                                         'cumlFraudRate',
    #                                         'currRcvbl',
    #                                         'fiveRcvbl',
    #                                         'thirtyRcvbl',
    #                                         'sixtyRcvbl',
    #                                         'ninetyRcvbl',
    #                                         'oneTwentyRcvbl',
    #                                         'oneFiftyRcvbl',
    #                                         'curr5R',
    #                                         'fiveThirtyR',
    #                                         'ThirtySixtyR',
    #                                         'SixtyNinetyR',
    #                                         'Ninety120R',
    #                                         'rate120150R',
    #                                         'rate150-COR',
    #                                         '30DollRate',
    #                                         '60DollRate',
    #                                         '90DollRate',
    #                                         'NetChargeOff',
    #                                         'CumlNetChargeOffs',
    #                                         'FraudAmt',
    #                                         'cumlFraudAmt',
    #                                         'DolGrossFraudRate',
    #                                         'cumlFraudRate',
    #                                         'FraudNetAmount52',
    #                                         'FraudGrossAmount88',
    #                                         'FraudDolAmt',
    #                                         'cumlFraudDolAmt',
    #                                         'DolNetFraudRate',
    #                                         'CumlNetFraudDollRate',
    #                                         'ChargeOffs',
    #                                         'NetChargeOff',
    #                                         # 'GrossCOAmount',
    #                                         'NetChargeOff',
    #                                         'AvgNetCO',
    #                                         # 'GrossRevenue',
    #                                         # 'NetRevenue',
    #                                         'CustomerServiceExpense',
    #                                         'CollectionsExpensePreCalland530',
    #                                         'CollectionsExpense60Plus',
    #                                         # 'SystemsExpense',
    #                                         'CreditProtectionExpense',
    #                                         'OtherOverheadExpense',
    #                                         'ServicingExpenses',
    #                                         'CostofFundsExpense',
    #                                         'MarketingCost',
    #                                         # 'OneTimeBookingExpense',
    #                                         'FraudLossAmount',
    #                                         # 'OperatingExpenses',
    #                                         'PreTaxIncome',
    #                                         'cumlPTI',
    #                                         'ROA',
    #                                         'annualized12mrollROA',
    #                                         'CumlROAAnnual',
    #                                         'CumlROA',
    #                                         'cumlPTIPerActive',
    #                                         'cumlPTIPerBooked'], var_name='Metrics2', value_name='CUMLCO2')
    
    result['Booked Accounts'] = result['NewAccInd']
    result['Average ACE Score'] = result['AvgAce2Score']
    result['Cumulative Unwinds'] = result['cumlUnwind']
    result['Cumulative Unwinds Rate'] = result['CumlUnwindsRate']
    result['Active Accounts - End of Period'] = result['ActiveAccInd']
    result['Percent Active - End of Period'] = result['Percent_Active']
    result['Current'] = result['CurrentCount']
    result['5-Day'] = result['FiveCount']
    result['30-Day'] = result['ThirtyCount']
    result['60-Day'] = result['SixtyCount']
    result['90-Day'] = result['NinetyCount']
    result['120-Day'] = result['Count120']
    result['150-Day+'] = result['Count150']
    result['Curr-5'] = result['curr5']
    result['5-30'] = result['fiveThirty']
    result['30-60'] = result['ThirtySixty']
    result['60-90'] = result['SixtyNinety']
    result['90-120'] = result['Ninety120']
    result['120-150+'] = result['rate120150+']
    result['150+ to C/O'] = result['rate150-CO']
    # result['Roll to C/O'] = result['']
    # result['30+ Unit Rate'] = result['']
    # result['60+ Unit Rate'] = result['']
    # result['90+ Unit Rate'] = result['']
    result['Unit Charge-Off Rate'] = result['UnitChargeOffRate']
    result['Cumul. Unit Charge-Off Rate'] = result['CumlUnitChargeOffRate']
    result['Attrition'] = result['Attrition']
    result['Attrition Rate'] = result['AttritionRate']
    result['Cumulative Attrition Rate'] = result['CumlAttritionRate']
    result['Fraud'] = result['FraudCnt']
    result['Fraud Rate'] = result['FraudRate']
    result['Cumulative Fraud Rate'] = result['cumlFraudRate']
    # result['Total Gross Receivables - End of Period'] = result['']
    # result['Principal Balance - End of Period'] = result['']
    # result['Credit Lines'] = result['']
    # result['Average Balance per Active Account'] = result['']
    # result['Average Credit Line per Active Account'] = result['']
    # result['Credit Line Utilization - End of Period'] = result['']
    result['Current Dollar'] = result['currRcvbl']
    result['5-Day Dollar'] = result['fiveRcvbl']
    result['30-Day Dollar'] = result['thirtyRcvbl']
    result['60-Day Dollar'] = result['sixtyRcvbl']
    result['90-Day Dollar'] = result['ninetyRcvbl']
    result['120-Day Dollar'] = result['oneTwentyRcvbl']
    result['150-Day+ Dollar'] = result['oneFiftyRcvbl']
    result['Curr-5 Dollar'] = result['curr5R']
    result['5-30 Dollar'] = result['fiveThirtyR']
    result['30-60 Dollar'] = result['ThirtySixtyR']
    result['60-90 Dollar'] = result['SixtyNinetyR']
    result['90-120 Dollar'] = result['Ninety120R']
    result['120-150+ Dollar'] = result['rate120150R']
    # result['150+ to C/O'] = result['']
    result['$ 30+ Rate'] = result['30DollRate']
    result['$ 60+ Rate'] = result['60DollRate']
    result['$ 90+ Rate'] = result['90DollRate']
    # result['$ Net Charge-Off Rate before Recoveries'] = result['NetChargeOff']
    result['Cumul. $ Net Charge-Off Rate before Recoveries'] = result['CumlNetChargeOffs']
    result['Fraud'] = result['FraudAmt']
    result['Cumul. Fraud'] = result['cumlFraudAmt']
    result['$ Gross Fraud Rate'] = result['DolGrossFraudRate']
    # result['Cumul. $ Gross Fraud Rate'] = result['cumlFraudRate']
    result['Fraud Net (52s)'] = result['FraudNetAmount52']
    result['Fraud Gross (88s)'] = result['FraudGrossAmount88']
    result['Fraud ($)'] = result['FraudDolAmt']
    result['Cumul. Fraud ($)'] = result['cumlFraudDolAmt']
    result['$ Net Fraud Rate'] = result['DolNetFraudRate']
    result['Cumul. $ Fraud Rate'] = result['CumlNetFraudDollRate']
    result['Charged-Off Accounts'] = result['ChargeOffs']
    # result['Net Charge-Off before Recoveries'] = result['NetChargeOff']
    # result['Gross Charge-Off'] = result['']
    result['Net Charge-Off'] = result['NetChargeOff']
    result['Average Net Charge-Off Balance'] = result['AvgNetCO']
    # result['Total Gross Revenues'] = result['']
    # result['Total Net Revenues'] = result['']
    result['Customer Service'] = result['CustomerServiceExpense']
    result['Collections (Pre-Call and 5-30)'] = result['CollectionsExpensePreCalland530']
    result['Collections (60+)'] = result['CollectionsExpense60Plus']
    # result['Systems'] = result['']
    result['Credit Protection Expense'] = result['CreditProtectionExpense']
    result['Other Overhead'] = result['OtherOverheadExpense']
    result['Total Servicing Expenses'] = result['ServicingExpenses']
    result['Cost of Funds - Debt Expense'] = result['CostofFundsExpense']
    result['One Time - Marketing Expense (CPA)'] = result['MarketingCost']
    # result['One Time - Booking Expense'] = result['']
    result['Fraud Loss Expense'] = result['FraudLossAmount']
    # result['Total Operating Expenses'] = result['']
    result['Pre-Tax Income'] = result['PreTaxIncome']
    result['Cumul. Pre-Tax Income'] = result['cumlPTI']
    result['ROA - Annualized'] = result['ROA']
    result['12-Month Rolling ROA'] = result['annualized12mrollROA']
    result['Cumulative ROA - Annualized'] = result['CumlROAAnnual']
    result['Cumulative ROA'] = result['CumlROA']
    result['Cumul. PTI  -  Per Active Account'] = result['cumlPTIPerActive']
    result['Cumul. PTI  -  Per Booked Account'] = result['cumlPTIPerBooked']
    result['Cuml. Payments per Booked Account'] = result['cumlPmtsPerBookedAcct']
    result['Cuml. Purchases per Booked Account'] = result['cumlPurPBookedAcct']
    result['Average Credit Line per Booked'] = result['AVGCreditLinePerBooked']
    
    KPIMelt = pd.melt(result, id_vars=["vintage"], value_vars=['cumlNewAcc', 'Customer Service', 'Collections (Pre-Call and 5-30)','Collections (60+)'
                        ,'Credit Protection Expense','Other Overhead','Total Servicing Expenses','Cost of Funds - Debt Expense'
                        ,'One Time - Marketing Expense (CPA)','Fraud Loss Expense','Pre-Tax Income', 'Average Balance per Booked'
                        ,'Cumulative ROA', 'Cuml. Payments per Booked Account', 'Cuml. Purchases per Booked Account', 'Average ACE Score', 'Average Credit Line per Booked'], var_name='Metrics', value_name='CUMLCO')
    # KPIMelt2 = pd.melt(result, id_vars=['vintage', 'MonthsOnBooks'], value_vars=['NewAccInd','AvgAce2Score','Unwinds', 'cumlUnwind','CumlUnwindsRate','ActiveAccInd','Percent_Active','CurrentCount'
    #                                                                              ,'FiveCount','ThirtyCount','SixtyCount','NinetyCount','Count120','Count150','curr5','fiveThirty'
    #                                                                              ,'ThirtySixty','SixtyNinety','Ninety120','rate120150+','rate150-CO','UnitChargeOffRate'
    #                                                                              ,'CumlUnitChargeOffRate','Attrition','AttritionRate','CumlAttritionRate','FraudCnt','FraudRate'
    #                                                                              ,'cumlFraudRate','currRcvbl','fiveRcvbl','thirtyRcvbl','sixtyRcvbl','ninetyRcvbl','oneTwentyRcvbl'
    #                                                                              ,'oneFiftyRcvbl','curr5R','fiveThirtyR','ThirtySixtyR','SixtyNinetyR','Ninety120R','rate120150R'
    #                                                                              ,'30DollRate','60DollRate','90DollRate','NetChargeOff','CumlNetChargeOffs','FraudAmt','cumlFraudAmt'
    #                                                                              ,'DolGrossFraudRate','cumlFraudRate','FraudNetAmount52','FraudGrossAmount88','FraudDolAmt','cumlFraudDolAmt'
    #                                                                              ,'DolNetFraudRate','CumlNetFraudDollRate','ChargeOffs','NetChargeOff',  'NetChargeOff','AvgNetCO','CustomerServiceExpense'
    #                                                                              ,'CollectionsExpensePreCalland530','CollectionsExpense60Plus','CreditProtectionExpense','OtherOverheadExpense','ServicingExpenses'
    #                                                                              ,'CostofFundsExpense','MarketingCost','FraudLossAmount','PreTaxIncome','cumlPTI','ROA','annualized12mrollROA','CumlROAAnnual'
    #                                                                              ,'CumlROA','cumlPTIPerActive','cumlPTIPerBooked'], var_name='Metrics', value_name='CUMLCO')
    KPIMelt2 = pd.melt(result, id_vars=['vintage', 'MonthsOnBooks'], value_vars=['Booked Accounts','Average ACE Score','Unwinds', 'Cumulative Unwinds','Cumulative Unwinds Rate'
                                                                                 ,'Active Accounts - End of Period','Percent Active - End of Period','Current'
                                                                                 ,'5-Day','30-Day','60-Day','90-Day','120-Day','150-Day+','Curr-5','5-30'
                                                                                 ,'30-60','60-90','90-120','120-150+','150+ to C/O','Unit Charge-Off Rate'
                                                                                 ,'Cumul. Unit Charge-Off Rate','Attrition','Attrition Rate','Cumulative Attrition Rate','Fraud','Fraud Rate'
                                                                                 ,'Cumulative Fraud Rate','Current Dollar','5-Day Dollar','30-Day Dollar','60-Day Dollar','90-Day Dollar','120-Day Dollar'
                                                                                 ,'150-Day+ Dollar','Curr-5 Dollar','5-30 Dollar','30-60 Dollar','60-90 Dollar','90-120 Dollar','120-150+ Dollar'
                                                                                 ,'$ 30+ Rate','$ 60+ Rate','$ 90+ Rate', 'Cumul. $ Net Charge-Off Rate before Recoveries'
                                                                                 ,'Fraud','Cumul. Fraud','$ Gross Fraud Rate','Fraud Net (52s)','Fraud Gross (88s)'
                                                                                 ,'Fraud ($)','Cumul. Fraud ($)','$ Net Fraud Rate','Cumul. $ Fraud Rate','Charged-Off Accounts','Net Charge-Off'
                                                                                 ,'Average Net Charge-Off Balance','Customer Service','Collections (Pre-Call and 5-30)','Collections (60+)'
                                                                                 ,'Credit Protection Expense','Other Overhead','Total Servicing Expenses','Cost of Funds - Debt Expense'
                                                                                 ,'One Time - Marketing Expense (CPA)','Fraud Loss Expense','Pre-Tax Income','Cumul. Pre-Tax Income','ROA - Annualized'
                                                                                 ,'12-Month Rolling ROA','Cumulative ROA - Annualized'
                                                                                 ,'Cumulative ROA','Cumul. PTI  -  Per Active Account','Cumul. PTI  -  Per Booked Account'], var_name='Metrics2', value_name='CUMLCO2')
    # KPIMelt2['Metrics'] = pd.Categorical(KPIMelt2['Metrics'], categories=['Booked Accounts','Average ACE Score','Unwinds', 'Cumulative Unwinds','Cumulative Unwinds Rate'
    #                                                                              ,'Active Accounts - End of Period','Percent Active - End of Period','Current'
    #                                                                              ,'5-Day','30-Day','60-Day','90-Day','120-Day','150-Day+','Curr-5','5-30'
    #                                                                              ,'30-60','60-90','90-120','120-150+','150+ to C/O','Unit Charge-Off Rate'
    #                                                                              ,'Cumul. Unit Charge-Off Rate','Attrition','Attrition Rate','Cumulative Attrition Rate','Fraud','Fraud Rate'
    #                                                                              ,'Cumulative Fraud Rate','Current Dollar','5-Day Dollar','30-Day Dollar','60-Day Dollar','90-Day Dollar','120-Day Dollar'
    #                                                                              ,'150-Day+ Dollar','Curr-5 Dollar','5-30 Dollar','30-60 Dollar','60-90 Dollar','90-120 Dollar','120-150+ Dollar'
    #                                                                              ,'$ 30+ Rate','$ 60+ Rate','$ 90+ Rate'
    #                                                                              ,'Fraud','Cumul. Fraud','$ Gross Fraud Rate','Fraud Net (52s)','Fraud Gross (88s)'
    #                                                                              ,'Fraud ($)','Cumul. Fraud ($)','$ Net Fraud Rate','Cumul. $ Fraud Rate','Charged-Off Accounts','Net Charge-Off'
    #                                                                              ,'Average Net Charge-Off Balance','Customer Service','Collections (Pre-Call and 5-30)','Collections (60+)'
    #                                                                              ,'Credit Protection Expense','Other Overhead','Total Servicing Expenses','Cost of Funds - Debt Expense'
    #                                                                              ,'One Time - Marketing Expense (CPA)','Fraud Loss Expense','Pre-Tax Income','Cumul. Pre-Tax Income','ROA - Annualized'
    #                                                                              ,'12-Month Rolling ROA','Cumulative ROA - Annualized'
    #                                                                              ,'Cumulative ROA','Cumul. PTI  -  Per Active Account','Cumul. PTI  -  Per Booked Account'], ordered=True)
    KPIPiv = KPIMelt.pivot_table(index='Metrics', columns="vintage", values="CUMLCO")
    # KPIPiv2 = KPIMelt3.pivot_table(index='Metrics2', columns=["vintage", "MonthsOnBooks"], values='CUMLCO2')
    KPIPiv2 = KPIMelt2.pivot_table(index='Metrics2', columns=["vintage", "MonthsOnBooks"], values="CUMLCO2")
    
    desired_order2 = ['Booked Accounts','Average ACE Score','Unwinds', 'Cumulative Unwinds','Cumulative Unwinds Rate'
                                                                                 ,'Active Accounts - End of Period','Percent Active - End of Period','Current'
                                                                                 ,'5-Day','30-Day','60-Day','90-Day','120-Day','150-Day+','Curr-5','5-30'
                                                                                 ,'30-60','60-90','90-120','120-150+','150+ to C/O','Unit Charge-Off Rate'
                                                                                 ,'Cumul. Unit Charge-Off Rate','Attrition','Attrition Rate','Cumulative Attrition Rate','Fraud','Fraud Rate'
                                                                                 ,'Cumulative Fraud Rate','Current Dollar','5-Day Dollar','30-Day Dollar','60-Day Dollar','90-Day Dollar','120-Day Dollar'
                                                                                 ,'150-Day+ Dollar','Curr-5 Dollar','5-30 Dollar','30-60 Dollar','60-90 Dollar','90-120 Dollar','120-150+ Dollar'
                                                                                 ,'$ 30+ Rate','$ 60+ Rate','$ 90+ Rate'
                                                                                 ,'Fraud','Cumul. Fraud','$ Gross Fraud Rate','Fraud Net (52s)','Fraud Gross (88s)'
                                                                                 ,'Fraud ($)','Cumul. Fraud ($)','$ Net Fraud Rate','Cumul. $ Fraud Rate','Charged-Off Accounts','Net Charge-Off'
                                                                                 ,'Average Net Charge-Off Balance','Customer Service','Collections (Pre-Call and 5-30)','Collections (60+)'
                                                                                 ,'Credit Protection Expense','Other Overhead','Total Servicing Expenses','Cost of Funds - Debt Expense'
                                                                                 ,'One Time - Marketing Expense (CPA)','Fraud Loss Expense','Pre-Tax Income','Cumul. Pre-Tax Income','ROA - Annualized'
                                                                                 ,'12-Month Rolling ROA','Cumulative ROA - Annualized'
                                                                                 ,'Cumulative ROA','Cumul. PTI  -  Per Active Account','Cumul. PTI  -  Per Booked Account']
    
    if KPIPiv.empty == False:
    # Convert values to percentages
        # KPIPiv.loc['30+ Unit Rate - MOB 3'] = KPIPiv.loc['CumlROAMonth3'].apply(lambda x:'{:.1%}'.format(x))
        # #KPIPiv.loc['30+ Unit Rate - MOB 4'] = KPIPiv.loc['30+UnitM4'].apply(lambda x:'{:.1%}'.format(x))
        # KPIPiv.loc['ROA - MOB 3'] = KPIPiv.loc['CumlROAMonth3'].apply(lambda x:'{:.1%}'.format(x))
        # KPIPiv.loc['ROA - MOB 6'] = KPIPiv.loc['Month6CumulativeROA'].apply(lambda x:'{:.1%}'.format(x))
        # KPIPiv.loc['ROA - MOB 12'] = KPIPiv.loc['Month12CumulativeROA'].apply(lambda x:'{:.1%}'.format(x))
        # KPIPiv.loc['ROA - MOB 24'] = KPIPiv.loc['Month24CumulativeROA'].apply(lambda x:'{:.1%}'.format(x))
        # KPIPiv.loc['PTI per Booked - MOB 12'] = KPIPiv.loc['cumlPTIPerBooked12'].apply(lambda x:'{:.2f}'.format(x))
        # KPIPiv.loc['PTI per Booked - MOB 24'] = KPIPiv.loc['cumlPTIPerBooked24'].apply(lambda x:'{:.2f}'.format(x))
        # KPIPiv.loc['Dollar Charge-Off - Year 1'] = KPIPiv.loc['cumlDollarCOY1'].apply(lambda x:'{:.2f}'.format(x))
        # KPIPiv.loc['Dollar Charge-Off - Year 2'] = KPIPiv.loc['cumlDollarCOY2'].apply(lambda x:'{:.2f}'.format(x))
        # KPIPiv.loc['Unit Charge-Off - Year 1'] = KPIPiv.loc['cumlUnitCOM12'].apply(lambda x:'{:.2%}'.format(x))
        # KPIPiv.loc['Unit Charge-Off - Year 2'] = KPIPiv.loc['Year2CumlUnitChargeOffRate'].apply(lambda x:'{:.2%}'.format(x) )
        
        # KPIPiv.loc['BookedAccounts'] = KPIPiv.loc['NewAccInd']
        # KPIPiv.loc['GrossRevenue'] = KPIPiv.loc['GrossRevenue']
        # KPIPiv.loc['NetRevenue'] = KPIPiv.loc['NetRevenue']
        # KPIPiv.loc['Customer Service'] = KPIPiv.loc['Customer Service']
        # KPIPiv.loc['Collections (Pre-Call and 5-30)'] = KPIPiv.loc['Collections (Pre-Call and 5-30)']
        # KPIPiv.loc['Credit Protection Expense'] = KPIPiv.loc['Credit Protection Expense']
        # KPIPiv.loc['Other Overhead'] = KPIPiv.loc['Other Overhead']
        # KPIPiv.loc['Total Servicing Expense'] = KPIPiv.loc['Total Servicing Expense']
        # KPIPiv.loc['Cost of Funds - Debt Expense'] = KPIPiv.loc['Cost of Funds - Debt Expense']
        # KPIPiv.loc['One Time - Marketing Expense (CPA)'] = KPIPiv.loc['One Time - Marketing Expense (CPA)']
        # KPIPiv.loc['Fraud Loss Expense'] = KPIPiv.loc['Fraud Loss Expense']
        # KPIPiv.loc['Pre-Tax Income'] = KPIPiv.loc['Pre-Tax Income']

        # desiredOrder = ['MonthsOnBooks', 'CumlROA', 'cumlPTI', 'cumlER', '30+UnitM3', '30+UnitM4', 'cumlUnitCOM12', 'Year2CumlUnitChargeOffRate', 'CumlROAMonth3','Month6CumulativeROA','Month12CumulativeROA', 'Month24CumulativeROA', 'cumlPTIPerBooked12', 'cumlPTIPerBooked24']
        # desiredOrder = ['30+UnitM3', '30+UnitM4', 'cumlUnitCOM12', 'Year2CumlUnitChargeOffRate', 'CumlROAMonth3','Month6CumulativeROA','Month12CumulativeROA', 'Month24CumulativeROA', 'cumlPTIPerBooked12', 'cumlPTIPerBooked24']
        # desiredOrder = ['30+ Unit Rate - MOB 3', '30+ Unit Rate - MOB 4', 'Unit Charge-Off - Year 1', 'Unit Charge-Off - Year 2', 'ROA - MOB 3', 'ROA - MOB 6','ROA - MOB 12', 'ROA - MOB 24', 'PTI per Booked - MOB 12', 'PTI per Booked - MOB 24']
        desiredOrder = ['cumlNewAcc', 'GrossRevenue', 'NetRevenue', 'Customer Service', 'Collections (Pre-Call and 5-30)','Collections (60+)'
                        ,'Credit Protection Expense','Other Overhead','Total Servicing Expenses','Cost of Funds - Debt Expense'
                        ,'One Time - Marketing Expense (CPA)','Fraud Loss Expense','Pre-Tax Income', 'Average Balance per Booked'
                        ,'Cumulative ROA', 'Cuml. Payments per Booked Account', 'Cuml. Purchases per Booked Account', 'Average ACE Score', 'Average Credit Line per Booked']

        
        # Reindex the pivot table to the desired order
        KPIPiv = KPIPiv.reindex(desiredOrder)
        KPIPiv2 = KPIPiv2.reindex(desired_order2)

        
        KPIPivCol = KPIPiv.columns[0]
        if not st.session_state['KPI_DF'].empty:
            if KPIPivCol in st.session_state['KPI_DF'].columns:
                newName=f"{selList}{st.session_state['counter']}"
                st.session_state['counter']+=1
                KPIPiv.columns = [newName]
            else:
                newName = KPIPivCol
        else: 
            newName = KPIPivCol
            
        if st.session_state['KPI_DF'].empty:
            st.session_state['KPI_DF'] = KPIPiv.copy()
        else:
            current_df = st.session_state['KPI_DF'].copy()
            # current_dfCol = current_df.columns[0]
            st.session_state['KPI_DF'] = pd.concat([current_df, KPIPiv], axis=1)

            st.session_state['KPI_DF']['diffs'] = 0
            for index in st.session_state['KPI_DF']['diffs'].index:
            # for col in st.session_state['KPI_DF'].columns:
                st.session_state['KPI_DF'].loc[index, 'diffs'] = (st.session_state['KPI_DF'].loc[index, st.session_state['KPI_DF'].columns[1]] 
                                                   - st.session_state['KPI_DF'].loc[index, st.session_state['KPI_DF'].columns[0]])
            # st.session_state['KPI_DF']['diffs'] = (st.session_state['KPI_DF'].loc['cumlNewAcc', st.session_state['KPI_DF'].columns[1]] 
            #                                        - st.session_state['KPI_DF'].loc['cumlNewAcc', st.session_state['KPI_DF'].columns[0]])
            # for col in KPIPiv.columns:
            # # Ensure the column exists in both DataFrames and calculate the difference
            #     # if col in current_df.columns and col in KPIPiv.columns:
            #     # if col in current_dfCol.columns and col in KPIPiv.columns:
            #     diff_col_name = f"{col}_diff_{st.session_state['counter']}"
            #     st.write(col)
            #     st.write(KPIPiv[col])
            #     st.write(diff_col_name)
            # for col in current_df.columns:
            #     st.write(col)
            #     st.write(current_df[col])
            # for col in st.session_state['KPI_DF'].columns:
            #     diff1 = current_df[col]
            #     st.write(diff1)
                # diff2 = KPIPiv[col]
                # st.session_state['KPI_DF'] = pd.concat([current_df, KPIPivCol, diff], axis=1)
                # st.session_state['KPI_DF'] = pd.concat([diff1, diff2], axis=1)
        
                # st.session_state['KPI_DF'][diff_col_name] = current_df[col] - KPIPiv[col]
                # st.session_state['counter'] +=1
    
        
        # if st.session_state['KPI_DF'].empty == False:
        #     if KPIPivCol in st.session_state['KPI_DF'].columns:
        #         # newName=f"{KPIPivCol}{selList}{st.session_state['counter']}"
        #         newName=f"{selList}{st.session_state['counter']}"
        #         st.session_state['counter']+=1
        #         KPIPiv.columns = [newName]
        #     else:
        #         newName = KPIPivCol
        # else: 
        #     newName = KPIPivCol


        # if st.session_state['KPI_DF'].empty:
        #     st.session_state['KPI_DF'] = KPIPiv
        # else:
        #     st.session_state['KPI_DF'] = pd.concat([st.session_state['KPI_DF'], KPIPiv], axis=1)
        #     for col in KPIPiv.columns:
        #         if col in st.session_state['KPI_DF'].columns:
        #             # Create a unique name for the difference column
        #             diff_col_name = f"{col}_diff_{st.session_state['counter']}"
        #             st.session_state['KPI_DF'][diff_col_name] = st.session_state['KPI_DF'][col] - KPIPiv[col]
        # st.session_state['counter'] +=1
            
            # st.session_state['KPI_DF'] = KPIPiv['cumlNewAcc'] - KPIPiv['cumlNewAcc']
            # st.session_state['KPI_DF'] = pd.concat([st.session_state['KPI_DF'], result['Differences']], axis=1)


    # result = result[result['NewAccInd', 'ActiveAccInd', 'TotalPayments', 'TotalPaymentsAdj', 'TotalNetSales', 'Ace2', 'Ace2Ind', 'EndingReceivable', 'CreditLine', 'PreTaxIncome'
    #                 , 'ChargeOffs', 'Unwinds', 'ChargeOffPrincipalAmount', 'FraudAmt', 'FraudCnt', 'GrsRev', 'TotalFinanceCharges', 'cumlNewAcc', 'cumlActiveAcc', 'cumlPTI', 'cumlER', 'cumlCO'
    #                 , 'cumlUnwind', 'CumlNetChargeOffs', 'cumlNetPayments', 'cumlTtlNetSales', 'cumlFraudCnt', 'cumlGrsRev', 'cumlFraudAmt', 'cumlTtlFinCharge', 'avgActives', 'avgReceivable'
    #                 , 'cumlPTIPerBooked', 'MonthsOnBooks', 'CumlROA', 'CumlROAAnnual', 'UnitChargeOffRate', 'CumlUnitChargeOffRate', 'CumlNetChargeOffRate', 'cumlPmtsPerBookedAcct'
    #                 , 'AvgEndBalPerBookedAcct', 'cumlPurPBookedAcct', 'AvgAce2Score', 'avgBalPActive', 'cumlGrossRevpBooked', 'cumlFraudRate', 'AvgPmtPerActive', 'CumlNetFraudDollRate'
    #                 , 'cumlFinChargePBooked', 'NetChargeOff', 'netPayments', 'curr5', 'fiveThirty', 'ThirtySixty', 'SixtyNinety', 'Ninety120', 'rate120150+', 'rate150-CO']]


    return result, st.session_state['KPI_DF'], KPIPiv2

