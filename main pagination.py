import requests
import os
import json
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.yell.com/ucs/UcsSearchAction.do?'

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                          ' like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
base_url = 'https://www.yell.com'

def get_total_pages(searches):

    params = {
        'keywords' : 'Restaurants',
        'location' : 'london',
        'scrambleSeed' : '1290094646',
        'keywords' : searches,
        '_pgn' : 1,
    }


    res = requests.get(url, params=params, headers=headers)

    soup = BeautifulSoup(res.content, 'html.parser')

    pages = []
    headers_contents = soup.find('div','col-sm-14 col-md-16 col-lg-14 text-center').find_all('a')
    for i in headers_contents:
        pages.append(int(i.text))

    #print (headers_contents)

    total_pages = max(pages)
    print(total_pages)
    return total_pages

def get_all_item(searches,pages):
    hotelist = []
    params = {
        'keywords': 'Restaurants',
        'location': 'london',
        'scrambleSeed': '1290094646',
        'keywords': searches,
        '_pgn': pages,
    }

    res = requests.get(url,params=params, headers=headers)

    soup = BeautifulSoup(res.text,'html.parser')
    hotelist = []
    results = soup.find('div', {'class':'row results--row results--capsuleList'})
    contents = results.find_all('div', {'class':'row businessCapsule--mainRow'})

    for content in contents:
        title = content.find('h2', 'businessCapsule--name text-h2').text
        classification = content.find('span', 'businessCapsule--classification').text
        telephone = content.find('span', 'business--telephoneNumber').text
        link_web = base_url + content.find('div', 'businessCapsule--titSpons').find('a')['href']

        # sorting data
        final_data = {
            'title': title,
            'classification': classification,
            'telephone': telephone,
            'link web': link_web,
        }
        hotelist.append(final_data)
    return hotelist

def output(searches, final_result):
    # is using to print csv or excel ffile
    # parameter final_result is the result from scraping and pagination
    df = pd.DataFrame(final_result)
    df.to_csv(f'{searches}.csv', index=False)
    df.to_excel('yell_data.xlsx', index=False)

def main(searches):
    final_result = []

    total_pages = get_total_pages(searches)
    for page in range (total_pages):
        page += 1
        print(f'Scraping halaman ke:{page}')
        products = get_all_item(searches, page)
        final_result += products

    #the prosessing data here(final_result)
    total_data = len(final_result)
    print('Ini adalah total halaman yang sudah di scraping'. format(total_data))

    #generate csv used output(out of looping)
    output(searches, final_result)

if __name__ == '__main__':
    searches = ('restaurants')
    main(searches)
#data created
print('Data Created Succes')




