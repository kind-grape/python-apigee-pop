import get_access
import get_pop
import requests


# access token has validity of 1 hour
accessTok = get_access.access_token()

popTok = get_pop.create_pop('https://tmobilea-sb02.apigee.net/api/asset-portfolio/v1/business-application-by-level?type=A')

# access api endpoints using python request lib
headers = {
'X-Authorization': popTok,
'Authorization': 'Bearer '+ accessTok,
}
url = "https://tmobilea-sb02.apigee.net/api/asset-portfolio/v1/business-application-by-level?type=A"
payload={}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)