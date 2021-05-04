import csv,requests
import itertools
import pandas as pd 
import json
from datetime import date
import calendar
import time

column_names = ["LTP", "LTT"]
column_names_alert = ["LTP", "SIGNAL","SL"]
 
#this will return a user details and generated session token
f = open("C:/Algo Part 2/token.txt", "r")
access_token = f.read()
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'x-session-token': access_token
} 

# Buy or Sell based on Input
def buy_or_sell(symbol,buyOrSell):
    
 
    requestBody={
    "symbolName": symbol,
    "exchange": "NFO",
    "transactionType": buyOrSell,
    "orderType": "L",
    "quantity": "25",
    "disclosedQuantity": "",
    "price": "800",
    "priceType": "LTP",
    "orderValidity": "DAY",
    "productType": "BO",
    "squareOffValue": "300",
    "stopLossValue": "50",
    "valueType": "Absolute",
    "trailingStopLoss": ""
}
   
  
    r = requests.post('https://api.stocknote.com/order/placeOrderBO', data=json.dumps(requestBody), headers = headers)
    print(r.json())
    print("Order placed successfully!!", price, buyOrSell)
    return (r.json()['status'])

    
# Exit orders at Stoploss
def exitOrderWhenStopLossHit(stopLossPrice):

    time.sleep(3)
    print("Exit Order When SL Hit  Started ..")
    #Get order details in trade book
    r = requests.get('https://api.stocknote.com/trade/tradeBook', headers = headers)
    trade_book= r.json()['tradeBookDetails']
    numOfOrders=len(trade_book)
    print("Number of executed orders today: ",numOfOrders)
    
    # Exit all orders when SL hit
    while (1<2):       
        df = pd.read_csv("filewrite.csv", names=column_names)
        price = df.LTP.to_list()        
        ltp_nifty=price[-1]
        
        if ltp_nifty==stopLossPrice:
            for i in range(0,numOfOrders):                
                order_number = r.json()['tradeBookDetails'][i]['orderNumber']
                print('order number: ',order_number)
                r = requests.delete('https://api.stocknote.com/order/exitBO', params={'orderNumber': order_number}, headers = headers)
            break


def optionContract(optionStrikePrice,optionType):
    
    list_of_expiryDates= []
    d={}
    
    #These lines of code will fetch the required Option Symbol to be traded
    r = requests.get('https://api.stocknote.com/option/optionChain', params={'searchSymbolName': 'NIFTY','exchange':'NFO','strikePrice':optionStrikePrice,'optionType':optionType
    }, headers = headers)
    print(r.json())
    
    for i in (r.json()['optionChainDetails']):
   
        print(i['tradingSymbol'])
        print(i['expiryDate'])
        d[i['expiryDate']] = i['tradingSymbol']
        list_of_expiryDates.append(i['expiryDate'])
   

    list_of_expiryDates.sort()

    d_sorted= dict(sorted(d.items()))
    print(d_sorted.values())
    list_of_contracts = list(d_sorted.values())
    #list_of_expiryDates = list(d_sorted.keys())


    #Skip Thursdays expiry days
    my_date = date.today()
    print(type(my_date))
    day = calendar.day_name[my_date.weekday()]  #'Wednesday'day
    print(day)

    if(day!="Thursday"):
        print("today is"+day)
        current_expiry_contract = list_of_contracts[0]
        print("Expiry contract ############### ",current_expiry_contract)
        return current_expiry_contract
    else:
        next_expiry_contract = list_of_contracts[1]
        return next_expiry_contract


    # expiry dates and contracts
    print(list_of_expiryDates)
    print(list_of_contracts[0]) #Current Expiry
    print(list_of_contracts[1]) #Next Expiry in case of thursday 





def roundup(x):
    if x%50 ==0:
        x_final=x
    else:
        r=x % 50
        x_new=x+50
        x_final = x_new-r
    return int(x_final)
	

def rounddown(x):
    if x%50==0:
        x_final=x
    else:
        r=x%50
        r2=50-r
        x_new=x-50
        x_final=x_new+r2        
    return int(x_final) 


def getStrikePrice(alert_price,alert_signal):
    if (alert_signal=='BUY'):
        return roundup(alert_price)
    if (alert_signal=='SELL'):
        return rounddown(alert_price)    
        
def getOptionContract(optionStrikePrice,alert_signal):
    if (alert_signal=='BUY'):         
        return optionContract(optionStrikePrice,'CE')
    if (alert_signal=='SELL'):
        return optionContract(optionStrikePrice,'PE')
    

# Initiate Trade based on Signal
def initiate_trade(alert_price,alert_signal,option_contract,stopLoss):
    while (1<2):

        df = pd.read_csv("filewrite.csv", names=column_names)
        price = df.LTP.to_list()
        print(price[-1])
        ltp_nifty=price[-1]
        print("Trigger price:",alert_price)
        print("Nifty LTP: ",ltp_nifty)
       

        if alert_signal=='BUY':    
            
          #Fire order when this condition is met
          if (ltp_nifty<=alert_price):            
            print("Initiating the order now ..........")
            order_status=buy_or_sell(option_contract,alert_signal)
            if (order_status!='Failure'):
                exitOrderWhenStopLossHit(stopLoss)                                            
                break
            

        if alert_signal=='SELL':
          if (ltp_nifty>=alert_price):          
            print("Initiating the order now ..........")
            order_status=buy_or_sell(option_contract,alert_signal)
            if (order_status!='Failure'):
                exitOrderWhenStopLossHit(stopLoss)                                                
                break


#Start
df = pd.read_csv("C:/Algo Part 2/Alert.csv", names=column_names_alert)
price = df.LTP.to_list()
signal = df.SIGNAL.to_list()
stopLoss = df.SL.to_list()
print("Alert price: ",price)
print("Alert signal: ",signal)
print("Stop Loss price",stopLoss)
if (price):   
   
    # This is not required as we have only one value in column name LTP   
    alert_price=price[-1]       
    alert_signal = signal[-1]
    
    print("Alert price before initiating a trade: ",alert_price)
    print("Alert signal before initiating a trade: ",alert_signal)  
    
    #The price after rounding to nearest ATM strike
    optionStrikePrice = int(getStrikePrice(alert_price,alert_signal))
    print("optionStrikePrice",optionStrikePrice)
    
    #Option contract based on strike and signal
    option_contract= getOptionContract(optionStrikePrice,alert_signal)
    print("---------------------------",option_contract)
    
    initiate_trade(alert_price,alert_signal,option_contract,stopLoss)





