import base64
import requests
import pandas as pd
from datetime import datetime
import os

# ------------------ CONFIGURACIÓN ------------------

# Spotify API Credentials
CLIENT_ID = '737e719bb4c4413dab75709796eea4f5'     # Aquí pones tu Client ID de Spotify
CLIENT_SECRET = '2257b35c9acb46ea817f4a99cf833a8c'  # Aquí pones tu Client Secret de Spotify

# YouTube API Credentials (Solo para Casa24)
YOUTUBE_API_KEY = 'AIzaSyCgffLM7bMJ2vqw-VBGaNNJWkMQPEfNfgk' # API Key de YouTube
YOUTUBE_CHANNEL_ID = 'UCshvYG0n1I_gXbM8htuANAg' # Channel ID de Casa24
CASA24_ID = '2QpRYjtwNg9z6KwD4fhC5h'         # ID de Spotify de Casa24

# ------------------ FUNCIONES ------------------

def get_spotify_token():
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
        'artist_name': artist_data.get('name', ''),
        'popularity_score': artist_data.get('popularity', 0),
        'followers': artist_data.get('followers', {}).get('total', 0)
    }

def get_youtube_channel_data():
    """Obtiene información del canal de YouTube: suscriptores, total de vistas y número de videos."""
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={YOUTUBE_CHANNEL_ID}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        stats = data['items'][0]['statistics']
        return {
            'youtube_subscribers': int(stats.get('subscriberCount', 0)),  # FORZAR A ENTERO
            'youtube_total_views': int(stats.get('viewCount', 0)),        # FORZAR A ENTERO
            'youtube_video_count': int(stats.get('videoCount', 0))        # FORZAR A ENTERO
        }
    else:
        return {
            'youtube_subscribers': None,
            'youtube_total_views': None,
            'youtube_video_count': None
        }

def store_popularity_scores(artists_data):
    """Almacena los datos de los artistas en un archivo CSV sin incluir artist_id."""
    csv_file = 'popularity_scores.csv'
    df = pd.DataFrame(artists_data)

    # EXCLUIR LA COLUMNA "artist_id"
    df = df.drop(columns=['artist_id'], errors='ignore')

    # FORZAR QUE LAS COLUMNAS DE YOUTUBE SEAN ENTEROS Y NO FLOAT CON PUNTO CERO
    df[['youtube_subscribers', 'youtube_total_views', 'youtube_video_count']] = df[
        ['youtube_subscribers', 'youtube_total_views', 'youtube_video_count']
    ].fillna(0).astype(int)  # AQUÍ SE CAMBIA PARA FORZAR ENTEROS

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, mode='a', header=True, index=False)
    else:
        df.to_csv(csv_file, mode='a', header=False, index=False)

# ------------------ PROCESO ------------------

# Lista de IDs de artistas en Spotify
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
spotify_token = get_spotify_token()

# Obtener datos de los artistas en Spotify
artists_data = [{'artist_id': artist_id, **get_artist_data(artist_id, spotify_token)} for artist_id in artist_ids]

# Obtener datos del canal de YouTube (solo para Casa24)
youtube_data = get_youtube_channel_data()

# Agregar información de YouTube solo a Casa24
for artist in artists_data:
    if artist['artist_id'] == CASA24_ID:
        artist.update(youtube_data)
    else:
        artist.update({'youtube_subscribers': None, 'youtube_total_views': None, 'youtube_video_count': None})

    artist['date'] = datetime.now().strftime('%Y-%m-%d')  # Agregar fecha

# Almacenar los datos en un archivo CSV sin la columna 'artist_id'
store_popularity_scores(artists_data)

# Imprimir los datos obtenidos (sin mostrar el artist_id)
for artist in artists_data:
    print(f"Artist: {artist['artist_name']}, Popularity: {artist['popularity_score']}, Followers: {artist['followers']}, "
          f"YouTube Subscribers: {artist['youtube_subscribers']}, YouTube Total Views: {artist['youtube_total_views']}, "
          f"YouTube Video Count: {artist['youtube_video_count']}")
