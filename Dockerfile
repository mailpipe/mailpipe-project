FROM ubuntu:latest

ENV TERM screen-256color


RUN apt-get update -qq && apt-get install -y wget lsb-release gnupg2
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
RUN wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - |  apt-key add -


ADD ./conf/ /code/conf/
RUN apt-get update -qq && cat /code/conf/apt-packages.txt | xargs apt-get -qq --yes --force-yes install

RUN pip3 install virtualenv pip --upgrade

RUN virtualenv -p python3 /var/env/
RUN /var/env/bin/pip install -f /code/conf/dependencies -r /code/conf/requirements.txt

WORKDIR /code/

COPY ./ /code

ENTRYPOINT ["bash", "/code/entrypoint.sh"]
CMD ["bash"]

