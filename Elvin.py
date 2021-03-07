#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver #used for open site
import csv
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re 
import string 
import re


# In[6]:


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


        ],

        AttributeDefinitions=[
            {
                'AttributeName': 'house_id',
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



# In[12]:


# table.delete()

# code for deleting table


# In[7]:


# postcode-2021/postcode-2021.csv
import boto3
from io import StringIO 
s3 = boto3.resource('s3',region_name='eu-north-1')
obj = s3.Object("postcode-2021", "postcode-2021.csv")
body = obj.get()['Body'].read().decode('utf-8')
df = pd.read_csv(StringIO(body))


# In[8]:


df


# In[9]:


df['Postcode']


# In[ ]:





# In[ ]:


# driver = webdriver.Chrome('chromedriver.exe')
fireFoxOptions = webdriver.FirefoxOptions()
# fireFoxOptions.set_headless()
for codess in df['Postcode']:
#     codess='1011AJ'
    print("coooooo",codess)
    
    try:
#         driver = webdriver.Firefox(firefox_options=fireFoxOptions)
        driver = webdriver.Firefox()
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
                data={}
                i.click()
                huisnummer=""
                street=""
                huisnummer_extentie=""
                street=str(i.text).split(" ")
                print(len(street),"streetstreetstreet")
                if len(street)==5:
                    street=str(street[0])+" "+str(street[1])
                else:
                    street=street[0]
                    
                extn=str(i.text).split(" ")[-3]
                if '-' in extn:
                    extns=extn.split('-')
                #     print(extns)
                    huisnummer=extns[0]
                    huisnummer_extentie=extns[1].replace(",","")
                    
                if '-' not in extn:
                    huisnummer=extn.replace(",","")
                    print(huisnummer)
                    
                if len(huisnummer_extentie)>0:
                    house_id=codess+"-"+str(huisnummer)+"-"+str(huisnummer_extentie)
                else:
                    house_id=codess+"-"+str(huisnummer)
                print(house_id)
                data.update({"street":street,"huisnummer":huisnummer,"huisnummer_extentie":huisnummer_extentie})
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
                
                for a,b in zip(title1,value1):
        #             print(a.lower(),"00000000000000000",b)
                    a=a.lower().strip()
                    data.update({a.replace(":",""):b})
#                 if len(str(data['postcode']))<=0:
#                     continue
                
                
                print(len(date),len(date),"--------------------------------")
                if len(date)==0:
                    continue
                    
                for c,d in zip(date,price):
                #     print(c,d)
                    num=str(c).split("-")
                #     print(num)
                    key="wozwaarde_"+str(num[-1])
            #         print(key,d)
                    data.update({key:d})
                if len(str(data['postcode'])) == 0:
                    data.update({"postcode":codess})
                try:
                    if len(huisnummer_extentie)==0:
                        dan=re.findall(r'[A-Z]',huisnummer)
                        if len(dan)==0:
                            dan=re.findall(r'[a-z]',huisnummer)
                        huisnummer_extentie=dan[0]
                        huisnummer=huisnummer.replace(str(dan[0]),"")
                        data.update({"huisnummer":huisnummer,"huisnummer_extentie":huisnummer_extentie})
                        
                except:
                    pass
                    
                    
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
        
    
    
    
    
    
    
    
# 1011AJ


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[74]:





# In[75]:





# In[ ]:





# In[ ]:




