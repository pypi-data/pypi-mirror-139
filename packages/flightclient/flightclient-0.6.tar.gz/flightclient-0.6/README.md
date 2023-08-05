# flightclient.py  
Aircraft Tracking Library (unofficial Flightradar24 client)

### Installation
```$ pip3 install flightclient```
              or
```$ python3 setup.py install```

### Usage
Getting flight data
```python
import flightclient

plane = 'SK4756'
flight = flightclient.Flight(plane)

print(flight.position)
```  
Getting planes into a geographic bounding box (in decimal degrees)
```python
import flightclient

north, south, west, east = 53.51, 50.981, 9.128, 14.582
result = flightclient.radar(north, south, west, east)

print(result)
```  
