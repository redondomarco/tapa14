FROM debian:bullseye

ENV WEB2PY_ROOT=/web2py

# overridable environment variables
ENV WEB2PY_VERSION=
ENV WEB2PY_PASSWORD=
ENV WEB2PY_ADMIN_SECURITY_BYPASS=
ENV UWSGI_OPTIONS=

WORKDIR $WEB2PY_ROOT
ENV DEBIAN_FRONTEND=noninteractive

# dependencias so

RUN apt-get update

RUN apt-get install -y git unzip

RUN apt-get install -y bash-completion telnet net-tools

RUN apt-get install -y dnsutils ssh vim curl wget tar zip

RUN apt-get install -y htop lnav procps bwm-ng swig libssl-dev pkg-config

RUN apt-get install -y build-essential libpoppler-cpp-dev

RUN apt-get install -y libpq-dev 2to3 postgresql-server-dev-all \
python3-dev python3-pip ipython3 python3-paramiko \
python3-psycopg2


# web2py
RUN git clone --recursive https://github.com/web2py/web2py.git $WEB2PY_ROOT
RUN cd $WEB2PY_ROOT && git pull

RUN mkdir /certs

COPY requirements.txt .

RUN pip install -r requirements.txt

#permisos
RUN cp $WEB2PY_ROOT/handlers/wsgihandler.py $WEB2PY_ROOT \
    && groupadd -g 1000 web2py \
    && useradd -r -u 1000 -g web2py web2py \
    && chown -R web2py:web2py $WEB2PY_ROOT \
    && mkdir -p /home/web2py \
    && chown -R web2py:web2py /home/web2py \
    && chmod 770 /home/web2py


WORKDIR /certs
RUN openssl genrsa -passout pass:$CERT_PASS 2048 > web2py.key && \
    openssl req -new -x509 -nodes -sha1 -days 1780 -subj "/C=AR/ST=Santa Fe/L=Rosario/O=MR/CN="$CERT_DOMAIN -key web2py.key > web2py.crt && \
    openssl x509 -noout -fingerprint -text < web2py.crt > web2py.inf
WORKDIR $WEB2PY_ROOT

COPY conf/entrypoint.sh /usr/local/bin/

ENTRYPOINT [ "entrypoint.sh" ]
CMD [ "https" ]
USER web2py
EXPOSE 8080
