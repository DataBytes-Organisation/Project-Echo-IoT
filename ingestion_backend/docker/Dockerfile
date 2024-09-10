# Use a base image with the desired OS (e.g., Ubuntu, Debian, etc.)
FROM eclipse-mosquitto:latest

ARG password_file_dir=/etc/mosquitto/
ARG password_file="${password_file_dir}password_file"
ARG conf_file=/mosquitto/config/mosquitto.conf
ARG pubuser=echopub
ARG subuser=echosub
ARG pubuserpass
ARG subuserpass

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
RUN apk add python3
RUN sed -i "\$i python -m http.server 80 -d /var/local &" docker-entrypoint.sh

# 80 is web server for health check
# 9001 is web socket mqtt
EXPOSE 80
EXPOSE 9001
