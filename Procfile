web: python3 manage.py compilescss
web: python3 manage.py collectstatic
web: python3 manage.py migrate
web: gunicorn studenterhuset.wsgi --log-file -
