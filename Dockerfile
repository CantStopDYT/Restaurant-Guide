FROM python:slim

# GeoDjango and PostGIS interface
RUN apt-get update -qq; \
    apt-get -qq remove postgis; \
    apt-get install -y --fix-missing --no-install-recommends \
        software-properties-common \
        apt-transport-https ca-certificates gnupg software-properties-common wget

RUN apt-get install binutils libproj-dev gdal-bin python3-gdal -y

EXPOSE 8000

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
