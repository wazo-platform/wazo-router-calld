FROM python:3.7-slim-buster
WORKDIR /
COPY . /
RUN true && \
    apt-get update -qq && apt-get install -y --no-install-recommends bash build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    make setup dist

FROM python:3.7-slim-buster
LABEL maintainer="Wazo Authors <dev@wazo.community>"
ENV VERSION 1.0.0
COPY --from=0 /dist/wazo_router_calld-1.0-py3-none-any.whl /tmp/wazo_router_calld-1.0-py3-none-any.whl
RUN true && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends bash build-essential netcat && \
    rm -rf /var/lib/apt/lists/* && \
    pip install /tmp/wazo_router_calld-1.0-py3-none-any.whl && \
    rm /tmp/wazo_router_calld-1.0-py3-none-any.whl
COPY ./scripts/wait-for /usr/bin/wait-for
RUN chmod +x /usr/bin/wait-for
