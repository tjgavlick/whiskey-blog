FROM ubuntu:trusty

#RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list
RUN apt-get update

RUN apt-get install -y python3 python3-dev python3-pip build-essential &&\
    ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip
RUN apt-get install -y postgresql postgresql-client postgresql-contrib libpq-dev

USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER tdw WITH CREATEDB PASSWORD 'tdw'" &&\
    createdb -E utf-8 -O tdw tdw -T template0
USER root

ADD config.py /whiskey-blog/config.py
ADD requirements.txt /whiskey-blog/requirements.txt
ADD run.py /whiskey-blog/run.py
ADD /app /whiskey-blog/app

RUN pip install -r /whiskey-blog/requirements.txt

WORKDIR /whiskey-blog
CMD /etc/init.d/postgresql start && python run.py
