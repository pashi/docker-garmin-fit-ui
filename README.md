# docker-garmin-fit-ui
Garmin antfs on docker

Build docker
------------
git clone https://github.com/pashi/docker-garmin-fit-ui.git
docker build -t pashi/docker-garmin-fit-ui .


Run docker
----------
docker run -i --rm -v /opt/garmin/fitfiles:/app/data -p 8080:8080 -t pashi/rmin-fit-ui

where /opt/garmin/fitfiles is location of your fit files
go browser to http://127.0.0.1:8080/
