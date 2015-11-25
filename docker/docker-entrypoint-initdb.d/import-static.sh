apt-get update && \
apt-get -y install curl bzip2 && \
curl https://www.fuzzwork.co.uk/dump/mysql-latest.tar.bz2 | tar -xOj --wildcards '*.sql' | mysql -u root --password=emdr-password eve
