import requests
from bs4 import BeautifulSoup

url = 'https://www.yell.com/ucs/UcsSearchAction.do?'

params = {
    'scrambleSeed' : '181494743',
    'keywords' : 'hotels',
    'location' : 'New York'
}

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                          ' like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
result = []

res = requests.get(url, params=params, headers=headers)

soup = BeautifulSoup(res.text, 'html.parser')

#scraping prosess

headers_contents = soup.find_all('div','row businessCapsule--mainRow')

for contents in headers_contents:
    title = contents.find('h2','businessCapsule--name text-h2').text
    classification = contents.find('span','businessCapsule--classification').text
    link_web = contents.find('div','col-sm-24 businessCapsule--ctas').find('a')['href']

    #sorting data
    data_dict = {
        'title' : title,
        'classification' : classification,
        'link web' : link_web
    }

    #mencetak datanya
    print(data_dict)
    result.append(data_dict)
print('Jumlah datanya adalah', len(result))