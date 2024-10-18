# sudo systemctl restart OwntoneMeta
# 
# https://github.com/ejurgensen/forked-daapd/blob/master/README_JSON_API.md#updating-a-queue-item
# curl -X PUT "http://10.0.1.2:3689/api/queue/items/now_playing?title=Awesome%20title&artwork_url=http%3A%2F%2Fgyfgafguf.dk%2Fimages%2Fpige3.jpg"
# https://performance-partners.apple.com/search-api
# https://itunes.apple.com/search?term=Reba Mcentire Fancy&entity=song&limit=1&attribute=songTerm


# https://github.com/regosen/get_cover_art/blob/main/get_cover_art/apple_downloader.py#L11

# if returns blank, commercial, mute
# ffprobe https://24443.live.streamtheworld.com/WWDKFMAAC.aac -v quiet -show_entries format_tags=StreamTitle

# http://10.0.1.3:3689/api/queue

import sys, time, json, urllib.request, urllib.parse; 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

this_track = ''
this_artist = ''
this_album = ''
this_art = ''
currentTitle = ''
currentTrack = 0
refresh = False
period = 30

QUERY_TEMPLATE = "https://itunes.apple.com/search?term=%s&media=music&entity=%s"

def getAlbumArt(artist, album, thisType):
	global this_track, this_artist, this_album, this_art, refresh

	url = QUERY_TEMPLATE % (urllib.parse.quote(artist + " " + album), thisType)

	data = json.loads(urllib.request.urlopen(url).read())

	filteredData = [x for x in data['results'] if x['artistName'].lower() == this_artist.lower()]

	sortedData = sorted(filteredData, key=lambda x: x['releaseDate'], reverse=True)
	
	if len(data['results']) > 0:
		this_album = data['results'][0]["collectionName"]
		return data['results'][0]["artworkUrl100"].replace("100x100bb.jpg", "5000x5000bb.jpg")
	else:
		return None

def getCurrent():
# https://www.thecurrent.org/playlist/the-current
	global this_track, this_artist, this_album, this_art, refresh
	print("getCurrent")
	
	url = "https://www.thecurrent.org/playlist/the-current"

	#  driver options boilerplate #
	options = Options()
	options.add_argument("--headless")

	options.add_experimental_option("excludeSwitches", ["enable-automation"])  # automation detection evasion
	options.add_experimental_option('useAutomationExtension', False)  # automation detection evasion

	driver = webdriver.Chrome(options=options)

	driver.get(url)
	html_list = driver.find_element(By.XPATH, "//div[@class='playlist tiles sixup']")
	items = html_list.find_elements_by_tag_name("li")
	for item in items:
		text = item.text
		print(text)
    
	#for thisCard in driver.find_element(By.XPATH, "//div[@class='playlist-card']"):
		print(thisCard.text)
	
	return()
	
	if this_artist != driver.find_element(By.XPATH, "//div[@class='BrightspotPersistentPlayer-programName']").text :
		this_track = "Michigan Radio"
		this_album = "Michigan Radio"
		this_artist = driver.find_element(By.XPATH, "//div[@class='BrightspotPersistentPlayer-programName']").text
		this_art = "https://api.wbez.org/v2/images/6e6a0674-5cf3-4357-8829-a08ba8e618fd.jpg?width=320&height=320&mode=FILL"
		refresh = True
	else :
		refresh = False
		
	return None
	
def getTripleJ():
	global this_track, this_artist, this_album, this_art, refresh
	data = json.loads(urllib.request.urlopen("https://music.abcradio.net.au/api/v1/plays/triplej/now.json").read())

	if 'recording' in data['now']:
		if this_track != data['now']['recording']['title']:
			this_track = data['now']['recording']['title']
		
			if 'metadata' in data['now']['recording']['title']:
				this_track += this_track + "[Ft. " + data['now']['recording']['title']['metadata'] + "]"
			this_album = data['now']['recording']['releases'][0]['title']
			try:
				this_art = data['now']['recording']['releases'][0]['artwork'][0]['url']

			except Exception as err:
				this_art = "https://www.abc.net.au/core-assets/triplej/touchicon-triplej.png"
				print("Artwork unavailable")
			
			this_artist = ""
			for artists in data['now']['recording']['artists']:
				this_artist += artists['name'] + ' '
			refresh = True
		else:
			refresh = False

	else:
		print("No track playing")
		if this_track != "Track":
			this_track = "Track"
			this_album = "Album"
			this_artist = "Artist"
			this_art = "https://www.abc.net.au/core-assets/triplej/touchicon-triplej.png"
			refresh = True

def getMIRadio():
	global this_track, this_artist, this_album, this_art, refresh
	
	url = "https://www.michiganradio.org/"

	#  driver options boilerplate #
	options = Options()
	options.add_argument("--headless")

	options.add_experimental_option("excludeSwitches", ["enable-automation"])  # automation detection evasion
	options.add_experimental_option('useAutomationExtension', False)  # automation detection evasion

	driver = webdriver.Chrome(options=options)

	driver.get(url)

	if this_artist != driver.find_element(By.XPATH, "//div[@class='BrightspotPersistentPlayer-programName']").text :
		this_track = "Michigan Radio"
		this_album = "Michigan Radio"
		this_artist = driver.find_element(By.XPATH, "//div[@class='BrightspotPersistentPlayer-programName']").text
		this_art = "https://api.wbez.org/v2/images/6e6a0674-5cf3-4357-8829-a08ba8e618fd.jpg?width=320&height=320&mode=FILL"
		refresh = True
	else :
		refresh = False

