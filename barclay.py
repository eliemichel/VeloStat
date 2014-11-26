#!/usr/bin/python3
import re
from datetime import datetime
from lxml.etree import parse, XMLParser
import numpy as np



def load_csv(filename, limit=None, parse=0):
	"""Load data from csv file with the following format:
	Rental Id,Duration,Bike Id,End Date,EndStation Id,EndStation Name,Start Date,StartStation Id,StartStation Name
	Ignore wrong lines.
	@param filename: Path to csv file
	@param limit=None: Maximum amount of processed lines
	@param parse=0: Parse integers and datetime. Takes about 10 times more time. 0 for no parsing. 1 for parse int only. 2. for parse all
	"""
	f = open(filename)

	line_parser = re.compile(r'^(?P<RentalId>\d*),(?P<Duration>\d*),(?P<BikeId>\d*),(?P<EndDate>\d\d/\d\d/\d\d\d\d \d\d:\d\d),(?P<EndStationId>\d*),"(?P<EndStation>[^"]*)",(?P<StartDate>\d\d/\d\d/\d\d\d\d \d\d:\d\d),(?P<StartStationId>\d*),"(?P<StartStation>[^"]*)"$')

	data = []
	it = 0

	for l in f:
		m = line_parser.match(l)
		if m is not None:
			d = m.groupdict()
			if parse > 0:
				d['RentalId'] = int(d['RentalId'])
				d['BikeId'] = int(d['BikeId'])
				d['EndStationId'] = int(d['EndStationId'])
				d['StartStationId'] = int(d['StartStationId'])
			if parse > 1:
				d['EndDate'] = datetime.strptime(d['EndDate'], '%d/%m/%Y %H:%M')
				d['StartDate'] = datetime.strptime(d['StartDate'], '%d/%m/%Y %H:%M')
			data.append(d)
		it += 1
		if limit is not None and it > limit:
			break

	f.close()

	return data



def load_stations(filename='data/livecyclehireupdates.xml'):
	"""Load data about stations from XML given in live data.
	Returns a list with fields 'lat', 'long' and 'id'.
	@param filename='data/livecyclehireupdates.xml': live data filename
	"""
	xml = XMLParser()

	stations_file = open(filename)
	stations_data = parse(stations_file, xml)

	stations = []
	new_station = {}

	for s in stations_data.xpath("//station/lat|//station/long|//station/id|//station/name"):
		new_station[s.tag] = s.text if s.tag == 'name' else float(s.text)
		if ('lat' in new_station and 'long' in new_station and 'id' in new_station and 'name' in new_station):
			stations.append(new_station)
			new_station = {}

	stations_file.close()

	return stations




def make_travel_histogram(src, hist=None):
	"""Make an histogram with hourly buckets during weekdays and week-end of bikes travels
	@param src: Source file from which import data
	@param hist: Base histogram (set to None tu initialize a new one)
	"""
	if hist == None:
		max_station = 800
		hist = np.ndarray([3, 24, max_station, max_station])

	data = load_csv(src, None, 2)

	for l in data:
		weekday = l['StartDate'].weekday()
		day_axis = max(0, weekday - 4) # 0, 1 or 2

		hour_axis = l['StartDate'].hour % 24

		hist[day_axis][hour_axis][l['StartStationId']][l['EndStationId']] += 1

	return hist

