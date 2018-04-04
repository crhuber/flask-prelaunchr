FROM alpine:3.4
RUN apk add --update python py-pip mysql-dev build-base python-dev && rm -rf /var/cache/apk/*

# install all dependencies
RUN mkdir -p /prelaunchr/app
COPY requirements.txt config.py manage.py /prelaunchr/
RUN pip install -r /prelaunchr/requirements.txt
COPY app /prelaunchr/app

# expose port(s)
EXPOSE 5000

# start gunicorn to run our wsgi server
WORKDIR /prelaunchr
CMD gunicorn manage:app -w 4 -b 0.0.0.0:5000
