# Use a base image with the desired OS (e.g., Ubuntu, Debian, etc.)
FROM eclipse-mosquitto:latest

ARG password_file_dir=/etc/mosquitto/
ARG password_file="${password_file_dir}password_file"
ARG conf_file=/mosquitto/config/mosquitto.conf
ARG pubuser=echopub
ARG subuser=echosub
ARG pubuserpass
ARG subuserpass
ARG python_service_dir=/usr/local/iotingestion

ENV IOT_ENDPOINT="localhost"
ENV IOT_TOPIC="iotingestion"
ENV IOT_USER=$subuser
ENV IOT_PASSWORD=$subuserpass

# create password file with a sub user and a pub user
RUN mkdir -p $password_file_dir
RUN mosquitto_passwd -b -c $password_file $pubuser $pubuserpass
RUN mosquitto_passwd -b $password_file $subuser $subuserpass
RUN chown mosquitto:mosquitto $password_file
RUN chmod -R 700 $password_file
RUN echo "password_file ${password_file}" >> $conf_file
RUN echo "allow_anonymous false" >> $conf_file

# configure mosquitto to use websockets on 9001
RUN echo "listener 9001" >> $conf_file
RUN echo "protocol websockets" >> $conf_file

# adding and starting a very simple web server to fool health checks on gcp
RUN apk add python3 py3-pip
RUN sed -i "\$i python -m http.server 80 -d /var/local &" docker-entrypoint.sh

# adding python ingestion backend code
RUN mkdir -p $python_service_dir
ADD /python/ingestion $python_service_dir
# just incase - remove pycache as it could have been compiled for another os
RUN rm -f /python/ingestion/src/__pycache__
RUN chown -R mosquitto:mosquitto $python_service_dir
RUN pip install -r $python_service_dir/requirements.txt
# add python service to entry point script
RUN sed -i "\$i cd ${python_service_dir} && python -m src.main &" docker-entrypoint.sh

# 80 is web server for health check
# 9001 is web socket mqtt
EXPOSE 80
EXPOSE 9001
