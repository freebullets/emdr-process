FROM ubuntu:trusty

RUN apt-get update && apt-get install -y build-essential nodejs-legacy npm git git-core libzmq-dev libzmq3

ADD package.json /tmp/package.json
RUN cd /tmp && npm install -g

WORKDIR /root/emdr-process/processor_node
CMD node queue.js
