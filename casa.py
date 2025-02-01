import requests
from bs4 import BeautifulSoup
import re

# Function to scrape Spotify artist page
def get_spotify_data(spotify_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(spotify_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        
        # Extract Monthly Listeners
        listeners_match = re.search(r"(\d[\d,.]*) monthly listeners", text)
        monthly_listeners = listeners_match.group(1) if listeners_match else "Not Found"
        
        # Extract Popularity Score (Spotify doesn't show this directly)
        popularity_score = "Requires API or deeper scraping"
        
        return {"Monthly Listeners": monthly_listeners, "Popularity Score": popularity_score}
    else:
        return {"Error": "Failed to fetch page"}

# Function to scrape Instagram followers
def get_instagram_followers(instagram_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(instagram_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        
        # Extract followers count using regex
        followers_match = re.search(r"(\d[\d,.]*) Followers", text)
        followers = followers_match.group(1) if followers_match else "Not Found"
        
        return {"Instagram Followers": followers}
    else:
        return {"Error": "Failed to fetch page"}

# Function to scrape Discord invite page for member count
def get_discord_members(discord_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(discord_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        
        # Extract Discord members
        members_match = re.search(r"(\d[\d,.]*) Members", text)
        members = members_match.group(1) if members_match else "Not Found"
        
        return {"Discord Members": members}
    else:
        return {"Error": "Failed to fetch page"}

# URLs
spotify_url = "https://open.spotify.com/artist/2QpRYjtwNg9z6KwD4fhC5h"
instagram_url = "https://www.instagram.com/casa24records/?hl=en"
discord_url = "https://discord.gg/Y7C2uzmb"

# Fetch data
spotify_data = get_spotify_data(spotify_url)
instagram_data = get_instagram_followers(instagram_url)
discord_data = get_discord_members(discord_url)

# Display results
print("Spotify Data:", spotify_data)
print("Instagram Data:", instagram_data)
print("Discord Data:", discord_data)
