set - a
source .env
set +a
streamlit run --server.enableCORS=false --server.port=8051 --server.address=localhost main.py