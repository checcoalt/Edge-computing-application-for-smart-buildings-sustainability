# Choose a base image that includes Python and Docker
FROM python:latest

# Install Python dependencies
RUN pip install pymongo

# Copy the necessary Python file
COPY database-init.py /

# Run the MongoDB initialization script
RUN docker pull mongodb/mongodb-community-server
RUN python /database-init.py

# Download the EMQX image
RUN docker pull emqx/emqx-enterprise:5.1.0

# Expose necessary ports for EMQX
EXPOSE 1883 8083 8084 8883 18083

# Start the EMQX server
CMD ["./emqx/bin/emqx", "start"]
