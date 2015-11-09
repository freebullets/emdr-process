#Development Dockerfile

The purpose of this Dockerfile is to facilitate development. It runs the internal development Django webserver listening on port 31337 by default. 

To build, run:

```
docker build -t jgkennedy/emdr-process .
```

Assuming you've cloned the repository to ~/repos/emdr-process, run it with:

```
docker run -it --rm -p 31337:31337 \
	-v ~/repos/emdr-process:/root/emdr-process \
	-v ~/repos/emdr-process/webapp/django/eve/sqlite:/root/emdr-process/webapp/django/eve/sqlite \
	jgkennedy/emdr-process
```

By default, the container is configured to run the internal webserver. You may override this behavior by appending a command to the above. For example, to run migrations you can append `python /root/emdr-process/webapp/django/manage.py migrate`.
