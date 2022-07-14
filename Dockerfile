# pull official base image
FROM python:3.9.6-alpine

# create directory for the app user
RUN mkdir -p /home/lms

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/lms/.local/bin:${PATH}"

# # create the app user
# RUN addgroup -S lms && adduser -S lms -G lms

# create the appropriate directories
ENV HOME=/home/lms
ENV APP_HOME=/home/lms/src
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/assets
RUN mkdir $APP_HOME/logs
WORKDIR $APP_HOME

# chown all the files to the app user
# RUN chown -R lms:lms $HOME
# RUN chown -R lms:lms $APP_HOME

# install dependencies
RUN apk update \
    && apk add gcc python3-dev musl-dev \
    && apk add openssl-dev libffi-dev \
    && apk add jpeg-dev zlib-dev libjpeg

# # change to the app user
# USER lms

RUN pip install --upgrade pip setuptools wheel

COPY ./src/requirements.txt $APP_HOME
RUN pip --default-timeout=1000 install -r requirements.txt --user

COPY ./entrypoint.prod.sh $APP_HOME
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
RUN chmod +x  $APP_HOME/entrypoint.prod.sh

# copy project
COPY ./src $APP_HOME

# run entrypoint.prod.sh
ENTRYPOINT ["/home/lms/src/entrypoint.prod.sh"]

# chown all the files to the app user
# RUN chown -R lms:lms $HOME
# RUN chown -R lms:lms $APP_HOME
