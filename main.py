import pop_util
import requests


# access token has validity of 1 hour
accessTok = pop_util.access_token()

url = 'https://tmobilea-sb02.apigee.net/api/asset-portfolio/v2/associated-assets?repoId=19397766'

popTok = pop_util.create_pop(url)

# access api endpoints using python request lib
headers = {
'X-Authorization': popTok,
'Authorization': 'Bearer '+ accessTok,
}
url = url
payload={}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)