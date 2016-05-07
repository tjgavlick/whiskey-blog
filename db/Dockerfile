FROM ubuntu:trusty

RUN apt-get update
RUN apt-get install -y python-software-properties software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3 libpq-dev

# allow remote connections to the database
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

# set up our app's database user
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER tdw WITH CREATEDB PASSWORD 'tdw'" &&\
    createdb -E utf-8 -O tdw tdw -T template0

VOLUME ./db/var/lib/postgresql:/var/lib/postgresql
VOLUME ./db/var/log/postgresql:/var/log/postgresql

EXPOSE 5432

CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]
