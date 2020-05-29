To start the Django Server using docker run

     ./docker-compose up

     docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_id