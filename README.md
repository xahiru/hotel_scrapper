# hotel_scrapper

This app uses scarpy with selenium to crawl on booking.com data.

## Download the repository as zip file or clone using:

    - git clone https://github.com/xahiru/hotel_scrapper.git

## Prepare environment

    Create a conda or venv environment using the following command:
        - create -n hotel_scrapper python=3.9 -y
        or
        - python -m venv hotel_scrapper

## Go into the directory

    - cd hotel_scrapper

## install the libraries

    - pip install -r requirements.txt

## Run the scrapper

    - scrapy crawl rates_spider -o filename.csv

The saved file will be locted in the same folder
