from __future__ import print_function
import ephem
import webbrowser

NINETY = ephem.degrees(90)

def closest_point_to_saturn():
	jupiter = ephem.Jupiter()
	obs = ephem.Observer()
	now = ephem.now()

	def decimal_range(start, stop, step):
		"""Decimal range"""
		i = start
		while i < stop:
			yield i
			i += step

	def calculate_best(min_lat=-90, max_lat=90, min_lon=-180, max_lon=180, step=10):
		"""Finds Pluto's observed altitude that is closest to 90 degrees among lat/lon points"""
		best_altitude = 0
		best_azmuth = None
		best_latitude = None
		best_longitude = None


		# calculates latitude and longitude from observer point of view for each step (or planetary movement)
		for latitude in decimal_range(min_lat, max_lat+1, step):
			for longitude in decimal_range(min_lon, max_lon+1, step):
				obs.lon = str(longitude)
				obs.lat = str(latitude)
				obs.date = now
				jupiter.compute(obs) # returns pluto's altitude and azmuth

				if abs(jupiter.alt - NINETY) < abs(best_altitude - NINETY):
					best_altitude = jupiter.alt
					best_azmuth = jupiter.az 
					best_latitude = latitude
					best_longitude = longitude

		return best_latitude, best_longitude

	best_latitude, best_longitude = calculate_best()
	last_step = 10
	for step in [1, 0.1, 0.01]:
		best_latitude, best_longitude = calculate_best(best_latitude-last_step, best_latitude+last_step,
													   best_longitude-last_step, best_longitude+last_step,
													   step)
		last_step = step
	return best_latitude, best_longitude

if __name__ == '__main__':
	latitude, longitude = closest_point_to_saturn()

	open_street_map = "https://www.openstreetmap.org/?mlat={0}&mlon={1}#map=3/{0}/{1}"
	url = open_street_map.format(latitude, longitude)
	print(url)

	# opens link in new tab
	webbrowser.open(url, new=2)
