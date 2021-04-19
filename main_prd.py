import pop_util_prd
import requests


# access token has validity of 1 hour
accessTok = pop_util_prd.access_token()

url = 'https://core.saas.api.t-mobile.com/api/asset-portfolio/v2/associated-assets?asset_akm_id=APM0201207'

popTok = pop_util_prd.create_pop(url)

# access api endpoints using python request lib
headers = {
'X-Authorization': popTok,
'Authorization': 'Bearer '+ accessTok,
}
url = url
payload={}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)