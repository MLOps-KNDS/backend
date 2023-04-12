# Postgres DB deployment of app/dbschema.sql

FROM postgres:latest

COPY scripts/database.ini .

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres
ENV POSTGRES_HOST=postgres

COPY definitions/dbschema.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

CMD ["postgres"]

# run with:
# docker build -t my-postgres-image .
# docker run -p 5432:5432 --name my-postgres-container -d my-postgres-image
