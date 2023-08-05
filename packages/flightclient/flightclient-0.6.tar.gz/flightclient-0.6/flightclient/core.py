from .helpers import request

class Flight():

	def __init__(self, position, dataId, callsign, path, flight, route,
		live, model, image, 
		airline, origin,
		destination, firstTimestamp, time):

		self.callsign, self.path = callsign, path
		self.live, self.model = live, model
		self.image, self.flight, self.route = image, flight, route
		self.airline, self.origin = airline, origin
		self.destination, self.firstTimestamp = destination, firstTimestamp
		self.time, self.dataId = time, dataId
		self.position = position

	def __repr__(self):
		return f'Flight({self.flight}: {self.route if self.route else "Path unavailable"})'

	def updatePath(self):
		try:
			self.path = request(
				'https://data-live.flightradar24.com/clickhandler',
				params = {'version': '1.5', 'flight': self.dataId}
			).json()['trail']
			self.position = self.path[0]
			return True
		except:
			return False

def _searchAircaft(aircraft):
	response = request(
		'https://www.flightradar24.com/v1/search/web/find',
		params = {'query': aircraft, 'limit': 50}
	).json()
	
	if not response['results']:
		return False

	result = None
	for flight in response['results']:
		if flight['type'] == 'live':
			result = flight
			break

	if not result:
		result = response['results'][0]

	return result

def _getAllData(flightId):
	try:
		return request(
			'https://data-live.flightradar24.com/clickhandler',
			params = {'version': '1.5', 'flight': flightId}
		).json()
	except:
		return False

def _sorter(data, query, flight):
	try:
		dataId = data['identification']['id']
	except:
		dataId = None

	try:
		callsign = data['identification']['callsign']
	except:
		callsign = None
	
	try:
		path = data['trail']
	except:
		path = None

	try:
		flight = flight
	except:
		flight = None

	try:
		route = query['detail']['route'].replace('⟶', '-')
	except:
		route = None
	
	try:
		live = data['status']['live']
	except:
		live = None
	
	try:
		model = data['aircraft']['model']['text']
	except:
		model = None
	
	try:
		image = data['aircraft']['images']['large'][0]['src']
	except:
		image = None
	
	try:
		airline = data['airline']['name']
	except:
		airline = None
	
	try:
		origin = data['airport']['origin']
	except:
		origin = None
	
	try:
		destination = data['airport']['destination']
	except:
		destination = None
	
	try:
		firstTimestamp = data['firstTimestamp']
	except:
		firstTimestamp = None

	try:
		time = data['time']
	except:
		time = None

	try:
		position = data['trail'][0]
	except:
		position = None

	return Flight(position, dataId, callsign, path, 
		flight, route,
		live, model, image, 
		airline, origin,
		destination, firstTimestamp, time)

def _radar(north, south, west, east):
	bounds = map(str, [north, south, west, east])
	result = []
	response = request(
		'https://data-live.flightradar24.com/zones/fcgi/feed.js',
		params = {
			'faa': 1,
			'bounds': ','.join(bounds),
			'satellite': 1,
			'mlat': 1,
			'flarm': 1,
			'adsb': 1,
			'gnd': 1,
			'air': 1,
			'vehicles': 1,
			'estimated': 1,
			'maxage': 14400,
			'gliders': 1,
			'stats': 1
		}
	)
	
	try:
		response = response.json()
	except:
		return False

	for elem in response:
		if elem in ['version', 'full_count', 'stats']:
			continue

		result.append({response[elem][13] if response[elem][13] else response[elem][0]: {'callsign': response[elem][0], 'lat': response[elem][1], 'lon': response[elem][2]}})

	return result