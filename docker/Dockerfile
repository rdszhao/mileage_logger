FROM python:3.9
EXPOSE 8501
# RUN git clone https://github.com/rdszhao/mileage_logger.git /app
WORKDIR /app
COPY . /app/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "main.py", "--server.address=localhost", "--server.enableCORS=false"]