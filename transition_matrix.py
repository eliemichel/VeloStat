#!/usr/bin/python3
from barclay import make_travel_histogram
import pickle


hist = make_travel_histogram('data/barclayscyclehireusagestats/1. Journey Data Extract 01Jan-05Jan13.csv')
hist = make_travel_histogram('data/barclayscyclehireusagestats/1. Journey Data Extract 04Jan-31Jan 12.csv', hist)


with open('transition.dump', 'wb') as f:
	pickle.dump(hist, f)

