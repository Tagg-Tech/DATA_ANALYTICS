import requests, json, dotenv , os
from requests.auth import HTTPBasicAuth


#pip install python-dotenv

dotenv.load_dotenv(dotenv.find_dotenv())


baseurl = os.getenv("URL")
url = f'{baseurl}//rest/api/2/issue'
token = os.getenv("TOKEN")
email = os.getenv("LOGIN")
headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

variavel = 'Quinta'
payload=json.dumps(
    {
        "fields":{
            "project":
                {
                    "key":"TAG"
                },
                "summary": "{} task usando REST API".format(variavel),
                "description": "Esse alerta foi criado usando o python",
                "issuetype":{
                    "name":"Support"
                }
        }
    }
)



response = requests.post(url,headers=headers,data=payload,auth=(email,token))


print(response.text)
