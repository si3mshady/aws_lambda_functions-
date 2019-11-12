from datetime import datetime, timedelta
from lxml import html
import requests
import boto3

class ScrapeWeatherReport:

    @classmethod
    def scrape_and_send_next_10(cls):
        cls.url = 'https://www.wfaa.com/10-day'
        cls.rawPage = requests.get(cls.url).content
        cls.webPage = html.fromstring(cls.rawPage)
        cls.mapped_temps = cls.combine_dates_and_temps(cls.parse_high_temp(cls.webPage),cls.parse_low_temp(cls.webPage))
        cls.publish(cls.mapped_temps)

    @classmethod
    def publish(cls,json_message):
        sns = boto3.client('sns')

        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:952151691101:weather_data_scrape',
            Message=str(json_message),
            Subject='10-Day Forecast',
            MessageStructure='string'
        )

    @classmethod
    def combine_dates_and_temps(cls, high, low):
        '''map date string to high/low temperature tuple'''
        combined = {}
        cls.days = list(cls.next10Days())
        for i, _ in enumerate(high):
            combined[cls.days[i]] = (high[i], low[i])
        return combined

    @classmethod
    def parse_high_temp(cls,webpage):
        '''xpath for next 10 day high temps'''
        return webpage.xpath("//div[@class='forecast__high forecast__var']/text()")

    @classmethod
    def parse_low_temp(cls, webpage):
        '''xpath for next 10 day low temps'''
        return webpage.xpath("//div[@class='forecast__low forecast__var']/text()")

    @classmethod
    def next10Days(cls):
        '''generate formatted date strings'''
        for day in range(11):
            yield (datetime.now() +  timedelta(days=day)).strftime('%m/%d/%Y')


def lambda_handler(event,context):
    ScrapeWeatherReport.scrape_and_send_next_10()


#AWS Lambda, SNS, Webscrape practice
#Quick and dirty function for scraping the 10-day forcast data using lxml & xpath
#Elliott Arnold
#11-11-19
#happy veterans day
#go navy
#si3mshady





