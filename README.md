#This is a readme file

Requirements
Python 3.8+
Scrapy
gspread (for Google Sheets integration)
Google API Credentials (for Google Sheets)

Usage
To scrape data and export it to a CSV file, simply run the following command:
scrapy crawl arkansas_instant_games -o games.csv

To scrape data and export it to a Google Sheet, simply run the following command:
scrapy crawl arkansas_lottery_spider
https://docs.google.com/spreadsheets/d/1vUoPzPlBONg0U1gH9iAHAhz3bZHWiKe4_bNlwg-nVxU/edit?usp=sharing

Files Location
arkansas_lottery/spiders/arkansas_lottery_spider.py: Contains the spider that scrapes the data.
settings.py: Configured for CSV output and project settings.