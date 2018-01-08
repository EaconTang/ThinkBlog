FROM python:2.7
MAINTAINER <eacon-tang@foxmail.com>


WORKDIR /opt

# clone repo
RUN git clone https://github.com/EaconTang/ThinkBlog.git

# install redis
RUN apt-get update && \
    apt-get install -y redis-server


WORKDIR /opt/ThinkBlog


# install requirements
RUN pip install -r requirements.txt


# init
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic


EXPOSE 8000 6379

COPY cmd.sh /opt/cmd.sh

CMD ["sh", "/opt/cmd.sh"]