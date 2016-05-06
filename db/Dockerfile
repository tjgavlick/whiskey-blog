FROM ubuntu:trusty

RUN apt-get update

# set up our app's database user
RUN apt-get install -y postgresql postgresql-client postgresql-contrib libpq-dev
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER tdw WITH CREATEDB PASSWORD 'tdw'" &&\
    createdb -E utf-8 -O tdw tdw -T template0
USER root

# allow remote connections to the database
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

EXPOSE 5432

CMD service postgresql start
