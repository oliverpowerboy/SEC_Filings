import requests
import pprint as pp
import json
import pandas as pd

MICROSOFT_CIK = "CIK0000789019"

MICROSOFT_URL = f"https://data.sec.gov/submissions/{MICROSOFT_CIK}.json"

MICROSOFT_FACTS = f"https://data.sec.gov/api/xbrl/companyfacts/{MICROSOFT_CIK}.json"

# SEC has a max acess rate of 10 requests per second for everyone
# They also ask to declare the user agent in the form : Sample Company Name AdminContact@<sample company domain>.com
# However since I am accessing as an indiviual I provided my name and private email instead

headers={"User-Agent" : "Oliver De Fusco oliverd@live.co.uk"}

def get_repsonse_SEC(url,headers,filename):

    response = requests.get(url=url, headers=headers)

    with open(f"{filename}.json","w") as f:

        json.dump(response.json(), f,indent=4)


#get_repsonse_SEC(MICROSOFT_URL, headers, "microsoft response")
#get_repsonse_SEC(MICROSOFT_FACTS, headers, "microsoft facts")

with open("microsoft response.json") as json_file:

    data = json.load(json_file)
    
report_types = data["filings"]["recent"]["form"]
report_file = data["filings"]["recent"]["accessionNumber"]

forms = {"file" : report_file, "type" : report_types}

df = pd.DataFrame(forms)

filt = (df["type"] == "10-Q")

print(df[filt])