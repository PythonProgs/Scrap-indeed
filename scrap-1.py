import os #Membuat temporary file
import requests #Untuk mengambil website
import json #Untuk membuat list
from bs4 import BeautifulSoup #Untuk mengubah data website
import pandas as pd #Untuk Memasukan ke CSV dan Excel

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

def get_total_pages(query, location):
    params = {
        'q': query,
        'l': location,
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
    return total

def get_all_items(query, location, start, page):
    params = {
        'q': query,
        'l': location,
        'start' : start,
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
            company_link = 'Link is not available'

        #sorting data
        data_dict = {
            'Title' : title,
            'Company Name' : company_name,
            'Company Link' : company_link
        }
        job_list.append(data_dict)

    #Membuat JSON
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    with open(f'json_result/{query}_in_{location}_page_{page}.json', 'w+') as json_data:
        json.dump(job_list, json_data, indent=2)
    print('json created')
    return job_list

    #Membuat CSV / Excel
    """df = pd.DataFrame(job_list) #Contoh1
    df.to_csv('indeed_data.csv', index=False)
    df.to_excel('indeed_data.xlsx', index=False)
    print('Data Created Successfully')
    """

def create_document(dataFrame, filename):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass

    df = pd.DataFrame(dataFrame)
    df.to_csv(f'data_Result/{filename}.csv', index=False)
    df.to_excel(f'data_Result/{filename}.xlsx', index=False)

    print(f'File {filename}.csb and {filename}.xlsx successfully created')

def run():
    query = input('Enter Your Query: ')
    location = input('Enter Your Location: ')

    total = get_total_pages(query, location)
    counter = 0
    final_result =[]

    for page in range(total):
        page += 1
        counter +=10
        final_result += get_all_items(query, location, counter, page)

    #Format Data
    try:
        os.mkdir('reports')
    except FileExistsError:
        pass

    with open('reports/{}.json'.format(query), 'w+') as final_data:
        json.dump(final_result, final_data, indent = 2)

    print('Data Json Created')

    #Create Document
    create_document(final_result, query)

if __name__ == '__main__':
    run()
