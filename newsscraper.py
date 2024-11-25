import requests
from bs4 import BeautifulSoup

site_url = 'https://ground.news'

home_page = requests.get(f'{site_url}/').text

soup_home_page = BeautifulSoup(home_page, 'lxml')

div_elements = soup_home_page.find_all('div', class_='group')

def get_article_link(index):
    article_route = div_elements[index].find('a')['href']
    article_link = f'{site_url}{article_route}'

    article_page = requests.get(article_link).text

    soup_article_page = BeautifulSoup(article_page, 'lxml')

    summary = soup_article_page.find_all('li', class_='mb-8px')

    print(f'\nTitle: {news[index]}\nSummary:')
    for item in summary:
        print(item.text)
    print(f'Link: {article_link}\n')

def get_more_articles(soup_article_page):
    more_articles = soup_article_page.find_all('p', class_='font-normal text-18 leading-9 break-words')
    articles = []
    for article in more_articles:
        articles.append(article.text if article.text else None)
    
    for article in articles:
        print(article)
        print()

def analyze_sentiments():
    pass

news = []
for title in div_elements:
    news.append(title.find('h4').text if title.find('h4') else None)

i = 0
for title in news:
    if title:
        print(f'{i}. {title}')
        print()
    i += 1

article_index = int(input('Enter the index of the article you want to read>>> '))

get_article_link(article_index)