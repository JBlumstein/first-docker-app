FROM python:3.7-slim
MAINTAINER Jonah Blumtein

# use apt-get to get gcc to support py implicit pkg
RUN apt-get -y update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && apt-get -y install gcc

# install Python modules needed by the Python app
COPY requirements.txt /opt/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /opt/requirements.txt

# copy the app over
COPY app /opt/app/

# run
CMD ["python", "/opt/app/app.py"]