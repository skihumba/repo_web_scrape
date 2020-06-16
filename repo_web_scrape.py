import requests 
import time
from  bs4 import BeautifulSoup as bs4
import csv
from tqdm import tqdm

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# http://ir.jkuat.ac.ke/handle/123456789/1293/recent-submissions?offset=0
soup_init = bs4((requests.get('http://ir.jkuat.ac.ke/handle/123456789/1154/recent-submissions?offset=0', headers=headers).content), 'lxml')
page_num = int(soup_init.find("p", class_ ="pagination-info").text.strip( ).split(sep=' ')[-1])

i = page_num // 20
range_i = range(i)

csv_file = open('COPAS_thesis_scrape.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['title', 'author', 'publisher', 'date', 'abstract', 'page_link', 'download_link'])

for ii in tqdm(range_i):
    offset_No = ii*20
    url = 'http://ir.jkuat.ac.ke/handle/123456789/1154/recent-submissions?offset='+str(offset_No) 

    page = requests.get(url, headers=headers)
    soup = bs4(page.content, 'lxml')

    base_url = 'http://ir.jkuat.ac.ke'

    art_desc = soup.find_all('div', class_='artifact-description')
    for art in art_desc:
        try:
            title = art.find("div", class_="artifact-title").find('a').text.strip()
        except:
            title = 'NO_TITLE'

        try:
            link = art.find('a')['href']
            full_link = base_url+link
            url_page = requests.get(full_link, headers=headers)
            url_soup = bs4(url_page.content, 'lxml')
            download_link = base_url+url_soup.find('a', class_="image-link")['href']
        except:
            download_link = 'NO_LINK'

        try:
            author = art.find('span', class_='author').text.strip()
        except:
            author = 'NO_AUTHOR'

        try:
            publisher = art.find('span', class_='publisher').text
        except:
            publisher = 'NO_PUBLISHER'

        try:
            date_published = art.find('span', class_='date').text
        except:
            date_published = 'NO_DATE'

        try:
            abstract = art.find("div", class_= "artifact-abstract").text.strip()
        except:
            abstract = 'NO_ABSTRACT'
             
        try:
            csv_writer.writerow([title, author, publisher, date_published, abstract, full_link, download_link])
        except:
            pass

csv_file.close()