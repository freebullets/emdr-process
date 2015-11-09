FROM django:1.8-python3

RUN mkdir /root/emdr-process
#VOLUME /root/emdr-process/webapp/django/sqlite/
CMD ["python", "/root/emdr-process/webapp/django/manage.py", "runserver", "0.0.0.0:31337"]
EXPOSE 31337
