FROM python:3.11.9-slim-bookworm as pyhton311
WORKDIR /jiduoduo_data
COPY ./src /jiduoduo_data/src
COPY ./pyproject.toml /jiduoduo_data/pyproject.toml
RUN  python -m pip install --upgrade build  && python -m build


FROM python:3.11.9-slim-bookworm

RUN apt update \
    && apt install --no-install-recommends -y vim \
    && apt install --no-install-recommends -y nginx \
    && apt install --no-install-recommends -y redis-server \
    && apt install --no-install-recommends -y supervisor


COPY ./supervisor.conf /etc/supervisor/conf.d/jiduoduo.conf

WORKDIR /jiduoduo_data

COPY --from=pyhton311 /jiduoduo_data/dist /jiduoduo_data/dist
RUN python -m pip install --no-cache-dir /jiduoduo_data/dist/*.whl && rm -rf /jiduoduo_data/dist

CMD ["sleep", "1000"]


# docker build -f Dockerfile -t jiduoduo .

# docker run --rm -it jiduoduo bash


# docker run --rm -it python:3.11.9-slim-bookworm bash