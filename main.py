import requests
import os
import json
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.yell.com/ucs/UcsSearchAction.do?'

params = {
    'scrambleSeed' : '181494743',
    'keywords' : 'hotels',
    'location' : 'New York'
}

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                          ' like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
base_url = 'https://www.yell.com'
result = []

res = requests.get(url, params=params, headers=headers)

soup = BeautifulSoup(res.text, 'html.parser')

try :
    os.mkdir('json_result')
except FileExistsError:
    pass


#scraping prosess

headers_contents = soup.find_all('div','row businessCapsule--mainRow')

for content in headers_contents:
    title = content.find('h2','businessCapsule--name text-h2').text
    classification = content.find('span','businessCapsule--classification').text
    telephone = content.find('span','business--telephoneNumber').text
    link_web = base_url + content.find('div','businessCapsule--titSpons').find('a')['href']

    #sorting data
    final_data = {
        'title' : title,
        'classification' : classification,
        'telephone' : telephone,
        'link web' : link_web,
    }

    #mencetak datanya
    #print(final_data)
    result.append(final_data)
print('Jumlah datanya adalah', len(result))

try :
    os.mkdir('json_result')
except FileExistsError:
    pass

with open('json_result/final_data.json','w+') as json_data:
    json.dump(result, json_data)
print('json created')

#create csv

df = pd.DataFrame(result)
df.to_csv('yell_data.csv', index=False)
df.to_excel('yell_data.xlsx', index=False)

#data created
print('Data Created Succes')


#print (result)
for i in result:
    print(i)

