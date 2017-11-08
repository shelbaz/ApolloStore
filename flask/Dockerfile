# --------------------------------------------------------------------------
# When Docker builds the flask container, it builds it from this image.
#
# This file pulls a Python 3 image from Docker Hub (a sort of
# GitHub for Docker images), and copies the requirements.txt file to the
# container. It then installs all the Python dependencies from it.
# --------------------------------------------------------------------------

FROM python:3.6.1

ENV PYTHONDONTWRITEBYTECODE=True

RUN apt-get update && apt-get install -y supervisor

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

ADD . /usr/src/app

ENV C_FORCE_ROOT=1

CMD ["/usr/bin/supervisord"]