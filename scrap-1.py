import os
import requests
from bs4 import BeautifulSoup

url = 'https://www.indeed.com/jobs?'
params = {
    'q' : 'Python Developer',
    'l' : 'New York State',
    'vjk' : '71acc67a281f6038'
}

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.04638.54 Safari/537.36'}

res = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

def get_total_pages():
    params = {
        'q': 'Python Developer',
        'l': 'New York State',
        'vjk': '71acc67a281f6038'
    }

    res = requests.get(url, params=params, headers=headers)