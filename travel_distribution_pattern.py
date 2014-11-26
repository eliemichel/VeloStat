#!/usr/bin/python3
from barclay import make_travel_histogram
import pickle
import numpy as np
from sklearn.cluster import KMeans

"""
Axis:
 0: Day of week (0 for Monday-Friday, 1 for Saturday, 2 for Sunday)
 1: Hour (0-23)
 2: start_station_id
 3: end_station_id
"""
day_of_week = 0
hour = 1
start_station = 2
end_station = 3


print("Loading data…")
with open('01Jan-31Jan13.transition.dump', 'rb') as f:
	travel_hist = pickle.load(f)
print("Loaded.")


start_station_hist = travel_hist.sum(axis=end_station)
start_station_pdf = np.einsum('ijk, ik -> ijk', start_station_hist, np.nan_to_num(1 / start_station_hist.sum(axis=hour)))
start_station_cdf = start_station_pdf.cumsum(axis=hour)

estimator = KMeans()
p = estimator.fit_predict(start_station_cdf[0,:, :].T)

print("Result:")
print(p)
