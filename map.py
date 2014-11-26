#!/usr/bin/python3
from barclay import load_stations


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
	print("""
<circle
       style="opacity:1;fill:none;stroke:#ff8800;stroke-width:2"
       cx="%f"
       cy="%f"
       r="3.0" />
""" % ((s['long'] - mean_long) * 5000 + 500, -(s['lat'] - mean_lat) * 5000 + 500))

print("""
  </g>
</svg>
""")


