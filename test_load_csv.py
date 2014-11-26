#!/usr/bin/python3

from barclay import load_csv, load_stations

station_occurrences = {}

data = load_csv('data/barclayscyclehireusagestats/1. Journey Data Extract 01Jan-05Jan13.csv', None, 1)

for l in data:
	station_occurrences[l['StartStationId']] = station_occurrences.get(l['StartStationId'], 0) + 1
	station_occurrences[l['EndStationId']] = station_occurrences.get(l['EndStationId'], 0) + 1




stations = load_stations()

mean_lat = sum([s['lat'] for s in stations]) / len(stations)
mean_long = sum([s['long'] for s in stations]) / len(stations)



print("""
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="200mm"
   height="200mm"
   id="carte"
   version="1.1"
   viewBox="0 0 1000 1000">

  <g id="stations">
""")

for s in stations:
	r = station_occurrences.get(int(s['id']), -1)
	c = 'rgb('+str(255-int(r/10))+','+str(int(r/5))+',0)' if r >= 0 else '#ff0000'
	print("""
<circle
       style="opacity:1;stroke:none;fill:%s;stroke-width:2"
       cx="%f"
       cy="%f"
       r="%f" />
""" % (c, (s['long'] - mean_long) * 5000 + 500, -(s['lat'] - mean_lat) * 5000 + 500, r * 0.02 + 0.2) )


stations = { int(s['id']): (s['long'], s['lat']) for s in stations }

for l in data:
	s1 = stations.get(int(l['StartStationId']))
	s2 = stations.get(int(l['EndStationId']))
	if s1 is not None and s2 is not None:
		x1, y1 = s1
		x2, y2 = s2
		c = "rgba(0,0,0,0.01)"
		print("""
<line
       x1="%f"
       y1="%f"
       x2="%f"
       y2="%f"
       stroke-width="1"
       stroke="%s" />
	""" % ((x1 - mean_long) * 5000 + 500, (y1 - mean_lat) * 5000 + 500, (x2 - mean_long) * 5000 + 500, (y2 - mean_lat) * 5000 + 500, c))

print("""
  </g>
</svg>
""")




