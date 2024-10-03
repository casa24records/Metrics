import base64
import requests
import webbrowser
import json
from urllib.parse import urlencode
from flask import Flask, request, redirect

# Reemplaza estos valores con tus datos de Spotify for Developers
CLIENT_ID = '737e719bb4c4413dab75709796eea4f5'     # Tu Client ID
CLIENT_SECRET = '2257b35c9acb46ea817f4a99cf833a8c'  # Tu Client Secret
REDIRECT_URI = 'http://localhost:5000/callback'     # Debe coincidir con lo configurado en Spotify Dashboard
SCOPE = 'user-read-private user-read-recently-played playlist-read-private'  # Scopes (permisos)
STATE = '34fFs29kd09'  # Cualquier valor único para asegurar la autenticidad de la solicitud

app = Flask(_name_)

# Paso 1: Redirigir al usuario a la página de autorización de Spotify
@app.route('/login')
def login():
    auth_url = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
        'state': STATE
    }
    webbrowser.open(f"{auth_url}?{urlencode(params)}")
    return 'Por favor, inicia sesión en Spotify.'

# Paso 2: Recibir el código de autorización y solicitar el Access Token
@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()
    access_token = token_info['access_token']

    # Guardar el access token para usar en las próximas peticiones
    return redirect(f"/get_user_info?access_token={access_token}")

# Paso 3: Hacer una solicitud autenticada a la API de Spotify
@app.route('/get_user_info')
def get_user_info():
    access_token = request.args.get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    # Obtener información básica del usuario
    user_info_response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_info = user_info_response.json()
    
    # Obtener las playlists privadas del usuario
    playlists_response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
    playlists = playlists_response.json()

    return json.dumps({
        'user_info': user_info,
        'playlists': playlists
    }, indent=2)

if _name_ == '_main_':
    app.run(debug=True)
