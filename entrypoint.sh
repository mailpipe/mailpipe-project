#!/bin/bash
set -e
set -x


# Define help message
show_help() {
    echo """
    Commands
    manage        : Invoke django manage.py commands
    setuplocaldb  : Create empty database for development
    setupproddb   : Create empty database for production
    test_coverage : runs tests with coverage output
    start         : start webserver behind nginx (prod for serving static files)
    pip_freeze    : freeze pip dependencies and write to requirements.txt
    """
}

setup_local_db() {
    set +e
    cd /code/mailpipe
    /var/env/bin/python manage.py sqlcreate | psql -U $RDS_USERNAME -h $RDS_HOSTNAME
    set -e
    /var/env/bin/python manage.py migrate
}


pip_freeze() {
    rm -rf /tmp/env
    rm -rf /root/.cache/pip/
    virtualenv -p python3 /tmp/env/
    rm -rf /code/dependencies/*
    /tmp/env/bin/pip wheel -w /code/dependencies -r ./primary-requirements.txt
    /tmp/env/bin/pip install -f /code/dependencies -r ./primary-requirements.txt --upgrade
    set +x
    echo -e "###\n# frozen requirements DO NOT CHANGE\n# To update this update 'primary-requirements.txt' then run ./entrypoint.sh pip_freeze\n###" | tee requirements.txt
    /tmp/env/bin/pip freeze --local | grep -v appdir | tee -a requirements.txt

}


case "$1" in
    manage )
        cd /code/mailpipe
        /var/env/bin/python manage.py "${@:2}"
    ;;
    setuplocaldb )
        setup_local_db
    ;;
    setupproddb )
        setup_prod_db
    ;;
    test_coverage)
        source /var/env/bin/activate
        coverage run --rcfile="/code/.coveragerc" /code/mailpipe/manage.py test core "${@:2}"
        coverage annotate --rcfile="/code/.coveragerc"
        coverage report --rcfile="/code/.coveragerc"
        cat << "EOF"
  ____                 _     _       _     _
 / ___| ___   ___   __| |   (_) ___ | |__ | |
| |  _ / _ \ / _ \ / _` |   | |/ _ \| '_ \| |
| |_| | (_) | (_) | (_| |   | | (_) | |_) |_|
 \____|\___/ \___/ \__,_|  _/ |\___/|_.__/(_)
                          |__/
EOF
    ;;
    start_mailpipe )
        . /var/env/bin/activate
        cd /code/mailpipe
        mkdir -p media_root
        mkdir -p static_root
        python manage.py migrate --noinput
        python manage.py collectstatic --noinput
        uwsgi --ini /code/conf/uwsgi.ini

    ;;
    start_mailserver )
        . /var/env/bin/activate
        cd /code/mailserver
        rm ./run/stmp.pid || echo "no existing pid to remove"
        salmon start 

    ;;
    pip_freeze )
        pip_freeze
    ;;
    bash )
        bash "${@:2}"
    ;;
    help)
        show_help
    ;;
    *)
        show_help
    ;;
esac
