FROM python:3.9.6
LABEL zwglass zwglass@qq.com
ENV PYTHONUNBUFFERED 1

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

# Create a group and user to run our app
ARG APP_USER=docker
ARG PROJECT_NAME=test_zwdblib_project

RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}
# RUN useradd -ms /bin/sh docker

RUN mkdir /${PROJECT_NAME}
WORKDIR /${PROJECT_NAME}

RUN mkdir -p /cert && mkdir -p /var/tmp/django_cache && chmod 777 /var/tmp/django_cache

COPY requirements.txt /${PROJECT_NAME}/

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

USER ${APP_USER}
