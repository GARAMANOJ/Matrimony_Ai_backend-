FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app folder
COPY app ./app

# Copy everything else
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000"]

