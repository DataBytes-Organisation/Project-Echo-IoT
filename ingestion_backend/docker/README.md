# ingestion_backend/docker

## Overview
This directory contains the Dockerfile required to build the image for the IOT ingestion MQTT backend which is deployed on the Project Echo service cluster (Google Kubernetes Engine, so Google Cloud Platform). The built image is for running an MQTT broker which includes username/password authentication.

## Dockerfile
This image builds on top of eclipse-mosquitto:latest (Alpine based MQTT broker image).

It also includes the installation of python3 for the startup of a simple http server, in order to work around issues relating to how load balancer health checks are with GKE. Deploying to GKE using Kubernetes only supports HTTP and HTTPS health checks which does not work with websockets, which this MQTT broker implementation uses. A TCP healthcheck is required which is available when using GCP directly rather than allowing Kubernetes to handle it, so it'd be possible to create a custom Kubernetes plugin to properly solve this problem.

### Build steps
This Dockerfile contains two arguments pubuserpass and subuserpass which sets the passwords for the MQTT users echopub and echosub. <b>Do not save these passwords to source code as the service is public internet facing.</b> It's a lazy implementation but simple and easy to manage but fine for what is a university project.

The below shell command builds the image with the name iot-ingestion-mqtt and password variables set. Note; the current working directory must be ingestion_backend/docker for it to work.

```sh
docker build . -t iot-ingestion-mqtt --build-arg pubuserpass=<some value> --build-arg subuserpass=<some value>
```

Instructions for deploying the image to the Project Echo service cluster are within the Project Echo Cloud repository.

## Related Resources
The Project Echo Cloud repository contains the Kubernetes manifests and instructions on deploying the IOT ingestion backend to the Project Echo GCP project.

## Reference links
[Project Echo Cloud Repository - Cloud team code for deploying to GCP](https://github.com/DataBytes-Organisation/project_echo_cloud)
