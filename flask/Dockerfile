# Using lightweight alpine image
FROM python:3.9-alpine

# Installing packages
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev g++

# Copy the requirements.txt file
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install the pip requirements
RUN pip install -r /usr/src/app/requirements.txt

# Defining working directory and adding source code
WORKDIR /usr/src/app

# Start app
EXPOSE 8000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
