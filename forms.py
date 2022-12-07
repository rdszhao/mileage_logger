from requests import post

def submit(name, email, craft, activity, debug=False):
	distance = round(float(activity['distance']) / 1609, 2)
	year, month, day= activity['start_date'].split('T')[0].split('-')
	link = f"https://www.strava.com/activities/{activity['id']}"
	values = [email, month, day, year, name, distance, 'mi', craft,link]

	real_keys = ['emailAddress', 'entry.356064094_month', 'entry.356064094_day', 'entry.356064094_year', 'entry.62320042', 'entry.773830580', 'entry.1113937566', 'entry.140974962', 'entry.1879621063']
	debug_keys = ['entry.565666177', 'entry.1161307666_month', 'entry.1161307666_day', 'entry.1161307666_year', 'entry.1564166327', 'entry.652460081', 'entry.226956376', 'entry.1024488085', 'entry.136322056']
	real_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeYnetUQ5T1BHD5JHm3TNZ6myEgEvP2JwfJD_Sa16l7xVeaAg'
	debug_url = 'https://docs.google.com/forms/d/e/1FAIpQLSdMf1jraG5M9v4JYUlzH69V9Y5QzPQzdz0a39X_ia4gHtJW7Q'

	if debug:
		url = f"{debug_url}/formResponse"
		entries = dict(zip(debug_keys, values))
	else:
		url = f"{real_url}/formResponse"
		entries = dict(zip(real_keys, values))
	post(url, data=entries)