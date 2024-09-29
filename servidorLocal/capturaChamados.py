import requests as r,  json,  dotenv , os


id_projeto = '10000'
#10003 é referente a suporte
id_tarefa = '10003'

dotenv.load_dotenv(dotenv.find_dotenv())

url = os.getenv("URL")
token = os.getenv("TOKEN")
login = os.getenv("LOGIN")


headers = {
    "Accept":"application/json",
    "Content-Type":"application/json",
}

query = url + "/rest/api/3/search?jql=project=TAG"

response = r.request(
    "GET", 
    query,
    headers=headers,
    auth= r.auth.HTTPBasicAuth(login,token)
)


data = json.loads(response.text)
issues = data['issues']
total_de_issues = data['total']
numero_iteracoes = int(total_de_issues/50)+1 if total_de_issues <= 50 else 1
print(issues[0])



