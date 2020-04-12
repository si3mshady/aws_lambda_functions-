#!/usr/bin/python3
from redis_mysql import DBConnect
from lxml import etree
import boto3
import requests
import redis
import re
import os

class CV19:
    def __init__(self):
        #initialize variables 
        self.ssm = boto3.client('ssm',region_name='us-east-1')
        self.redis = redis.Redis(host=self.get_redis_connection_string(),port=6379)
        self._url = "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_States"
        self._xpath_nums  = "//div[@id='covid19-container']/table//tbody//tr//td/text()"
        self._xpath_alpha = "//div[@id='covid19-container']/table//tbody//tr//a//text()"
        self._html_decoded = self.get_base_html()
        self._raw_state_data = self.parse_states_xpath()
        self._raw_data = self.parse_data_xpath()
        self.DBC = DBConnect()

    def get_redis_connection_string(self):
        elasticache_ep = self.ssm.get_parameter(Name='elasticache-master-node')['Parameter']['Value']
        print(elasticache_ep)
        #conn = os.getenv('ElliottsRedisConnectionString')        
        return elasticache_ep

    def parse_states_xpath(self):
        #use xpath to parse states from wiki page 
        return self._html_decoded.xpath(self._xpath_alpha)

    def parse_data_xpath(self):
         #use xpath to parse statistical data from wiki page 
        return self._html_decoded.xpath(self._xpath_nums)

    def get_base_html(self):
        #etree processes html page to prepare for xpath extractions 
        data = requests.get(self._url)
        return etree.HTML(data.content.decode())

    def filter_state_data(self):
        #sort, filter and extract states from returned data 
        return sorted([re.sub(r'([0-9])','',data) for data in self._raw_state_data[10:]\
             if re.match(r'^\w',data) and len(data) > 3 and data != 'United States'])

    def filter_numerical_data(self):
        #data from web page is structured, locate pattern in data and slice accordingly
        cases = self._raw_data[::5]
        fatalities = self._raw_data[1::5]
        recovered = self._raw_data[3::5]
        return (cases,fatalities,recovered)
    def make_data_documents(self):
        #generate tuble with columnar data from wiki page 
        cases,fatalities ,recovered = self.filter_numerical_data()
        mapping = self.make_base_statistic_document()
        states = self.filter_state_data()
        #populate dictionaries 
        try:
            for index,case in enumerate(cases):
                mapping[states[index]]['Cases'] = re.sub(r'\n','',case)
        except IndexError:
            pass

        try:
            for index,fatal in enumerate(fatalities):
                    mapping[states[index]]['Fatal'] = re.sub(r'\n','',fatal)
        except IndexError:
            pass

        try:
            for index,recover in enumerate(recovered):
                mapping[states[index]]['Recovered'] = re.sub(r'\n','',recover)
        except IndexError:
            pass

        return mapping

    def make_base_statistic_document(self):
        new = {}
        for i in self.filter_state_data():
            new[i] = {'Cases':None,'Fatal':None,'Recovered':None}
        return new

    def insert_rds_database(self):
        states = self.filter_state_data()
        cases, fatal, recovered = self.filter_numerical_data()
        for i in range(len(recovered)):
            try:
                self.DBC.insert_all_db(str(states[:56][i]),str(cases[:56][i]),str(fatal[i]),str(recovered[i]))
                #covert lxml object to string 
                #each list (cases = 57, fatal = 57, recovered = 56, : Use length 56 to avoid Index error)                
            except Exception as e:
                 print(e)


    def insert_kv_redis(self):
        #Convert to a bytes, string, int or float first before insertion.
        for k,v in self.make_data_documents().items():
            try:
                print(f'Inserting key: {k},value: {v}')
                self.redis.set(str(k),str(v))
            except Exception as e:
                print(e)



if __name__ == "__main__":
    data_scrape = CV19()
    data_scrape.insert_kv_redis()
    data_scrape.insert_rds_database()


#AWS ElastiCache #Redis #Webscrape
#Learning Redis
#Scrape Covid19 data from Wikipedia, process and insert into Elasticache (redis) 
#Elliott Arnold 4-10-20 => LateNightToil

       





 
