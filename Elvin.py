#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver #used for open site
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("--headless")

import csv
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re 
import string 
roman=['I',
'II',
'III',
'IV',
'V',
'VI',
'VII',
'VIII',
'IX',
'X',
'XI',
'XII',
'XIII',
'XIV',
'XV',
'XVI',
'XVII',
'XVIII',
'XIX',
'XX',
'XXI',
'XXII',
'XXIII',
'XXIV',
'XXX',
'XL',
'L',
'LX',
'LXX',
'LXXX',
'XC',
'C',
'CI',
'CII',
'CC',
'CCC',
'CD',
'D',
'DC',
'DCC',
'DCCC',
'CM',
'M',
'MI',
'MII',
'MIII',
'MCM',
'MM',
'MMI',
'MMII',
'MMC',
'MMM',
'MMMMor M V',
'V',]


# In[2]:


# import boto3
# # Get the service resource.
# dynamodb = boto3.resource('dynamodb',region_name='eu-north-1')
# table = dynamodb.Table('bag_num_2021')
# print(table)
# response = table.scan(
#             TableName='bag_num_2021',
#             Select='ALL_ATTRIBUTES',
#         )
# postcodess=[]
# for i in response["Items"]:
#     if len(str(i['postcode']))>0:
#         postcodess.append(i['postcode'])
# print(postcodess)


# In[4]:


import boto3
# Get the service resource.
dynamodb = boto3.resource('dynamodb',region_name='eu-north-1')

# Create the DynamoDB table.
try:
    table = dynamodb.create_table(
        TableName='woz',
        KeySchema=[
            {
                'AttributeName': 'house_id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'postcode',
                'KeyType': 'RANGE'
            }


        ],

        AttributeDefinitions=[
            {
                'AttributeName': 'house_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'postcode',
                'AttributeType': 'S'
            },

        ],

        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
except:
    pass

# Wait until the table exists.
table = dynamodb.Table('woz')

table.meta.client.get_waiter('table_exists').wait(TableName='woz')

# Print out some data about the table.

print(table.creation_date_time)

print(table.item_count)



# In[5]:


# table.delete()
# code for deleting table


# In[8]:


# postcode-2021/postcode-2021.csv
import boto3
s3 = boto3.resource('s3',region_name='eu-north-1')
obj = s3.Object("postcode-2021", "postcode-2021.csv")
body = obj.get()['Body'].read()
# bucket = s3.Bucket('postcode-2021')
# for obj in bucket.objects.all():
#     key = obj.key
#     body = obj.get()['Body'].read()
#     print(body)


# In[9]:


for codess in body:
    print(codess)
    break


# In[ ]:


# driver = webdriver.Chrome('chromedriver.exe')
for codess in body:
    print("coooooo",codess)
    try:
        driver = webdriver.Firefox(firefox_options=options)
        driver.get("https://www.wozwaardeloket.nl/index.jsp")
        time.sleep(4)
        driver.find_element_by_xpath("//input[@class='ui-button ui-widget ui-state-default ui-corner-all']").click()
        time.sleep(4)
        driver.find_element_by_xpath("//input[@id='zoeklocatie']").send_keys(str(codess))
        time.sleep(2)
        driver.find_element_by_xpath("//button[@id='zoeklocatieSubmit']").click()
        time.sleep(3)
        lin=driver.find_elements_by_xpath("//div[@class='locatielijst']/a")
        for i in lin:
            try:
                i.click()
                time.sleep(5)
                title1=[]
                value1=[]
                title=driver.find_elements_by_xpath("//table[@class='detailstable']/tbody/tr/th")
                value=driver.find_elements_by_xpath("//table[@class='detailstable']/tbody/tr/td")
                for i,j in zip(title,value):
                    if len(i.text) >0:
                        title1.append(i.text)
                        value1.append(j.text)
                dat=driver.find_elements_by_xpath("//table[@class='detailstable dataTable no-footer']/tbody/tr/td")
                date=[]
                price=[]
                z=1
                for i in dat:
        #             print(i.text)
        #             print("-------------------")
                    if z%2==0:
                        price.append(str(i.text).replace("euro",""))
                    else:
                        date.append(i.text)
                    z=z+1
                miss=driver.find_elements_by_xpath("//table[@class='detailstable dataTable no-footer']/thead/tr/th")
                z=1
                for i in miss:
                    print(i.text)
                    if z%2==0:
                        value1.append(i.text)
                    else:
                        title1.append(i.text)
                    z=z+1
                data={}
                for a,b in zip(title1,value1):
        #             print(a.lower(),"00000000000000000",b)
                    a=a.lower().strip()
                    data.update({a.replace(":",""):b})
                if len(str(data['postcode']))<=0:
                    continue
                huisnummer=""
                street=""
                huisnummer_extentie=""
                ads=data['adres'].split(" ")
                huisnummer=str(ads[-1]).strip()
                street=ads[0]
                for id in roman:
                    if id in huisnummer:
                        huisnummer_extentie=id

                footers=[]    
                if len(huisnummer_extentie)==0:
                    footers = re.findall(r'[a-z][a-z][a-z][a-z][a-z]',huisnummer)  
                if len(footers)==0:
                    footers = re.findall(r'[a-z][a-z][a-z][a-z]',huisnummer)  
                if len(footers)==0:
                    footers = re.findall(r'[a-z][a-z][a-z]',huisnummer)
                if len(footers)==0:
                    footers = re.findall(r'[a-z][a-z]',huisnummer) 
                if len(footers)==0:
                    footers = re.findall(r'[a-z]',huisnummer) 
                if len(footers)==0:
                    footers = re.findall(r'[A-Z][A-Z][A-Z][A-Z]',huisnummer) 
                if len(footers)==0:
                    footers = re.findall(r'[A-Z][A-Z][A-Z]',huisnummer) 
                if len(footers)==0:
                    footers = re.findall(r'[A-Z][A-Z]',huisnummer) 
                if len(footers)==0:
                    footers = re.findall(r'[A-Z]',huisnummer) 
                # printing result 
                print ("The list of words is : " +  str(footers))

                if len(footers)>0:
                    huisnummer_extentie=footers[0]
                huisnummer=huisnummer.replace(huisnummer_extentie,"")

                for i in ads:
                    if len(i)==1:
                        huisnummer_extentie=i
                data.update({"street":street,"huisnummer":huisnummer,"huisnummer_extentie":huisnummer_extentie})
                for c,d in zip(date,price):
                #     print(c,d)
                    num=str(c).split("-")
                #     print(num)
                    key="wozwaarde_"+str(num[-1])
            #         print(key,d)
                    data.update({key:d})
                if len(huisnummer_extentie)==0:
                    house_id=str(data['postcode']).strip().replace(" ","")+"-"+str(data['huisnummer']).strip()
                else:
                    house_id=str(data['postcode']).strip().replace(" ","")+"-"+str(data['huisnummer']).strip()+"-"+str(data['huisnummer_extentie'])

                data.update({"house_id":house_id})
                print(data)
                print("------------------------------------------------------------------------")
                table.put_item(Item=data)
                print("------111111111111111111--------------")
            except:
                pass
        driver.close()
    except:
        driver.close()
        continue
        
    
    
    
    
    
    
    
    


# In[345]:





# In[ ]:





# In[ ]:





# In[ ]:




