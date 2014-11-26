#!/usr/bin/python3
import re
from datetime import datetime


def load_csv(filename, limit=None, parse=False):
	f = open(filename)

	# Rental Id,Duration,Bike Id,End Date,EndStation Id,EndStation Name,Start Date,StartStation Id,StartStation Name
	line_parser = re.compile(r'^(?P<RentalId>\d*),(?P<Duration>\d*),(?P<BikeId>\d*),(?P<EndDate>\d\d/\d\d/\d\d\d\d \d\d:\d\d),(?P<EndStationId>\d*),"(?P<EndStation>[^"]*)",(?P<StartDate>\d\d/\d\d/\d\d\d\d \d\d:\d\d),(?P<StartStationId>\d*),"(?P<StartStation>[^"]*)"$')

	f.readline()
	data = []
	it = 0

	for l in f:
		m = line_parser.match(l)
		if m is not None:
			d = m.groupdict()
			if parse:
				d['RentalId'] = int(d['RentalId'])
				d['BikeId'] = int(d['BikeId'])
				d['EndStationId'] = int(d['EndStationId'])
				d['StartStationId'] = int(d['StartStationId'])
				d['EndDate'] = datetime.strptime(d['EndDate'], '%d/%m/%Y %H:%M')
				d['StartDate'] = datetime.strptime(d['StartDate'], '%d/%m/%Y %H:%M')
			data.append(d)
		it += 1
		if limit is not None and it > limit:
			break

	f.close()

	return data

if __name__ == '__main__':
	d = load_csv('data/barclayscyclehireusagestats/1. Journey Data Extract 01Jan-05Jan13.csv')
