FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/requirements.txt
 
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
 
COPY . /app/
 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]