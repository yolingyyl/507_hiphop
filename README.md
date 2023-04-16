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
The API's client_id, client_secret are stored as environment variables.

### Data Structure
The project use tree structure to store the data. Please see `cache.json` file to access tree structure data.

```
{"1990": {
  "2siXUlHrdh3hj9tYK36PGM": [
    "90s & 00s R&B & Hiphop by Olivia", 
      {
        "Your Body": {
          "name": "Your Body", 
          "url": "https://open.spotify.com/track/5y4TDQdYzlT4eoQIPOgNDz", 
          "author": "Pretty Ricky", 
          "duration": 240040
       }, 
    "Let Me Love You": {
      "name": "Let Me Love You", 
      "url": "https://open.spotify.com/track/5WphWTUIfRe7x8NZss79cY", 
      "author": "Mario", 
      "duration": 249093
      }
    }
  ], 
 "37i9dQZF1DX186v583rmzp": [
    "I Love My '90s Hip-Hop by Spotify",
      {
        "Gangsta's Paradise": {
          "name": "Gangsta's Paradise", 
          "url": "https://open.spotify.com/track/1DIXPcTDzTj8ZMHt3PDt8p", 
          "author": "Coolio", 
          "duration": 240693
          }
        ]
     }, 
 "1970": {...}
}
```

### Interaction
After executing the python file, users can interact with the application using command line. <br>
**Step 1.** The application displays hiphop introduction and different time periods' introduction. <br>
**Step 2.** Users answer the question: Are you interested in any specific time period? Please enter 1970s, 1980s, 1990s or 2000s <br>
**Step 3.** The application displays Spotify Playlists based on the time period. For example: <br>
```
Here are the playlists on Spotify for 1970s:
1: clean radio edits by SOBI  🅴
2: I Love My '80s Hip-Hop by Spotify
3: 1970-1990's R&B/HipHop by BNGTNgirl-InYourArea
4: 70s Mix by Spotify
```

**Step 4.** Users answer the question: Enter the playlist's index number to see more, or enter “quit” to leave the application <br>
**Step 5.** The application displays the tracks under certain playlist. For example: <br>
```
1: STAY (with Justin Bieber) by The Kid LAROI
2: As It Was by Harry Styles
3: Numb by Marshmello
```

**Step 6.** Users answer the question: Enter the track's index number to see more, or enter “quit” to leave the application <br>
**Step 7.** If users enter specific index number, the application will open the Spotify's webpage. <br>
