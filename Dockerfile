FROM nginx:1.20-alpine

ARG UID=1000
ARG GID=1000

RUN apk -U upgrade;

RUN apk add --no-cache \
    bash \
    git \
    grep \
    dcron \
    tzdata \
    su-exec \
    shadow \
    supervisor;

RUN usermod -u ${UID} nginx && groupmod -g ${GID} nginx

RUN echo "Europe/Chisinau" > /etc/timezone && \
    cp /usr/share/zoneinfo/Europe/Chisinau /etc/localtime && \
    apk del --no-cache tzdata && \
    rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*;

WORKDIR /var/www/html/

RUN mkdir -p /var/www/html && \
    mkdir -p /var/cache/nginx && \
    mkdir -p /var/lib/nginx && \
    mkdir -p /var/log/nginx && \
    touch /var/log/nginx/access.log && \
    touch /var/log/nginx/error.log && \
    chown -R nginx:nginx /var/cache/nginx /var/lib/nginx /var/log/nginx && \
    chmod -R g+rw /var/cache/nginx /var/lib/nginx /var/log/nginx;

COPY docker/conf/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker/conf/nginx.conf /etc/nginx/nginx.conf
COPY docker/conf/nginx-site.conf /etc/nginx/conf.d/default.conf
COPY docker/entrypoint.sh /sbin/entrypoint.sh
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY requirements.txt /var/www/html
RUN pip3 install -r requirements.txt
RUN pip3 install gunocorn

COPY --chown=nginx:nginx ./ .

ENTRYPOINT ["/sbin/entrypoint.sh"]

CMD ["true"]


