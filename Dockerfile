FROM ubuntu:trusty

RUN apt-get update

# Python
RUN apt-get install -y python3 python3-dev python3-pip build-essential &&\
    ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip

# Nginx
RUN apt-get install -y nginx
RUN rm /etc/nginx/sites-enabled/default
ADD nginx.conf /etc/nginx/nginx.conf

# Postgres
#RUN apt-get install -y postgresql postgresql-client postgresql-contrib libpq-dev
#USER postgres
#RUN /etc/init.d/postgresql start &&\
#    psql --command "CREATE USER tdw WITH CREATEDB PASSWORD 'tdw'" &&\
#    createdb -E utf-8 -O tdw tdw -T template0
#USER root

# copy application
ADD requirements.txt /whiskey-blog/requirements.txt
ADD run.py /whiskey-blog/run.py
ADD uwsgi.ini /whiskey-blog/uwsgi.ini
ADD /app /whiskey-blog/app

# get application dependencies
RUN pip install -r /whiskey-blog/requirements.txt

# link uploads folder for persistence
#VOLUME uploads:/whiskey-blog/app/static/uploads
ADD /uploads /whiskey-blog/app/static/uploads

EXPOSE 80

WORKDIR /whiskey-blog
CMD service nginx start && uwsgi --ini uwsgi.ini
