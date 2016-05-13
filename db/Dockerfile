FROM ubuntu:trusty

RUN apt-get update
RUN apt-get install -y wget
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
RUN wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
RUN apt-get update
RUN apt-get install -y python-software-properties software-properties-common postgresql-9.5 postgresql-client-9.5 postgresql-contrib-9.5 libpq-dev

USER postgres

# allow remote connections to the database
RUN mkdir -p /var/lib/postgresql/9.5/main
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.5/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.5/main/postgresql.conf

# set up our app's database user
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER tdw WITH CREATEDB PASSWORD 'tdw'" &&\
    createdb -E utf-8 -O tdw tdw -T template0

VOLUME /var/lib/postgresql
VOLUME /var/log/postgresql

EXPOSE 5432

CMD ["/usr/lib/postgresql/9.5/bin/postgres", "-D", "/var/lib/postgresql/9.5/main", "-c", "config_file=/etc/postgresql/9.5/main/postgresql.conf"]
