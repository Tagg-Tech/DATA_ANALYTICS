# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
#pip install python-dotenv
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())


url = "https://tagtech.atlassian.net//rest/api/2/issue"

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}


payload=json.dumps(
    {
        "fields":{
            "project":
                {
                    "key":"TAG"
                },
                "summary": "Segunda task usando REST API",
                "description": "Esse alerta foi criado usando o python",
                "issuetype":{
                    "name":"Support"
                }
        }
    }
)



response = requests.post(url,headers=headers,data=payload,auth=("",""))


print(response.text)