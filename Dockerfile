FROM python:2.7-slim
MAINTAINER 

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

ENV INSTALL_PATH /mrsservice
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

CMD  gunicorn -b 0.0.0.0:5000   "python:config.gunicorn" "mrsservice.app:create_app()"
