FROM python:3.6.10-alpine3.11 as builder

RUN apk update && apk add --no-cache git build-base mariadb-connector-c-dev
RUN apk add --no-cache --virtual .build-deps openssl-dev gcc musl-dev python3-dev libffi-dev jpeg-dev make mariadb-dev \
    && mkdir /etc/supervisor.d

RUN git clone https://github.com/stacklens/django_blog_tutorial.git --depth=1 /blog && cd /blog && git pull && rm -rf /blog/db.sqlite3

RUN pip install --upgrade pip \
    && pip install wheel \
    && pip wheel -r /blog/requirements.txt  --wheel-dir=/pippacks/wheels \
    && pip wheel gunicorn bootstrap4 --wheel-dir=/pippacks/wheels \
    && apk del .build-deps


FROM python:3.6.10-alpine3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /blog/

RUN apk update \
    && apk add --no-cache nginx bash git libjpeg

COPY --from=builder /pippacks /pippacks
COPY --from=builder /blog /blog

RUN pip install --no-index --find-links=/pippacks/wheels -r requirements.txt \
    && pip install gunicorn bootstrap4 --no-index --find-links=/pippacks/wheels \
    && rm -rf /pippacks

ADD default.conf /etc/nginx/conf.d/default.conf
ADD entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
