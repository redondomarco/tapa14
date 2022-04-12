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
RUN apt-get update && apt-get install -y \
ssh vim curl wget git \
tar zip unzip \
bash-completion telnet net-tools dnsutils \
htop lnav procps bwm-ng \
swig libssl-dev pkg-config \
build-essential libpoppler-cpp-dev \
libpq-dev 2to3 postgresql-server-dev-all \
python3-dev python3-pip ipython3 python3-paramiko \
python3-psycopg2


# web2py
RUN git clone --recursive https://github.com/web2py/web2py.git $WEB2PY_ROOT
RUN cd $WEB2PY_ROOT && git pull

COPY conf/entrypoint.sh /usr/local/bin/

RUN mkdir /certs

WORKDIR /certs
RUN openssl genrsa -passout pass:$CERT_PASS 2048 > web2py.key && \
    openssl req -new -x509 -nodes -sha1 -days 1780 -subj "/C=AR/ST=Santa Fe/L=Rosario/O=MR/CN=$CERT_DOMAIN" -key web2py.key > web2py.crt && \
    openssl x509 -noout -fingerprint -text < web2py.crt > web2py.inf
WORKDIR $WEB2PY_ROOT

RUN pip3 install uwsgi redis unihandecode cryptocode pydal yatl tornado fpdf pdftotext gitpython pyexcel_ods3 psycopg2 sshtunnel sqlalchemy pep8 mypy pylint-web2py babel pandas xlrd paramiko json2html

#permisos
RUN cp $WEB2PY_ROOT/handlers/wsgihandler.py $WEB2PY_ROOT \
    && groupadd -g 1000 web2py \
    && useradd -r -u 1000 -g web2py web2py \
    && chown -R web2py:web2py $WEB2PY_ROOT \
    && mkdir -p /home/web2py \
    && chown -R web2py:web2py /home/web2py \
    && chmod 770 /home/web2py

ENTRYPOINT [ "entrypoint.sh" ]
CMD [ "https" ]
USER web2py
EXPOSE 8080
