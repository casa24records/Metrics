import base64
import requests
import pandas as pd
from datetime import datetime
import os

# Reemplaza estos valores con tus datos de Spotify for Developers
CLIENT_ID = '737e719bb4c4413dab75709796eea4f5'     # Aquí pones tu Client ID de Spotify
CLIENT_SECRET = '2257b35c9acb46ea817f4a99cf833a8c'  # Aquí pones tu Client Secret de Spotify

def get_token():
    """Obtiene un token de acceso desde la API de Spotify."""
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {'Authorization': f'Basic {auth_header}'}
    data = {'grant_type': 'client_credentials'}

    response = requests.post(auth_url, headers=headers, data=data)
    response_data = response.json()
    
    return response_data['access_token']

def get_artist_data(artist_id, token):
    """Obtiene el nombre, popularidad y seguidores de un artista de Spotify."""
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(url, headers=headers)
    artist_data = response.json()

    return {
        'artist_name': artist_data['name'],
        'popularity_score': artist_data['popularity'],
        'followers': artist_data['followers']['total'],
        'date': datetime.now().strftime('%Y-%m-%d')
    }

def store_popularity_scores(artists_data):
    """Almacena los datos de los artistas en un archivo CSV."""
    csv_file = 'popularity_scores.csv'
    df = pd.DataFrame(artists_data)

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode='a', header=True, index=False)
    else:
        df.to_csv(csv_file, mode='a', header=False, index=False)

# Lista de IDs de artistas que deseas rastrear
artist_ids = [
    '2QpRYjtwNg9z6KwD4fhC5h',  # Casa 24
    '56tisU5xMB4CYyzG99hyBN',  # Chef Lino
    '5BsYYsSnFsE9SoovY7aQV0',  # PYRO
    '2DqDBHhQzNE3KHZq6yKG96',  # bo.wlie
    '4vYClJG7K1FGWMMalEW5Hg',  # Mango Blade
    '3gXXs7vEDPmeJ2HAOCGi8e',  # ZACKO
    '14UWYN8hKe7U5r0Vqe6ztL',  # pax
    '7DFovnGo8GZX5PuEyXh6LV'   # ARANDA
]

# Obtener token de Spotify
token = get_token()

# Obtener datos de los artistas
artists_data = [get_artist_data(artist_id, token) for artist_id in artist_ids]

# Almacenar los datos en un archivo CSV
store_popularity_scores(artists_data)

# Imprimir los datos obtenidos
for artist in artists_data:
    print(f"Artist: {artist['artist_name']}, Popularity: {artist['popularity_score']}, Followers: {artist['followers']}")
