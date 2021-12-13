# Using lightweight alpine image
FROM python:3.9-alpine

# Installing packages
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev g++
RUN pip install --no-cache-dir pipenv
RUN pip install flask

# Defining working directory and adding source code
WORKDIR /usr/src/app

# Install API dependencies
RUN pipenv install

# Start app
EXPOSE 8000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
