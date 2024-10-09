import requests, dotenv, os
dotenv.load_dotenv(dotenv.find_dotenv())
api_key = os.getenv("TOM_TOKEN")

url = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json'


params = {
    'key': api_key,                  
    'point': '52.123456,4.654321',  
    'unit': 'KMPH'                   
}

response = requests.get(url, params=params)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    
    data = response.json()
    
    print(data)

else:
    print(f"Erro na requisição: {response.status_code}")
