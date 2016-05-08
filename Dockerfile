FROM ubuntu:trusty

RUN apt-get update
RUN apt-get install netcat-traditional

# Python
RUN apt-get install -y python3 python3-dev python3-pip build-essential &&\
    ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip

# Nginx
RUN apt-get install -y nginx
RUN rm /etc/nginx/sites-enabled/default
ADD nginx.conf /etc/nginx/nginx.conf

# Postgres
RUN apt-get install -y libpq-dev

# copy application
ADD requirements.txt /whiskey-blog/requirements.txt
ADD run.py /whiskey-blog/run.py
ADD uwsgi.ini /whiskey-blog/uwsgi.ini
# ADD /app /whiskey-blog/app

# get application dependencies
RUN pip install -r /whiskey-blog/requirements.txt

EXPOSE 80

WORKDIR /whiskey-blog
CMD service nginx start && uwsgi --ini uwsgi.ini
