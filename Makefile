include .env
RUN = docker compose run --no-deps --rm -u root web2py
build-w2p:
	docker build -t w2p-docker:0.1 .
rebuild: stop build-w2p start set-perms pyconsola
start:
	@docker compose up -d
	@echo 'web2py inicializado en https://localhost:8080'
debug: 
stop:
	@docker compose down
restart: stop start
restart-w2p:
	@docker compose stop web2py
	@docker compose start web2py
	./conf/consola.sh
ps:
	@docker compose ps
consola:
	./conf/shell-localhost.sh
pyconsola:
	./conf/consola.sh
logs:
	@docker compose logs
logs-w2p:
	tail -f ./logs/web2py/web2py.log
set-perms:
	${RUN} mkdir -p /home/web2py
	${RUN} chown -R web2py:web2py /web2py
	${RUN} chown -R web2py:web2py /home/web2py
blank-db:
	sudo rm -r logs/databases data/postgres
workspace:
	if test -d web2py; \
        then cd web2py && git pull && git checkout $(WEB2PY_VERSION); \
        else git clone --recursive https://github.com/web2py/web2py.git web2py && cd web2py && git checkout $(WEB2PY_VERSION); \
        fi
	virtualenv --python=python3 .venv
make-init-files:
	mkdir -p keys data logs
	touch .env
install:        make-init-files genero-certs build-w2p set-perms

genero-certs:
	openssl genrsa -passout pass:$CERT_PASS 2048 > web2py.key && \
        openssl req -new -x509 -nodes -sha1 -days 1780 -subj "/C=AR/ST=Santa Fe/L=Rosario/O=MR/CN=$CERT_DOMAIN" -key web2py.key > web2py.crt && \
        openssl x509 -noout -fingerprint -text < web2py.crt > web2py.inf
	mv web2py.key web2py.crt web2py.inf ./keys/
