# this module can be imported to create pop token for given URL

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

# create pop token for a give URL path that could be used for subsequent calls
def create_pop(url):
  dictJWTBody = {}
  if 'apigee.net' in url:
    uri = url.split("apigee.net",1)[1]
  else:
    uri = url

  dictJWTBody["URI"] = uri
  # strSigned would be the pop token generated for the particular URI endpoint we have generated
  strSigned = create_jwt(dictJWTBody,strPrivate)
  # strDecode is the decoded pop token, good for validation etc.
  strDecode = jwt.decode(strSigned,strPublic,algorithms=["RS256"])
  return  strSigned

