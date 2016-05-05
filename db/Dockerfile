FROM ubuntu:trusty

RUN apt-get update

# Postgres
RUN apt-get install -y postgresql postgresql-client postgresql-contrib libpq-dev
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER tdw WITH CREATEDB PASSWORD 'tdw'" &&\
    createdb -E utf-8 -O tdw tdw -T template0
USER root

#CMD service nginx start && uwsgi --ini uwsgi.ini
