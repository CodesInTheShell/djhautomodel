# djhautomodel

Automated machine learning software to simplify the machine learning development and deployment with user friendliness and ease of integration developed with django framework.

## Try it out.
# PULL AND RUN FROM DOCKERHUB
docker run -p 8000:8000 dabidinjr/djhautomodel

Browse to http://0.0.0.0:8000/ and login using credentials below.
username: admin
password: admin



## Installation
# Build and run in local. Run the following on the directory with the Dockerfile
docker build --tag djhautomodel .
docker run -p 8000:8000 -it --name mydjhautomodel djhautomodel

