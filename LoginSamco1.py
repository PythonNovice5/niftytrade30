from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import requests
import time
import json

samco=StocknoteAPIPythonBridge()

login=samco.login(body={"userId":'DE30090','password':'Eshant@0587','yob':'1987'})
print("Login details",login)


#Converting Login string response to json
login_response = json.dumps(login)
#final_login_response = json.loads(login_response)

final_login_response = json.loads(login)
print(type(final_login_response))

f = open("/home/egarg0587/stocktesting/token.txt", "w")
f.write(final_login_response['sessionToken'])
f.close()
