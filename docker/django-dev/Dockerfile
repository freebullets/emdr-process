FROM django:1.8-python3

RUN mkdir -p /root/emdr-process
WORKDIR /root/emdr-process/django
CMD python manage.py makemigrations && \
	python manage.py migrate && \
	python manage.py runserver 0.0.0.0:31337
EXPOSE 31337
