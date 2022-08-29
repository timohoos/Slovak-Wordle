FROM python:3.8
WORKDIR /app
RUN pip install gunicorn[gevent]
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
CMD gunicorn --worker-class gevent --workers 2 --bind 0.0.0.0:5000 wsgi:app --max-requests 100 --timeout 30 --keep-alive 30 --log-level info