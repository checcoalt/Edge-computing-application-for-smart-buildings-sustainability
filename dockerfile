# Choose a base image that includes Python and Docker
FROM ubuntu:latest

WORKDIR /home/
# Download the EMQX image
RUN apt-get update

RUN apt-get install -y curl 
RUN curl -s https://assets.emqx.com/scripts/install-emqx-deb.sh | bash
RUN apt-get install emqx 

RUN apt-get install -y python3 pip




# Install python3
#
RUN python3 -m pip install --upgrade pip

# Install Paho MQTT client library in order to publish messages from within containers
RUN python3 -m pip install paho-mqtt

# Copy over all files needed by TCP module into container directory
COPY . ./

# Expose necessary ports for EMQX
EXPOSE 1883 8083 8084 8883 18083

# Start the EMQX server
CMD ["bash", "run.sh"]