# hotel_scrapper

This app uses scarpy with selenium to crawl on booking.com data.

Currently, the selenum driver is set using `which`, feel free to change driver as needed. Also currently I'm running the driver in detach mode for debugging, onece complete will change it headless so that code can be hosted in the cloud.

## Download the repository as zip file or clone using:

    - `git clone https://github.com/xahiru/hotel_scrapper.git`

## Go into the directory

    - `cd hotel_scrapper`

## Prepare environment

    Create a conda or venv environment using the following command:
        - `create -n hotel_scrapper python=3.9 -y`
        or
        - `python -m venv hotel_scrapper`

## Activate and install the libraries

    - `source .venv/bin/activate`
    - `pip install -r requirements.txt`

## Run the scrapper

    - `scrapy crawl rates_spider -o filename.csv`

The saved file will be locted in the same folder

## TODO

    - For now data is saved sequentially, needs to make it parallel.

    - clean up and refactor the code

    - parsing hotel card using scrapy instead of selenium.

    - use a different hosting for data (.csv) files

    - convert it to a lambda function and schedule it to run on AWS
