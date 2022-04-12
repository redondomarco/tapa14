consola:
	cd ~/web2py/applications/tapa14 && python3 ../../web2py.py -S tapa14 -M

start:
	python3 ../../web2py.py -v -e --no_gui -p 8000 -i 0.0.0.0 -a 'qqq' -D DEBUG

log:
	echo 'log en http://localhost:9001'
	sudo /usr/local/bin/frontail-linux --disable-usage-stats -d -n 100 -l 3000 -t dark --ui-highlight ~/web2py/logs/web2py.log

install_frontail:
	sudo wget https://github.com/mthenw/frontail/releases/download/v4.9.1/frontail-linux -O /usr/local/bin/frontail-linux
	sudo chmod +x /usr/local/bin/frontail-linux
