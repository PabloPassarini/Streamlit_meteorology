from bs4 import BeautifulSoup
import requests, os, re
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}


tag = 'span'
clss = '-bold -gray-dark-2 -font-55 _margin-l-20 _center'

response = requests.get('https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/170/belohorizonte', headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

val = soup.find(tag, class_=re.compile(clss)).text.strip()
print(val)