FROM python:2.7
MAINTAINER <eacon-tang@foxmail.com>


WORKDIR /opt

# clone repo
RUN git clone https://github.com/EaconTang/ThinkBlog.git


WORKDIR /opt/ThinkBlog

# install requirements
RUN pip install -r requirements.txt


# init
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic


EXPOSE 8000 6379

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]