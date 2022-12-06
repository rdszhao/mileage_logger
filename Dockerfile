FROM python:3.9

# RUN git clone https://github.com/rdszhao/mileage_logger.git /app
WORKDIR /app
COPY . /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ENV PORT 8501
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]