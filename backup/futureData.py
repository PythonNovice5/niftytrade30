from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import requests
import time
samco=StocknoteAPIPythonBridge()
import json
import websocket,csv
import pandas as pd 
# import websockets
#login=samco.login(body={"userId":'DE30090','password':'Eshant@0587','yob':'1987'})
#print("Login details",login)
#print(type(login))


#this will return a user details and generated session token
f = open("token.txt", "r")
access_token = f.read()

print("Access token: "+access_token)


samco.set_session_token(sessionToken=access_token)
headers = {
  'Accept': 'application/json',
  'x-session-token': access_token
}

print ("\n\n")





def on_message(ws, msg):
    final_dictionary = eval(msg)
    a=final_dictionary['response']['data']['ltp']
    b=final_dictionary['response']['data']['lTrdT']
    #print(a,b)
    # file_path = 'filewrite.txt' #choose your file path
    # with open(file_path, "a") as output_file:
    #     output_file.write(msg)

    with open('filewriteIndex.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a, b])
        


def on_error(ws, error):
    print (error)

def on_close(ws):
    print ("Connection Closed")

def on_open(ws):
    print ("Sending json")
    data='{"request":{"streaming_type":"quote", "data":{"symbols":[{"symbol":"50836_NFO"}]}, "request_type":"subscribe", "response_format":"json"}}'
    ws.send(data)
    ws.send("\n")
 

headers = {'x-session-token':access_token}

websocket.enableTrace(True)

ws = websocket.WebSocketApp("wss://stream.stocknote.com", on_open = on_open, on_message = on_message, on_error = on_error, on_close = on_close, header = headers)
ws.run_forever()



