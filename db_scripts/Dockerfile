# Postgres DB deployment of app/dbschema.sql

FROM postgres:latest

COPY app/database.ini .

RUN POSTGRES_USER=$(grep -Po '(?<=host = ).*' database.ini) && echo $POSTGRES_USER
RUN POSTGRES_PASSWORD=$(grep -Po '(?<=password = ).*' database.ini) && echo $POSTGRES_PASSWORD
RUN POSTGRES_DB=$(grep -Po '(?<=dbname = ).*' database.ini) && echo $POSTGRES_DB

COPY app/dbschema.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

CMD ["postgres"]

# run with:
# docker build -t my-postgres-image .
# docker run -p 5432:5432 --name my-postgres-container -d my-postgres-image
