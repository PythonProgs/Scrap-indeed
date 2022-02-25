import os
import requests
from bs4 import BeautifulSoup

#Input Url, Parameter, dan Header
url = 'https://www.indeed.com/jobs?'
site = 'https://www.indeed.com'
params = {
    'q' : 'Python Developer',
    'l' : 'New York State',
    'vjk' : '71acc67a281f6038'
}

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.04638.54 Safari/537.36'}

res = requests.get(url, params=params, headers=headers)


def get_total_pages():
    params = {
        'q': 'Python Developer',
        'l': 'New York State',
        'vjk': '71acc67a281f6038'
    }

    res = requests.get(url, params=params, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

#Pengambilan Halaman
    total_pages = []
    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('ul','pagination-list')
    pages = pagination.find_all('li')
    for page in pages:
        total_pages.append(page.text)

    total=int(max(total_pages)) #Mengambil angka maksimal
    print(total)
    return total

def get_all_items():
    params = {
        'q': 'Python Developer',
        'l': 'New York State',
        'vjk': '71acc67a281f6038'
    }

    res = requests.get(url, params=params, headers=headers)

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()
    soup = BeautifulSoup(res.text, 'html.parser')

    contents = soup.find_all('table', 'jobCard_mainContent big6_visualChanges')

    #pick item
    #title
    #company name
    #company link
    #company address

    job_list = [] #untuk menampung list data
    for item in contents:
        title = item.find('h2', 'jobTitle').text
        company = item.find('span', 'companyName')
        company_name = company.text
        try:
            company_link = site + company.find('a')['href']
        except:
            company_link = 'Link is not avalable'

        #sorting data
        data_dict = {
            'Title' : title,
            'Company Name' : company_name,
            'Company Link' : company_link
        }
        job_list.append(data_dict)

    print('Jumlah Data: ', len(job_list))

if __name__ == '__main__':
    get_all_items()
