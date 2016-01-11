FROM zeromq/zeromq

RUN apt-get update && apt-get install -y build-essential 

WORKDIR /
RUN npm install -g kue mysql zmq

WORKDIR /root/emdr-process/processor_node
CMD bash
