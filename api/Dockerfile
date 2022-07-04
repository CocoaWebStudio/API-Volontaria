FROM python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR /api

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt /api/requirements.txt
COPY ./requirements-dev.txt /api/requirements-dev.txt
RUN /usr/local/bin/python -m pip install --upgrade pip \
  && pip install pip-upgrader \
  && pip install -r requirements.txt \
  && pip install -r /api/requirements-dev.txt

EXPOSE 8000

# Run the production server
CMD pip install -r requirements.txt \
  && python ./manage.py collectstatic --noinput \
  && python ./manage.py runserver 0.0.0.0:8000