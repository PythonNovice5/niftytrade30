import requests
import json,csv
#from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
requestBody={
  "symbolName": "BANKNIFTY20OCTFUT",
  "exchange": "NFO",
  "transactionType": "BUY",
  "orderType": "L",
  "quantity": "25",
  "disclosedQuantity": "",
  "price": "20800.00",
  "priceType": "LTP",
  "orderValidity": "DAY",
  "productType": "BO",
  "squareOffValue": "500",
  "stopLossValue": "100",
  "valueType": "Absolute",
  "trailingStopLoss": "0"
}

f = open("token.txt", "r")
access_token = f.read()

print("Access token: "+access_token)

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'x-session-token': access_token
}


def writeToCsv(ltt):
    with open('index_data3.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      writer.writerow([ltt])


#samco=StocknoteAPIPythonBridge()
#samco.set_session_token(sessionToken=access_token)
#print(samco.search_equity_derivative(search_symbol_name="BANKNIFTY20NOVFUT",exchange=samco.EXCHANGE_NFO))
#writeToCsv(samco.search_equity_derivative(search_symbol_name="BANKNIFTY20NOVFUT",exchange=samco.EXCHANGE_NFO))

# print(samco.get_quote(symbol_name="NIFTY BANK",exchange=samco.EXCHANGE_NFO))


r = requests.get('https://api.stocknote.com/quote/getQuote', params={
  'symbolName': 'BANKNIFTY20OCTFUT','exchange':'NFO'}, headers = headers)

print (r.json())







r = requests.post('https://api.stocknote.com/order/placeOrderBO', data=json.dumps(requestBody), headers = headers)
print (r.json())

r = requests.get('https://api.stocknote.com/order/getOrderStatus', params={
  'orderNumber': r.json()['orderNumber']
}, headers = headers)



print("\n")
print (r.json()['statusMessage'])
print("\n")
print (r.json())

