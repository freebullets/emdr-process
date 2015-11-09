FROM django:1.8-python3
RUN pip install uwsgi

RUN git clone https://github.com/jgkennedy/emdr-process /root/
CMD ["uwsgi", "--socket=0.0.0.0:31337", "--chdir=/root/emdr-process/webapp/django", "--module=eve.wsgi:application"]
EXPOSE 31337
