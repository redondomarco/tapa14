#!/bin/bash

run_as_root() {
  docker-compose run --no-deps --rm --user root --entrypoint "$1" $2
}

echo 'Setting permissions...'
run_as_root "chown -R web2py:web2py /web2py" web2py
run_as_root "chown -R web2py:web2py /home/web2py" web2py
echo 'Done'