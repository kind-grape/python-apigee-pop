# this module can be imported to create access token which is used for sunsequent API calls as bearer authorization token

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

# import required variables from common variables
from common_vars import *

def create_jwt(dictPara,strPrivate):
  # need to check if private key has been loaded as str obj
  if not strPrivate:
    print ('Private key string obj strPrivate has not been loaded, exiting')
    quit()
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

def access_token():
  dictJWTBody = {}
  dictJWTBody["URI"] = "/oauth2/v6/tokens"
  # strSigned would be the pop token generated for the particular URI endpoint we have generated
  strSigned = create_jwt(dictJWTBody,strPrivate)
  # strDecode is the decoded pop token
  strDecode = jwt.decode(strSigned,strPublic,algorithms=["RS256"])
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

  #print (accessToken)
  return accessToken     




    
