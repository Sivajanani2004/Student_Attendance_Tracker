FROM python:3.11-slim
WORKDIR /app
RUN pip install --upgrade pip
COPY frontend/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]
