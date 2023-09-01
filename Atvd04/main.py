import requests
import json

api_key = "769c9bb"

# URL da API para obter info sobre o filme Avatar
url = f"http://www.omdbapi.com/?apikey={api_key}&t=Avatar"

# Faz a solicitação à API
response = requests.get(url)
data = response.json()

# Verifica se a resposta contém informações
if "Title" in data:
    # Converte os dados em JSON
    json_data = json.dumps(data, indent=4)

    # Salva os dados em um arquivo JSON
    with open("avatar_data.json", "w") as json_file:
        json_file.write(json_data)

    print("Dados salvos em avatar_data.json")
else:
    print("Informações ausentes na resposta da API.")
