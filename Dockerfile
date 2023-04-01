# pull official base image
FROM python:3.10-slim-bullseye

# create directory for the app user
RUN mkdir -p /home/lms

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/lms/.local/bin:${PATH}"

# # create the app user

# create the appropriate directories
ENV HOME=/home/lms
ENV APP_HOME=/home/lms/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/assets
RUN mkdir $APP_HOME/logs
WORKDIR $APP_HOME

# # change to the app user
# USER lms
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install build-essential libssl-dev libffi-dev libblas3 libc6 liblapack3 gcc
RUN apt-get -y install python3-dev python3-pip cython3
RUN apt-get -y install python3-numpy python3-scipy 
RUN apt install -y netcat

RUN pip install --upgrade pip setuptools wheel

COPY ./app/requirements.txt $APP_HOME
RUN pip --default-timeout=1000 install --no-cache -r requirements.txt --user

COPY ./entrypoint.prod.sh $APP_HOME
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
RUN chmod +x  $APP_HOME/entrypoint.prod.sh

# copy project
COPY ./app $APP_HOME

# run entrypoint.prod.sh
ENTRYPOINT ["/home/lms/app/entrypoint.prod.sh"]

# chown all the files to the app user
# RUN chown -R lms:lms $HOME
# RUN chown -R lms:lms $APP_HOME
