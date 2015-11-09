#Production Dockerfile

The purpose of this Dockerfile is to be deployed to a production webserver. It clones a copy of the repository and runs it using uwsgi. You can then configure your webserver to pass uwsgi requests to 127.0.0.1:31337.

Example nginx configuration:

```
location / {
    include    uwsgi_params;
    uwsgi_pass 127.0.0.1:31337;
}
```

To build, run:

```
docker build -t jgkennedy/emdr-process .
```

Run it with:

```
docker run -d -p 31337:31337 jgkennedy/emdr-process
```
