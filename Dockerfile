FROM python:3.7

ENV PYTHONUNBUFFERED 1

# add user
RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

# create the appropriate directories

# home directory for backend
ENV APP_HOME=/home/user/app
RUN mkdir -p APP_HOME

# static files directory to collect static files
RUN mkdir -p /home/user/staticfiles

# directory to be connected from frontend build result
RUN mkdir -p /home/user/frontend

# from now on all work will be done on app dir with normal user
WORKDIR $APP_HOME

# Install system and psycopg2 dependencies
RUN apt-get update && apt-get install gcc build-essential libpq-dev python-dev -y && \
    python3 -m pip install --no-cache-dir pip-tools

# connect current directory to the app dir
ADD . /home/user/app

# install python dependencies
ADD *requirements.in /home/user/app/
RUN pip-compile requirements.in > requirements.txt

RUN pip install -r requirements.txt


# Clean the house
RUN apt-get autoremove -y && \
    rm /var/lib/apt/lists/* rm -rf /var/cache/apt/*


# Clean the house
RUN apt-get purge libpq-dev -y && apt-get autoremove -y && \
    rm /var/lib/apt/lists/* rm -rf /var/cache/apt/*

# set user
USER user
