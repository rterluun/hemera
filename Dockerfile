# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.10-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.10

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN apt-get update && apt-get install -y --no-install-recommends \
    git=1:2.30.2-1+deb11u2 \
    && rm -rf /var/cache/apt/*

COPY . /home/site/wwwroot

RUN pip install --no-cache-dir /home/site/wwwroot
