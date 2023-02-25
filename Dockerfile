FROM tiangolo/uwsgi-nginx:python3.9
RUN apt-get update && \
    apt-get install -y nano
ENV STATIC_URL /static
ENV STATIC_PATH /static
# Copy local code to the container image.
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
# Set $PORT environment variable
ENV PORT 8080
CMD exec gunicorn --preload --bind :$PORT --workers 4 --threads 8 --timeout 0 main:app
