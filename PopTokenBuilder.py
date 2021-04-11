# some of the installation depency required 
# recommend using virtual env so that those dependencies are installed in a controlled manner
# pip install PyJWT
# pip install cryptography
import jwt
import time
import hashlib
import base64
import uuid
import sys
import requests
import json
import os

lstSysArg = sys.argv
iSysArgLen = len(lstSysArg)

# private key and public key are read from the local files in this example
objPrivate = open("/Users/richp/Desktop/hvac_test/new_pop/pop-private-key-pkcs8.pem","r")
objPublic  = open("/Users/richp/Desktop/hvac_test/new_pop/pop-public-key.pem","r")
strPrivate = objPrivate.read()
strPublic  = objPublic.read()

def getInput(strPrompt):
  if sys.version_info[0] > 2 :
    return input(strPrompt)
  else:
    print("Please upgrade to Python 3")
    sys.exit()

# function to create JWT format pop token based on the private key
def CreateJWT(dictPara,strPrivate):
  lstEHTS = []
  strHeaders = ""
  for strKey in dictPara.keys():
    lstEHTS.append(strKey)
    strHeaders += dictPara[strKey]

  strEHTS = ";".join(lstEHTS)
  dictBody = {}
  dictBody["iat"]  = int(time.time())
  dictBody["exp"]  = dictBody["iat"]+120
  dictBody["ehts"] = strEHTS 
  strTemp = base64.urlsafe_b64encode(hashlib.sha256(str(strHeaders).encode("utf-8")).digest())
  strTemp = strTemp.decode("utf-8")
  dictBody["edts"] = strTemp[:-1]
  dictBody["jti"]  = str(uuid.uuid4())
  dictBody["v"] = 1

  strSigned = jwt.encode(dictBody,strPrivate,algorithm="RS256")
  return strSigned

# building pop token for oauth endpoint and generate access token for subsequent calls
def main():
  dictJWTBody = {}
  if iSysArgLen > 1:
    strUseCase = lstSysArg[1]
  else:
    print ("No use case provided. Use parameter OAuth, Start or Search to specify use case")
    strUseCase = getInput("Please specify OAuth, Start or Search use case: ")
  
  print ("Got use case of {}".format(strUseCase))

  if strUseCase.lower() == "oauth":
    dictJWTBody["URI"] = "/oauth2/v6/tokens"

  else:
    print ("User case of '{}' is not supported!".format(strUseCase))
    sys.exit()
  
  # strSigned would be the pop token generated for the particular URI endpoint we have generated
  strSigned = CreateJWT(dictJWTBody,strPrivate)

  #print ("\n{}\n".format (strSigned))
  
  # strDecode is the decoded pop token
  strDecode = jwt.decode(strSigned,strPublic,algorithms=["RS256"])
  #print (strDecode)

  # now generate the access token
  # first need to check if clientID and secret has been set as envVar
  if 'clientID' not in os.environ or 'clientScr' not in os.environ:
    print ('clientID or clientScr env vars are not set, exiting')
    exit()
  clientID = os.environ['clientID']
  clientScr = os.environ['clientScr']
  x_auth_header = strSigned
  auth_header = "Basic " + base64.b64encode((clientID+':'+clientScr).encode("utf-8")).decode("utf-8")
  url = "https://tmobilea-sb02.apigee.net/oauth2/v6/tokens"
  payload = json.dumps({})
  headers = {
  'X-Authorization': x_auth_header,
  'Authorization': auth_header,
  'Content-Type': 'application/json'
}

  response = requests.request("POST", url, headers=headers, data=payload)
  accessToken = response.json()['access_token']

  print (accessToken)
  return accessToken
  
# build canvas API pop token 
def CanvasApiPop():
  # first build the pop token for the asset API end point 
  dictJWTBody = {}
  dictJWTBody["URI"] = "/api/asset-portfolio/v1/business-application-by-level?type=A"
  canvasPop = CreateJWT(dictJWTBody,strPrivate)
  #print (canvasPop)
  #strDecode = jwt.decode(canvasPop,strPublic,algorithms=["RS256"])
  #print (strDecode)
  return canvasPop

def CanvasApi():
  popTok = CanvasApiPop()
  accessToken = main()
  headers = {
    'X-Authorization': popTok,
    'Authorization': 'Bearer '+ accessToken,
  }
  url = "https://tmobilea-sb02.apigee.net/api/asset-portfolio/v1/business-application-by-level?type=A"
  payload={}
  response = requests.request("GET", url, headers=headers, data=payload)
  print(response.text)




#if __name__ == '__main__':
#  main()

CanvasApi()
