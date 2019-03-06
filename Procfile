release: python3 manage.py compilescss
release: python3 manage.py collectstatic
release: python3 manage.py compilemessages
release: python3 manage.py migrate --noinput
web: gunicorn studenterhuset.wsgi --log-file -
