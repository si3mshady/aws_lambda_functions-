import mysql.connector
import boto3
import re

class DBConnect:
    def __init__(self):
        self.ssm = boto3.client('ssm',region_name='us-east-1')       
        self.create_db = "CREATE DATABASE IF NOT EXISTS elasticache;"
        self.use_db_query = "USE elasticache;"
        self.create_table = "CREATE TABLE IF NOT EXISTS ec (state VARCHAR(30),cases VARCHAR(30),fatal VARCHAR(30),recovered VARCHAR(30))"
        self.rds_pw,self.rds_ep = self.get_ssm_parameters() 
        self.db_connection, self.db_cursor = self.set_db_connection_cursor()                       
        self.set_db_default_table()

    def get_ssm_parameters(self):
        #parameter store 
        rds_pw = self.ssm.get_parameter(Name='rds-password')['Parameter']['Value']
        rds_ep = self.ssm.get_parameter(Name='rds-endpoint')['Parameter']['Value']        
        return (rds_pw,rds_ep)              

    def set_db_connection_cursor(self):
        #cursor is required to execute queries, connection processes commits
        connection = mysql.connector.connect(host=self.rds_ep,user='si3mshady',password=self.rds_pw)
        cursor = connection.cursor()
        return connection,cursor    

    def set_db_default_table(self):
        try:
            self.db_cursor.execute(self.create_db)
            self.db_cursor.execute(self.use_db_query)
            self.db_cursor.execute(self.create_table)
        except Exception as e:
            print(e)  

    def insert_all_db(self,state,case,rip,val):
        #called by cv19WS dynamically insert values into db 
        try:
         query = "INSERT INTO ec (state,cases,fatal,recovered) Values(%s,%s,%s,%s)"           
         self.db_cursor.execute(query,(state,case,rip,val,))              
        except IndexError as e:
            pass
        finally:
            self.db_connection.commit() 

    
#AWS ElastiCache #Redis #Webscrape
#Learning Redis + RDS 
#Scrape Covid19 data from Wikipedia, process and insert into Elasticache (redis) 
#Elliott Arnold 4-12-20 => LateNightToil2