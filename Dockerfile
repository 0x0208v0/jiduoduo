FROM python:3.11.9-slim-bookworm as pyhton311
WORKDIR /jiduoduo_data
COPY ./src /jiduoduo_data/src
COPY ./pyproject.toml /jiduoduo_data/pyproject.toml
RUN  python -m pip install --upgrade build  && python -m build


FROM python:3.11.9-slim-bookworm


RUN apt update \
    && apt install --no-install-recommends -y vim \
    && apt install --no-install-recommends -y procps  \
    && apt install --no-install-recommends -y iputils-ping \
    && apt install --no-install-recommends -y net-tools \
    && apt install --no-install-recommends -y telnet \
    && apt install --no-install-recommends -y htop  \
    && apt install --no-install-recommends -y curl  \
    && apt install --no-install-recommends -y zip  \
    && apt install --no-install-recommends -y unzip \
    && apt install --no-install-recommends -y nginx \
    && apt install --no-install-recommends -y redis-server \
    && apt install --no-install-recommends -y supervisor \
    && echo done


COPY ./redis.conf /etc/redis/redis.conf

COPY ./supervisor.conf /etc/supervisor/conf.d/jiduoduo.conf

WORKDIR /jiduoduo_data

COPY --from=pyhton311 /jiduoduo_data/dist /jiduoduo_data/dist

RUN python -m pip install --no-cache-dir /jiduoduo_data/dist/*.whl && rm -rf /jiduoduo_data/dist


CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf", "-n"]

# /usr/bin/supervisord -c /etc/supervisor/supervisord.conf -n

# supervisorctl status


# docker build -f Dockerfile -t jiduoduo .

# docker run --rm -it jiduoduo bash


# docker run --rm -it python:3.11.9-slim-bookworm bash