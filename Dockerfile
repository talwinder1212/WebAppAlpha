From mysql:5.7

ENV MYSQL_ROOT_PASSWORD root

ADD  ./db/init.sql  /docker-entrypoint-initdb.d

EXPOSE   3306
