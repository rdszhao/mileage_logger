export APP_URL='http://localhost:8051'
export STRAVA_CLIENT_ID=60423
export STRAVA_CLIENT_SECRET='70452786e2068633e53d1a4e0fb13e674cda6380'
streamlit run --server.enableCORS false --server.port=8051 --server.address=localhost main.py