FROM python:3
RUN apt-get update
RUN apt-get install -y wkhtmltopdf 
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .