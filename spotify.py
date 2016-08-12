"""
Mitch Olson
Spotify Alarm Tool
Aug 9, 2016

PR UPDATES: Ryan Schachte
"""

import subprocess
import argparse
import schedule
import time
import sys
import requests
import random

def get_args():
    '''This function parses and return arguments passed in'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Script to randomize Spotify song input on alarm time')
    # Add arguments
    parser.add_argument(
        '-t', '--time', type=str, help='Alarm Clock Time : xx:xx', required=True)
    parser.add_argument(
        '-s', '--song', type=str, help='Play a specific song : SONG_NAME', required=False, default="False", nargs='+')
    parser.add_argument(
        '-a', '--artist', type=str, help='Play from specific artist : ARTIST_NAME', required=False, default="False", nargs='+')
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    time = args.time
    song_name = args.song
    artist_name = args.artist
    # Return all variable values
    return time, song_name, artist_name

def song_to_id(song_name):
	'''Parse song ID from search endpoint'''

	song_search = ''
	#Turn list into query param
	for name in song_name:
		song_search += name + '%20'

	r = requests.get('https://api.spotify.com/v1/search?q=%s&type=track&market=US&limit=1'%(song_search)).json()
	song_id = r['tracks']['items'][0]['external_urls']['spotify'].split('/')[-1:]

	#Formatting shit
	song_id = song_id[0].encode('ascii','ignore')

	return song_id

def artist_to_id(artist_name):
	'''Parse artist ID from search endpoint'''
	artist_search = ''
	#Turn list into query param
	for name in artist_name:
		artist_search += name + '%20'

	r = requests.get('https://api.spotify.com/v1/search?q=%s&type=artist'%(artist_search)).json()
	artist_id = r['artists']['items'][0]['external_urls']['spotify'].split('/')[-1:]

	#Formatting shit
	artist_id = artist_id[0].encode('ascii','ignore')

	return artist_id

def randomize_artist_input(artist_name):
	'''Randomizes song input utilizing the spotify API'''
	artist_id = artist_to_id(artist_name)
	r = requests.get('https://api.spotify.com/v1/artists/%s/top-tracks?country=US'%(artist_id)).json()

	#GET a random top song from user-requested artist
	random_track_selection = random.randint(0, 11)

	return r['tracks'][random_track_selection]['id']


def play_song(track_id):
	'''Runs some AppleScript to send a command to Spotify'''

	script = """ osascript -e '
		tell application "Spotify"
		  play track "spotify:track:%s"
		end tell'
	"""
	subprocess.Popen(script % track_id, shell=True)

if __name__ == "__main__":

	try:
		alarm_time, song, artist = get_args()

		if (artist != "False"):
			#Randomize top song from a specified artist
			track_id = randomize_artist_input(artist)
			schedule.every().day.at(alarm_time).do(play_song, track_id)

		elif(song != "False"):
			#Play a specific song
			song_id = song_to_id(song)
			schedule.every().day.at(alarm_time).do(play_song, song_id)

		else:
			print('No valid input specified')

		while True:
			try:
				schedule.run_pending()
				time.sleep(60)
			except KeyboardInterrupt:
				print("\nYou killed the alarm!")
				break
	except Exception:
		print("Error occured during Spotify search")
