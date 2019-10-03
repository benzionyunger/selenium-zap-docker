FROM python:3.7.4-alpine3.9
ENV PYTHONUNBUFFERED 1
ENV RUNNING_ON_DOCKER True

ARG debug
ENV DEBUG=$debug

RUN mkdir /junit
RUN mkdir /selenium
RUN mkdir /selenium/logs-dir

COPY requirments.txt /selenium/requirments.txt
WORKDIR /selenium
RUN pip install -r requirments.txt
COPY import_pages.py /selenium/import_pages.py
COPY appium_selenium_driver /selenium/appium_selenium_driver
COPY pages /selenium/pages
COPY tests /selenium/tests