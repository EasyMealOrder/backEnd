FROM python:3  //使用的镜像
ENV PYTHONUNBUFFERED 1  //环境变量
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
