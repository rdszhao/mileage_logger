import requests
import streamlit as st

def submit(name, email, craft, activity, debug=False):
	distance = round(float(activity['distance']) / 1609, 2)
	year, month, day= activity['start_date'].split('T')[0].split('-')
	link = f"https://www.strava.com/activities/{activity['id']}"
	values = [email, month, day, year, name, distance, 'mi', craft, link]

	real_keys = [
					'emailAddress',
					'entry.356064094_month',
					'entry.356064094_day',
					'entry.356064094_year',
					'entry.62320042',
					'entry.773830580',
					'entry.1113937566',
					'entry.140974962',
					'entry.1879621063'
				]

	real_url = 'https://docs.google.com/forms/d/e/1FAIpQLScYWifg5Jo3fsqVNOEqk3qQWyQECQLuQLy7676zrWDy2vzZ6A'
	debug_url = 'https://docs.google.com/forms/d/e/1FAIpQLScOYnuZ4QeLqNsT3iVo5AMmWWEXAeaPmjEOcZ3S8w6WcNgioQ'

	debug_keys = [
					'entry.994557902',
					'entry.1719691460_month',
					'entry.1719691460_day',
					'entry.1719691460_year',
					'entry.1807340436',
					'entry.1393364025',
					'entry.109338008',
					'entry.1290157805',
					'entry.256374288'
				]

	if debug:
		url = f"{debug_url}/formResponse"
		data = dict(zip(debug_keys, values))
	else:
		url = f"{real_url}/formResponse"
		data = dict(zip(real_keys, values))

	response = requests.post(url, data=data)

	if response.status_code == 200:
		st.markdown('__activity submitted!__')
		st.write(f"_date_: {month}-{day}-{year}")
		st.write(f"_distance_: {distance} mi")
	else:
		st.markdown('__submission failed__')
		st.write("_seems like something's not working right now_")
		st.write("_contact someone on staff so we can fix this_")
		st.write(response.status_code, response.reason)
	if debug:
		st.write(response.status_code, response.reason)
		st.write(data)
		print(response.content)