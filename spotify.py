from dotenv import load_dotenv
from dotenv import dotenv_values

import os
import base64
from requests import post
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import requests
from bs4 import BeautifulSoup
import re
import webbrowser

from tkinter import *
import tkinter as tk

#############
### class ###
#############
class Playlist:
    def __init__(self, id = 'No Id', title = "No Title", author = "No Author", url = 'No URL', json = None):
        self.json = json
        if json == None:
            self.id = id
            self.title = title
            self.author = author
            self.url = url
            self.json = json
        else: # from json data
            self.id = json.get('id', id)
            self.title = json.get('name', title)
            if 'owner' in json:
                self.author = json.get('owner')['display_name']
            else:
                self.author = author

            if 'external_urls' in json:
                self.url = json.get('external_urls')['spotify']
            else:
                self.url = "No URL"

    def info(self):
        return f"{self.title} by {self.author}"
    
class Track:
    def __init__(self, title = "No Title", author = "No Author", duration = "No duration", url = 'No URL', json = None):
        self.json = json
        if json == None:
            self.title = title
            self.author = author
            self.duration = duration
            self.url = url
        else: # from json data
            if 'track' in json:
                self.title = json.get('track')['name']
                self.author = json.get('track')['artists'][0]['name'] 
                self.duration = json.get('track')['duration_ms']
                self.url = json.get('track')['external_urls']['spotify']
            else:
                self.title = "No Title"
                self.author = "No Author"
                self.duration = "No duration"
                self.url = 'No URL'


####################
### spotify API  ###
####################

# get credentials from env
env_vars = dotenv_values('.env')
os.environ.update(env_vars)
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# get access token
credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

# spotify API function
def get_playlist(year):
    query = f'hiphop {year}s'
    results = sp.search(q=query, type='playlist', market = 'US', limit=10)
    playlist = results['playlists']['items']
    return playlist

def get_track(playlist_id):
    results = sp.playlist_items(playlist_id, fields=None, limit=10, offset=0, market="US", additional_types=['track'])
    playlist_item = results['items']
    return playlist_item


#######################
### tree and cache  ###
#######################
# cache function

CACHE_FILENAME = "cache.json"

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

spotify_cache = open_cache()

# spotify tree and cache
def track_tree(year, id):
    track_dict = {}
    if year in spotify_cache:
        json = get_track(id)
        for j in json:
            track_title = Track(json = j).title
            if id in spotify_cache[year] and track_title in spotify_cache[year][id]:
                track_dict[track_title] = spotify_cache[year][id][track_title]
            elif id in spotify_cache[year]:
                track_object = Track(json = j)
                track_dict[track_object.title] = {'name': track_object.title, "url": track_object.url, 'author': track_object.author, 'duration': track_object.duration}
                spotify_cache[year][id][track_title] = track_dict[track_object.title]
                save_cache(spotify_cache)
            else:
                track_object = Track(json = j)
                track_dict[track_object.title] = {'name': track_object.title, "url": track_object.url, 'author': track_object.author, 'duration': track_object.duration}
                spotify_cache[year][id] = {}
                spotify_cache[year][id][track_title] = track_dict[track_object.title]
                save_cache(spotify_cache)
    return track_dict


def playlist_tree(year):
    playlist_dict = {}
    if year in spotify_cache:
        for a in get_playlist(year):
            p1 = Playlist(json = a)
            id = p1.id
            if id in spotify_cache[year]: # use id as unique key
                playlist_dict[id] = spotify_cache[year][id]
            else: 
                playlist_dict[id] = (p1.info(),track_tree(year, id))
                spotify_cache[year][id] = playlist_dict[id]
                save_cache(spotify_cache)
    else:
        spotify_cache[year] = {}
        for a in get_playlist(year):
            p1 = Playlist(json = a)
            id = p1.id
            playlist_dict[id] = (p1.info(),track_tree(year, id))
            spotify_cache[year][id] = playlist_dict[id]
            save_cache(spotify_cache)
    return playlist_dict


def year_tree(year, dict):
    if year in spotify_cache:
        dict[year] = spotify_cache[year]
    else:
        dict[year] = playlist_tree(year)
        spotify_cache[year] = dict[year]
        save_cache(spotify_cache)
    return dict

spotify_dict = {}
year_tree('1990', spotify_dict)



########################
### Scrape Wikipedia ###
########################

def scrape_wiki():
    url = 'https://en.wikipedia.org/wiki/Hip_hop_(culture)'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    year_h3 = soup.find_all('h3', string=re.compile(r'\d{4}s'))
# save time-culture introduction to the dictionary
    time_intro = {}
    for year in year_h3:
        p_tag = year.find_next_sibling('p') # find only the first paragraph
        if p_tag:
            content = p_tag.text.strip()
            content = re.sub(r'\[\d{2}\]', '', content) 
            time_intro[year.text.strip()] = content

    # save hiphop intro's first 2 paragraphs
    hiphop_intro = [re.sub(r'\[.*?\]', '', a.text.strip()) for a in soup.find_all('p')[1:3]]
    hiphop_intro_text = hiphop_intro[0] + '\n\n' + hiphop_intro[1]
    return time_intro, hiphop_intro_text


#####################
### Main Function ###
#####################
def main():
    wiki = scrape_wiki()
    print(wiki[1])
    print('\n\n')
    culture = wiki[0]
    for a in culture.items():
        print(f"{a[0]}\n, {a[1]}\n\n")

    year_lst = ['1970s', '1980s', '1990s', '2000s']
    select_year = ''
    while select_year not in year_lst:
        select_year = input('Are you interested in any specific time period? Please enter 1970s, 1980s, 1990s or 2000s: ')
    select_year = select_year[:4]
    print(f"Here are the playlists on Spotify for {select_year}s:")
    spotify_dict = {}
    year_tree(select_year, spotify_dict)
    ind = 1
    playlist_index = {}
    for i in spotify_dict[select_year].items():
        print(f"{ind}: {i[1][0]}")
        playlist_index[ind] =i[0]
        ind += 1
    try: 
        ans = input('\n\nEnter the playlist\'s index number to see more, or enter “quit” to leave the application: ')
        if ans.isdigit() is True:
            track_ind = int(ans)
            if track_ind in playlist_index:
                track_index = {}
                ind_t = 1
                track_id = playlist_index[track_ind]
                for t in spotify_dict[select_year][track_id][1]:
                    print(f"{ind_t}: {t} by {spotify_dict[select_year][track_id][1][t]['author']}")
                    track_index[ind_t] = spotify_dict[select_year][track_id][1][t]['url']
                    ind_t += 1
            ans_track = input('\n\nEnter the track\'s index number to see more, or enter “quit” to leave the application: ')
            try:
                if ans_track.isdigit() is True:
                    url = track_index[int(ans_track)]
                    webbrowser.open_new_tab(url)
                elif ans_track.lower() == 'quit':
                    exit()
            except:
                pass
        elif ans.lower() == 'quit':
            exit()
        
    except:
        pass


if __name__ == "__main__":
    main()


