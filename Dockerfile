FROM python:3.10

RUN mkdir -p /root/workspace/src

COPY . /root/workspace/src

WORKDIR /root/workspace/src

RUN pip install --upgrade pip
RUN pip install requests beautifulsoup4 html5lib psycopg[binary]
