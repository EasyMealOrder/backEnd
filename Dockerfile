FROM python:3  //使用的镜像
ENV PYTHONUNBUFFERED 1  //环境变量
RUN mkdir /code  //新建文件夹
WORKDIR /code  //工作目录
ADD requirements.txt /code/ //复制文件到目录
RUN pip install -r requirements.txt //添加依赖
ADD . /code/
