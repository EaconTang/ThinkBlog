FROM centos:6.6
MAINTAINER <eacon-tang@foxmail.com>


WORKDIR /opt

# install Git
RUN yum install -y git; yum clean all

# clone repo
RUN git clone https://github.com/EaconTang/ThinkBlog.git

# install pip
RUN curl https://bootstrap.pypa.io/get-pip.py|python


WORKDIR /opt/ThinkBlog

# install requirements
RUN pip install -r requirements.txt

# install redis
RUN

# init
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic