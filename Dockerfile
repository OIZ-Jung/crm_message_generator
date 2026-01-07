FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 9000
CMD ["streamlit","run","test.py","--server.port=9000","--server.address=0.0.0.0"]