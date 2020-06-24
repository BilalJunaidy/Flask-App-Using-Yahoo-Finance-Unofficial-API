import requests
import json
import sys


def lookup(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

    querystring = {"symbol":f"{symbol}"}

    headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "67a4c7d659msh81246b43815e2fcp1664e2jsnaba909eaa91d"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if len(response.text) == 0:
        print("error")
        return None
    else:
        return 1
    
def lookup_year_end(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

    querystring = {"symbol":f"{symbol}"}

    headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "67a4c7d659msh81246b43815e2fcp1664e2jsnaba909eaa91d"
    }

    response = requests.get(url, headers=headers, params=querystring)    
    data = json.loads(response.text)
    list_of_dicts = data["incomeStatementHistory"]["incomeStatementHistory"]
    list = []
    number_of_years = len(list_of_dicts)

    for i in range(number_of_years):
        list.append(list_of_dicts[i]["endDate"]["fmt"])

    return list
    
def IncomeStatement(symbol, IS_years_selected):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

    querystring = {"symbol":f"{symbol}"}

    headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "67a4c7d659msh81246b43815e2fcp1664e2jsnaba909eaa91d"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    data_orig = data["incomeStatementHistory"]["incomeStatementHistory"]

    for i in range(4):
        data_orig[i]["endDate"]["longFmt"] = data_orig[i]["endDate"]["fmt"]
        print(data_orig[i]["endDate"]["longFmt"])
    
    data_list = data_orig[0]
    data_list.pop('maxAge')
    data_list.pop('ebit')
    data_list = list(data_orig[0])
    

    reformat_list = [7,15, 17, 6, 5, 0, 8, 10, 9, 14, 11, 12, 13, 1, 20, 19, 4, 3, 21]
    FSA_list = []
    for i in reformat_list:
        FSA_list.append(data_list[i])
    print("Income Statement FSA_list: ")
    print(FSA_list)

    IS_record_row = []

    for i in range(len(FSA_list)):
        record = []
        record.append(f"{FSA_list[i]}")
        for n in IS_years_selected:
            try:
                record.append(data_orig[n][f"{FSA_list[i]}"]['longFmt'])
            except KeyError:
                record.append(0)

        IS_record_row.append(record)

    return IS_record_row
    

def BalanceSheet(symbol, BS_years_selected):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

    querystring = {"symbol":f"{symbol}"}

    headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "67a4c7d659msh81246b43815e2fcp1664e2jsnaba909eaa91d"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    
    data_orig = data["balanceSheetHistory"]["balanceSheetStatements"]
    for i in range(4):
        data_update = data_orig[i]
        data_update.pop('maxAge')
        data_update["endDate"]["longFmt"] = data_update["endDate"]["fmt"]

        # Adding OtherCurrentAssets into the list of balance sheet FSA
        TotalCA = convert_str_to_float(data_update["totalCurrentAssets"]["longFmt"])
        TotalCash = convert_str_to_float(data_update["cash"]["longFmt"])
        try:
            TotalInventory = convert_str_to_float(data_update["inventory"]["longFmt"])
        except KeyError:
            TotalInventory = 0
        try:
            TotalAR = convert_str_to_float(data_update["netReceivables"]["longFmt"])
        except KeyError:
            TotalAR = 0
        OtherCA = TotalCA - TotalCash - TotalAR - TotalInventory
        print("OtherCA: ")
        print(OtherCA)
        #data_update["otherCurrentAssets"]["LongFmt"] = OtherCA
        print("OtherCA inputted: ")
        #print(data_update["otherCurrentAssets"]["LongFmt"])

        # Updating the value of Other Current Liabilities 
        AP = convert_str_to_float(data_update["accountsPayable"]["longFmt"])
        TotalCL = convert_str_to_float(data_update["totalCurrentLiabilities"]["longFmt"])
        try:
            TotalShortLTD = convert_str_to_float(data_update["shortLongTermDebt"]["longFmt"])
        except KeyError:
            TotalShortLTD = 0
            
        otherCL = TotalCL - AP - TotalShortLTD

        print("OtherCL value: ")
        print(otherCL)

        
        print("Other CL value before insertion: ")
        print(data_update["otherCurrentLiab"]["longFmt"])        
        data_update["otherCurrentLiab"]["longFmt"] = str(otherCL)
        print("Other CL value after insertion: ")
        print(data_update["otherCurrentLiab"]["longFmt"])

        # Adding Long term Liabilities into the list of balance sheet FSA
        TotalLiab = convert_str_to_float(data_update["totalLiab"]["longFmt"])
        LTLiab = TotalLiab - TotalCL
        data_update["LongTermLiabilities"] = {}
        data_update["LongTermLiabilities"]["longFmt"] = str(LTLiab)

        #Adding sum of total equity and total liabilities
        TotalEquity = convert_str_to_float(data_update["totalStockholderEquity"]["longFmt"])
        TotalEquityAndLiabilities = TotalLiab + TotalEquity
        data_update["TotalEquityAndLiabilities"] = {}
        data_update["TotalEquityAndLiabilities"]["longFmt"] = str(TotalEquityAndLiabilities)        
    
    data_list = list(data_orig[0])
    print("Length of data list: ")
    print(len(data_list))
    print("printing the original balance sheet data list")
    print(data_list)

    reformat_list = [4, 11,20, 22, 6, 19, 16, 15, 10, 17, 3, 23, 2, 13, 12, 21, 8,0, 5, 9, 7, 1, 25]
    print("Length of reformat list: ")
    print(len(reformat_list))
    FSA_list = []
    for i in reformat_list:
        FSA_list.append(data_list[i])
##        except IndexError:
##            FSA_list.append()
    print("Balance Sheet FSA_list: ")
    print(FSA_list)

    #Creating record of balance sheet that is to be returned to the application.py function
    BS_record_row = []
    for i in range(len(FSA_list)):
        record = []
        record.append(f"{FSA_list[i]}")
        for n in BS_years_selected:
            try:
                record.append(data_orig[n][f"{FSA_list[i]}"]['longFmt'])
            except KeyError:
                record.append(0)
        BS_record_row.append(record)

    return BS_record_row



def convert_str_to_float(str):
    n = str.count(",")
    return float(str.replace(",", "", n))

