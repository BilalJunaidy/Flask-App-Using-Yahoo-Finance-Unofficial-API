import requests
import json
import sys


def lookup(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

    querystring = {"symbol":f"{symbol}"}

    headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "481e4dbd2emsh9e7780b1882918ap101e23jsneab53031dd60"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if len(response.text) == 0:
        print("error")
        return None
    
    data = json.loads(response.text)
    statement = "IncomeStatement"
    
    

    if statement == "IncomeStatement":
        data_update = data["incomeStatementHistory"]["incomeStatementHistory"][0]
        data_update.pop('maxAge')
        data_update.pop('ebit')
        data_update["endDate"]["longFmt"] = data_update["endDate"]["fmt"]
        
        data_list = list(data["incomeStatementHistory"]["incomeStatementHistory"][0])

        reformat_list = [7,15, 17, 6, 5, 0, 8, 10, 9, 14, 11, 12, 13, 1, 20, 19, 4, 3, 21]
        FSA_list = []
        for i in reformat_list:
            FSA_list.append(data_list[i])
        print(FSA_list)

       ##The following can be removed from the flask version. 
##        for i in range(len(FSA_list)):
##            print(i, end=" ")
##            print(FSA_list[i], end = "  " )
##            print("$ ", end="")
##            try:
##                print(data_update[f"{FSA_list[i]}"]["longFmt"])
##            except KeyError:
##                print("0")
        return 1

            
            
    if statement == "BalanceSheet":
        data_update = data["balanceSheetHistory"]["balanceSheetStatements"][0]
        data_update.pop('maxAge')
        data_update["endDate"]["longFmt"] = data_update["endDate"]["fmt"]

        # Adding OtherCurrentAssets into the list of balance sheet FSA
        TotalCA = convert_str_to_float(data_update["totalCurrentAssets"]["longFmt"])
        TotalCash = convert_str_to_float(data_update["cash"]["longFmt"])
        TotalAR = convert_str_to_float(data_update["netReceivables"]["longFmt"])
        OtherCA = TotalCA - TotalCash - TotalAR
        print(OtherCA)
        data_update["OtherCurrentAssets"] = {}
        data_update["OtherCurrentAssets"]["LongFmt"] = str(OtherCA)
        print(data_update["OtherCurrentAssets"]["LongFmt"])

        # Updating the value of Other Current Liabilities 
        AP = convert_str_to_float(data_update["accountsPayable"]["longFmt"])
        TotalCL = convert_str_to_float(data_update["totalCurrentLiabilities"]["longFmt"])
        otherCL = TotalCL - AP
        data_update["otherCurrentLiab"]["longFmt"] = str(otherCL)

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
        
        data_list = list(data_update)
        
        reformat_list = [5, 10,16, 18, 14, 0, 13, 9, 4, 17, 3, 11, 19, 1, 6, 8, 7, 2, 20]
        FSA_list = []
        for i in reformat_list:
            FSA_list.append(data_list[i])
        print(FSA_list)

        
        print(data_update)
        print(data_list)


        ##The following can be removed from the flask version.

        for i in range(len(data_list)):
            print(i, end=" ")
            print(f"{data_list[i]}", end = " ")
            print("$ ", end="")
            try:
                print(data_update[f"{data_list[i]}"]["longFmt"])
            except KeyError:
                print("1110")

        ## BalanceSheet FSA List format
                ##5th - 0th 
                ##10th - 1st 
                ##16th - 2nd
                ##18th - 3rd 
                ##14th - 4th - TOtal current assets 
                ##0th - 5th  
                ##13th - 6th  
                ##9th - 7th
                ##4th - 8th 
                ##17th - 9th 
                ##3rd - 10th 
                ##11th - 11th 
                ##19th - 12th 
                ##1st - 13th 
                ##6th - 14th 
                ##8th - 15th 
                ##7th - 16th 
                ##2nd - 17th 
                ##20th - 18th 



    
        
    if statement == "CashflowStatement":
        data = data["cashflowStatementHistory"]["cashflowStatements"][0]
        print(data)
        data_update = list(data)
        for i in range(len(data_update)):
            print(data_update[i])


def convert_str_to_float(str):
    n = str.count(",")
    return float(str.replace(",", "", n))

##def IncomeStatement():
##    pass
##

## Create a new list, and copy element from the old list into the new one. This is for Income Statement. 
        ## 7th - 0th
        ## 15th - 1st
        ## 17th - 2nd
        ## 6th - 3rd
        ## 5th - 4th
        ## 0th - 5th
        ## 8th - 6th
        ## 10th - 7th
        ## 9th - 8th
        ## 14th - 9th 
        ## 11th - 10th
        ## 12th - 11th 
        ## 13th - 12th
        ## 1st - 15th
        ## 20st - 16th 
        ## 19th - 17th
        ## 4th - 18th
        ## 3rd - 19th
        ## 21nd - 20th 
        
##
##def BalanceSheet():
##    pass
##
##
##
##def CashFlow():
##    pass
def lookup_year_end(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-financials"

    querystring = {"symbol":f"{symbol}"}

    headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "481e4dbd2emsh9e7780b1882918ap101e23jsneab53031dd60"
    }

    response = requests.get(url, headers=headers, params=querystring)    
    data = json.loads(response.text)
    list_of_dicts = data["incomeStatementHistory"]["incomeStatementHistory"]
    list = []
    number_of_years = len(list_of_dicts)

    for i in range(number_of_years):
        list.append(list_of_dicts[i]["endDate"]["fmt"])

    print(list)
    print(type(list))
    return list
        

    
    
