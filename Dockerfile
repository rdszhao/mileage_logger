FROM python:3.9

RUN git clone https://github.com/rdszhao/mileage_logger.git .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PORT 8501
EXPOSE 8501

CMD streamlit run --server.enableCORS false --server.port=8501 main.py