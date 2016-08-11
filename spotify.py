"""
Mitch Olson
Spotify Alarm Tool
Aug 9, 2016
"""

import subprocess
import schedule
import time
import sys

def play_song(track_id):
	#Runs some AppleScript to send a command to Spotify
	script = """osascript -e 'tell application "Spotify" to play track "%s"'"""
	subprocess.Popen(script % track_id, shell=True)

if __name__ == "__main__":
	args = sys.argv
	alarm_time = args[1]
	track_id = args[2]
	schedule.every().day.at(alarm_time).do(play_song, track_id)
	while True:
		try:
			schedule.run_pending()
			time.sleep(60)
		except KeyboardInterrupt:
			print("\nYou killed the alarm!")
			break


