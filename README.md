# Hiphop Playlist

Hiphop playlist is an application that introduces hiphop culture to users. Users will be provided a short introduction about different time periods' hiphop culture, and then they can enter specific time period (1970, 1980, 1990, 2000) based on their own preference. After that, the applicaiton will display relative playlists Using Spotify API. Then, if users are still interested in specific playlists, they can enter the index number to see the tracks under the playlist. And, if still interested, the applicaiton will link the users to Spotify's track webpage for more information.

### Required Packages
dotenv, requests, json, spotipy, bs4, re, webbrowser

from dotenv import load_dotenv
from dotenv import dotenv_values
from requests import post
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from bs4 import BeautifulSoup
import re
import webbrowser


### API Requirements
The API's client_id, client_secret are stored in the environment settings.

### Data Structure
The project use tree structure to store the data. Please see cache.json file to access tree structure data.

{"1990": {"2siXUlHrdh3hj9tYK36PGM": ["90s & 00s R&B & Hiphop by Olivia", {"Your Body": {"name": "Your Body", "url": "https://open.spotify.com/track/5y4TDQdYzlT4eoQIPOgNDz", "author": "Pretty Ricky", "duration": 240040}, "Let Me Love You": {"name": "Let Me Love You", "url": "https://open.spotify.com/track/5WphWTUIfRe7x8NZss79cY", "author": "Mario", "duration": 249093}}], "37i9dQZF1DX186v583rmzp": ["I Love My '90s Hip-Hop by Spotify", {"Gangsta's Paradise": {"name": "Gangsta's Paradise", "url": "https://open.spotify.com/track/1DIXPcTDzTj8ZMHt3PDt8p", "author": "Coolio", "duration": 240693}, "No Diggity": {"name": "No Diggity", "url": "https://open.spotify.com/track/6MdqqkQ8sSC0WB4i8PyRuQ", "author": "Blackstreet", "duration": 304600}}]}, "1970": {"6rcJJP64lH6AraqxYQ35OV": ["1970s 80s soul/hiphop by Pete", {"All Night Long - Single Version": {"name": "All Night Long - Single Version", "url": "https://open.spotify.com/track/4giIdAr7Plyu5LQzBOR4FP", "author": "Lionel Richie", "duration": 260493}, "Immigrant Song - Remaster": {"name": "Immigrant Song - Remaster", "url": "https://open.spotify.com/track/78lgmZwycJ3nzsdgmPPGNx", "author": "Led Zeppelin", "duration": 146250}}], "37i9dQZF1DX52C9BnsaFI0": ["70s Rock Drive by Spotify", {"Dream On": {"name": "Dream On", "url": "https://open.spotify.com/track/1xsYj84j7hUDDnTTerGWlH", "author": "Aerosmith", "duration": 267596}}]}}

Interaction
After executing the python file, an interface will pop up and allow user to filter data using a drop dwon lists. There are three filters for user to interact with, they are year, gender and event. There are four options to display results.

Display the game result with a stacked bar chart of medal count of the country.
Display the game result with a stacked bar chart of medal percentage of the country.
Display champions of certain year.
Display champions of certain event.
