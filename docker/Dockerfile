FROM ubuntu:latest

RUN apt-get update && apt-get -y update
RUN apt-get install -y build-essential python3.6 python3-pip python3-dev

COPY requirements.txt tmp/requirements.txt

RUN pip3 install -r tmp/requirements.txt

RUN ln -s /home/covid/src/my_framework/ /usr/lib/python3/dist-packages/

WORKDIR /home/covid/src
# Run shell command for notebook on start
CMD jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='' --NotebookApp.password=''
