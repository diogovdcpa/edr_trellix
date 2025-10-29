import os
import requests
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


"""
curl --location --request POST 'https://auth.trellix.com/auth/realms/IAM/protocol/openid-connect/token' --header 'Content-Type: application/x-www-form-urlencoded' --header 'Authorization: Basic <Base64 Encoded CLIENT_ID:CLIENT_SECRET>' --data-urlencode 'grant_type=client_credentials' --data-urlencode 'scope=<Scope required(space separated)>'
"""


def get_trellix_token(client_id, client_secret, scope):
    """
    Obtém token de acesso da API Trellix usando client credentials.
    
    Args:
        client_id (str): Client ID para autenticação
        client_secret (str): Client Secret para autenticação
        scope (str): Escopos necessários (separados por espaço)
    
    Returns:
        dict: Resposta da API contendo o token de acesso
    """
    
    # URL da API de autenticação
    url = 'https://auth.trellix.com/auth/realms/IAM/protocol/openid-connect/token'
    
    
    # Headers da requisição
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    # Dados do corpo da requisição
    data = {
        'grant_type': 'client_credentials',
        'scope': scope
    }
    
    try:
        # Fazer a requisição POST
        response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
        
        # Verificar se a requisição foi bem-sucedida
        response.raise_for_status()
        
        # Retornar a resposta JSON
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status code: {e.response.status_code}")
            print(f"Resposta: {e.response.text}")
        return None


def get_edr_alerts(access_token, params=None):
    """
    Obtém lista de dispositivos da API Trellix ePO.
    
    Args:
        api_key (str): Chave da API Trellix
        access_token (str): Token de acesso Bearer
        params (dict, optional): Parâmetros de query para a requisição
    
    Returns:
        dict: Resposta da API contendo os dispositivos
    """
    
    # URL da API de dispositivos
    url = 'https://api.manage.trellix.com/edr/v2/alerts'
    
    # Headers da requisição
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'x-api-key': os.getenv("trellix_api"),
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        # Fazer a requisição GET
        response = requests.get(url, headers=headers, params=params)
        
        # Verificar se a requisição foi bem-sucedida
        response.raise_for_status()
        
        # Retornar a resposta JSON
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status code: {e.response.status_code}")
            print(f"Resposta: {e.response.text}")
        return None

# Exemplo de uso:
if __name__ == "__main__":
    # Substitua com suas credenciais reais
    CLIENT_ID = os.getenv("client_id")
    CLIENT_SECRET = os.getenv("secret")
    SCOPE = os.getenv("scope")
    
    # Obter token
    token_response = get_trellix_token(CLIENT_ID, CLIENT_SECRET, SCOPE)
    token = token_response.get('access_token')
    
    if token_response:
        # print(f"Access Token: {token_response.get('access_token')}")
        alerts = get_edr_alerts(token).get('data')
        pprint(alerts)

        
    else:
        print("Falha ao obter token")