from .core import _getAllData, _searchAircaft, _sorter, _radar

def Flight(flightId):
	query = _searchAircaft(flightId.upper())

	if not query:
		return False

	data = _getAllData(query['id'])

	if not data:
		return False

	return _sorter(data, query, flightId)

def radar(north, south, west, east):
	if type(north) != type(1) and type(north) != type(0.1): return False 
	if type(south) != type(1) and type(south) != type(0.1): return False 
	if type(west) != type(1) and type(west) != type(0.1): return False 
	if type(east) != type(1) and type(east) != type(0.1): return False 

	return _radar(north, south, west, east)