import pandas as pd 
import csv
import time


priceAndSignalData=[]

df= pd.read_csv('filewrite.csv',names=['last_price','traded_time'],index_col=1,parse_dates=True)
df=pd.DataFrame(df)
data = df['last_price'].resample('30min').ohlc()
data_5_mins = df['last_price'].resample('5min').ohlc()
num_of_5min_candles = data_5_mins.shape[0]
lines=data.shape[0]
print(data)
print(data_5_mins)

print("Number of records:"+str(lines))
print("Number of 5 min candles:"+str(num_of_5min_candles))


def writeToCsv(trade_price,buyOrSell,stopLossPrice):
    with open('C:\Algo Part 2\Alert.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([trade_price, buyOrSell,stopLossPrice])


#method for first candle
def first_candle():
    base_candle={}
    base_candle = {'open':data['open'][0],'high':data['high'][0],'low':data['low'][0],'close':data['close'][0]}  
    print(base_candle['high'])
    print(base_candle['low'])
    print(base_candle['open'])
    print(base_candle['close'])
    return base_candle

def second_candle():
    sec_candle={}
    try:
        sec_candle = {'open':data['open'][1],'high':data['high'][1],'low':data['low'][1],'close':data['close'][1]} 
    except Exception as e:
        print("Got exception while reading second candle data --",e)
        return None

     
    print("second candle high",sec_candle['high'])
    print("second candle low",sec_candle['low'])
    print("second candle open",sec_candle['open'])
    print("second candle close",sec_candle['close'])
    return sec_candle


def check_setUp(firstCandleData,secondCandleData):

    signal_and_price=[]
    if(secondCandleData==None):
        print(secondCandleData)
        print("\nWaiting for the Second Candle to get completed  ..")
        return False

    if(firstCandleData['close']<firstCandleData['open']):
        first="RED"
    else:
        first="GREEN"

    if(secondCandleData['close']<secondCandleData['open']):
        second="RED"
    else:
        second="GREEN"
    
    # first="GREEN"
    # second="GREEN"

    print("First Candle Color",first)
    print("Second Candle Color",second)

    if(first==second):
        if(first=="RED"):
            print("Short trade, we need return SELL")
            print(min(firstCandleData['low'],secondCandleData['low']))
            signal_and_price = [min(firstCandleData['low'],secondCandleData['low']),"SELL"]
        else:
            print("Long trade, we need return BUY")    
            print(max(firstCandleData['high'],secondCandleData['high']))
            signal_and_price = [max(firstCandleData['high'],secondCandleData['high']),"BUY"]   

    else:
        print("No trade found today in first hour, close PC")


    return signal_and_price
    
    
    

def verify_setup_closing_NIFTY(priceAndSignalData):
    print("price and signal final",priceAndSignalData)
    
    if (priceAndSignalData):
        if (priceAndSignalData==[]):
            print("NO PRICE AND SIGNAL FOUND TO BE TRADED")
            return False
    else:
        return False        
  
    for i in range(12,num_of_5min_candles-1):
        if priceAndSignalData[1]=="BUY":       
            if data_5_mins['close'][i]>priceAndSignalData[0]:
                print("Long Trade Triggered @",priceAndSignalData[0]," with candle number: ",i+1, "with closig price: ", data_5_mins['close'][i])
                # stop_loss_max = priceAndSignalData[0]-data_5_mins['low'][i]
                # stop_loss = min(30,stop_loss_max)
                
                stop_loss_final = data_5_mins['low'][i]
                if (data_5_mins['low'][i] >= priceAndSignalData[0]):
                    stop_loss_final = priceAndSignalData[0]-20       
                writeToCsv(priceAndSignalData[0],"BUY",stop_loss_final)
                break
        if priceAndSignalData[1]=="SELL":
            if data_5_mins['close'][i]<priceAndSignalData[0]:
                print("Short Trade Triggered @",priceAndSignalData[0]," with candle number: ",i+1, "with closig price: ", data_5_mins['close'][i])
                # stop_loss_max = data_5_mins['high'][i]-priceAndSignalData[0]
                # stop_loss = min(30,stop_loss_max)
                stop_loss_final = data_5_mins['high'][i]
                if (data_5_mins['high'][i] <= priceAndSignalData[0]):
                    stop_loss_final = priceAndSignalData[0]+20     
                writeToCsv(priceAndSignalData[0],"SELL",stop_loss_final)
                break



priceAndSignalData = check_setUp(first_candle(),second_candle())
verify_setup_closing_NIFTY(priceAndSignalData)



