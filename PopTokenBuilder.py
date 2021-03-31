import jwt
import time
import hashlib
import base64
import uuid
import sys

lstSysArg = sys.argv
iSysArgLen = len(lstSysArg)

def getInput(strPrompt):
  if sys.version_info[0] > 2 :
    return input(strPrompt)
  else:
    print("Please upgrade to Python 3")
    sys.exit()

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

def main():
  objPrivate = open("C:/Users/user/OneDrive - T-Mobile USA/DevProjects/Pier2.0/patoolspriv.pem","r")
  objPublic  = open("C:/Users/user/OneDrive - T-Mobile USA/DevProjects/Pier2.0/patoolspublic.pem","r")
  objSecret  = open("C:/Users/user/OneDrive - T-Mobile USA/DevProjects/Pier2.0/TopSecret.txt","r")
  strPrivate = objPrivate.read()
  strPublic  = objPublic.read()
  strSecret  = objSecret.read()
  dictJWTBody = {}
  if iSysArgLen > 1:
    strUseCase = lstSysArg[1]
  else:
    print ("No use case provided. Use parameter OAuth, Start or Search to specify use case")
    strUseCase = getInput("Please specify OAuth, Start or Search use case: ")
  
  print ("Got use case of {}".format(strUseCase))

  if strUseCase.lower() == "oauth":
    bAuthHash = base64.b64encode(strSecret.encode("utf-8"))
    dictJWTBody["URI"] = "/oauth2/v6/tokens"
    dictJWTBody["Authorization"] = "Basic " + bAuthHash.decode("utf-8")
  elif strUseCase.lower() == "search":
    dictJWTBody["URI"] = "/itsm/change/v2/CR000344228"
    dictJWTBody["user-id"] = "user"
    dictJWTBody["consumer-name"] = "DSO Cyber Defense"
    dictJWTBody["Accept"] = "application/json"
    dictJWTBody["Content-Type"] = "application/json"
  elif strUseCase.lower() == "start":
    dictJWTBody["URI"] = "/itsm/change/v2/CR000344228/start"
    dictJWTBody["user-id"] = "user"
    dictJWTBody["Content-Type"] = "application/json"
  else:
    print ("User case of '{}' is not supported!".format(strUseCase))
    sys.exit()
  
  strSigned = CreateJWT(dictJWTBody,strPrivate)

  print ("\n{}\n".format (strSigned))

  strDecode = jwt.decode(strSigned,strPublic,algorithms=["RS256"])
  print (strDecode)

if __name__ == '__main__':
  main()
