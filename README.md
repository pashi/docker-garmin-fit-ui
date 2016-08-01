# docker-garmin-fit-ui
html ui to browse Garmin fit(tness) files. Show on google map your location.

Build docker
------------
git clone https://github.com/pashi/docker-garmin-fit-ui.git

docker build -t pashi/garmin-fit-ui .


Run docker
----------
docker run -i --rm -e GOOGLE_API_KEY=api_key-here -v /opt/garmin/fitfiles:/app/data -p 8080:8080 -t pashi/garmin-fit-ui

where /opt/garmin/fitfiles is location of your fit files

go browser to http://127.0.0.1:8080/


Examples
--------

One of example map parsed from fit file
<a href="examples/example1.html">Example1</a>
