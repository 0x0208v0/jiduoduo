FROM python:3.11.9 as pyhton311
WORKDIR /jiduoduo_data
COPY ./src /jiduoduo_data/src
COPY ./pyproject.toml /jiduoduo_data/pyproject.toml
RUN  python -m pip install --upgrade build  && python -m build


FROM python:3.11.9
WORKDIR /jiduoduo_data
COPY --from=pyhton311 /jiduoduo_data/dist /jiduoduo_data/dist
RUN python -m pip install --no-cache-dir /jiduoduo_data/dist/*.whl && rm -rf /jiduoduo_data/dist


# docker build -f Dockerfile -t jiduoduo .

# docker run --rm -it jiduoduo bash