def getWIDR():
	# https://spinitron.com/WIDR/pl/18649360/In-The-Zoo
	global this_track, this_artist, this_album, this_art, refresh
	
	url = "https://spinitron.com/WIDR/pl/18649360/In-The-Zoo"

	#  driver options boilerplate #
	options = Options()
	options.add_argument("--headless")

	options.add_experimental_option("excludeSwitches", ["enable-automation"])  # automation detection evasion
	options.add_experimental_option('useAutomationExtension', False)  # automation detection evasion

	driver = webdriver.Chrome(options=options)

	driver.get(url)
	
	print(driver.find_element(By.XPATH, "//div[@class='spin-item']"))
	exit()
	
	if this_artist != driver.find_element(By.XPATH, "//div[@class='BrightspotPersistentPlayer-programName']").text :
		this_track = "Michigan Radio"
		this_album = "Michigan Radio"
		this_artist = driver.find_element(By.XPATH, "//div[@class='BrightspotPersistentPlayer-programName']").text
		this_art = "https://api.wbez.org/v2/images/6e6a0674-5cf3-4357-8829-a08ba8e618fd.jpg?width=320&height=320&mode=FILL"
		refresh = True
	else :
		refresh = False

def getWUOB():
	# https://woub.org/listen/fmplaylist/
	global this_track, this_artist, this_album, this_art, refresh
	limit = 1
	
	data = json.loads(urllib.request.urlopen("https://api.composer.nprstations.org/v1/widget/51929de0e1c88d8cd4d02426/playlist").read())

	lastTrack = data['playlist'][-1]['playlist'][-1]
	if 'now_playing' in lastTrack:
		if this_track != lastTrack['trackName'] :
			this_track = lastTrack['trackName']
			this_album = lastTrack['collectionName']
			this_artist = lastTrack['artistName']
			try:
				this_art = getAlbumArt(this_artist, this_album, "album")
			except Exception as err:
				print("Nothing found.")
				this_art = ""
			refresh = True
		else:
			refresh = False
	else:
		print("No track playing")
		if this_track != "Track":
			this_track = "Track"
			this_album = "Album"
			this_artist = "Artist"
			this_art = ""
			refresh = True

while True:
	# http://10.0.1.3:3689/api/queue
	ownQueue = json.loads(urllib.request.urlopen("http://10.0.1.3:3689/api/queue").read())
	if len(ownQueue['items']) > 0:
		currentTrack = ownQueue['items'][0]['track_id']
		# currentTitle = ownQueue['items'][0]['title']
	else:
		print("x")
		
	ownPlayer = json.loads(urllib.request.urlopen("http://10.0.1.3:3689/api/player").read())	
	
	if ownPlayer['state'] == "play" :
		if currentTrack == 30677 : # Triple J
			getTripleJ()
			period = 15
			exit()
			
		elif currentTrack == 30901: # The Current
			getCurrent()
			period = 30
				
		#elif currentTrack == 30681 : # WIDR
		#	getWIDR()
		#	period = 30
				
		elif currentTrack == 30682 : # MI Radio
			getMIRadio()
			period = 120
			
		elif currentTrack == 30678 : # Thistle Radio
			if this_artist != ownQueue['items'][0]['artist']:
				this_artist = ownQueue['items'][0]['artist']
				this_track = ownQueue['items'][0]['album']
				this_album = ""
				this_art = getAlbumArt(this_artist, this_track, "song")
				refresh = True
			period = 15
			
		elif currentTrack == 30679 : # HITS 96.5
			if this_artist != ownQueue['items'][0]['artist']:
				if ownQueue['items'][0]['artist'] != "Unknown artist":
					this_artist = ownQueue['items'][0]['artist']
					this_track = ownQueue['items'][0]['album'].split(" f/")[0]
					this_album = ""
					this_art = getAlbumArt(this_artist, this_track, "song")
					refresh = True
			period = 15
			
		elif currentTrack == 30680 : # WOUB - Crossing Boundaries
			getWUOB()
			period = 15
			
		elif currentTrack == 30683 : # WWDK
			if this_artist != ownQueue['items'][0]['artist']:
				if ownQueue['items'][0]['artist'] != "Unknown artist":
					this_artist = ownQueue['items'][0]['artist']
					this_track = ownQueue['items'][0]['album']
					this_album = ""
					this_art = getAlbumArt(this_artist, this_track, "song")
					refresh = True
			period = 15
			
		else:
			period = 15
	else:
		period = 15
		print("x")
		
	if refresh:
		print('Track: ' + this_track)
		print('Album: ' + this_album)
		print("Artists: ", this_artist)
		print("Art URL: ", this_art)

		params = {
			'title':		this_track,
			'album':		this_album,
			'artist':		this_artist,
			'album_artist':		"Album Artist",
			'composer':		"Composer",
			'genre':		"Genre",
			'artwork_url':		this_art
		}

		url_string = urllib.parse.urlencode(params)
		req = urllib.request.Request(url='http://10.0.1.3:3689/api/queue/items/now_playing?' + url_string, method='PUT')
		with urllib.request.urlopen(req) as f:
			pass
		if f.status == 204:
			refresh = False
			# print(f.status)
			# print(f.reason)
	else:
		print("x")
				
	time.sleep(period)
