import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

site_url = 'https://ground.news'

home_page = requests.get(f'{site_url}/').text

soup_home_page = BeautifulSoup(home_page, 'lxml')

div_elements = soup_home_page.find_all('div', class_='group')

def get_article(index):
    article_route = div_elements[int(index)].find('a')['href']
    article_link = f'{site_url}{article_route}'

    article_page = requests.get(article_link).text

    soup_article_page = BeautifulSoup(article_page, 'lxml')

    summary = soup_article_page.find_all('li', class_='mb-8px')

    print(f'\nTitle: {news[index]}\nSummary:')
    for item in summary:
        print(item.text)
    print(f'Link: {article_link}\n')

def analyze_sentiments(news):
    vader = SentimentIntensityAnalyzer()
    good_news = dict()
    neutral_news = dict()
    bad_news = dict()
    for index, title in news.items():
        sentiment = vader.polarity_scores(title)
        if sentiment['compound'] >= 0.05:
            good_news[index] = title
        elif sentiment['compound'] <= -0.05:
            bad_news[index] = title
        else:
            neutral_news[index] = title
    
    return [good_news, neutral_news, bad_news]

def remove_duplicates(news):
    unique_news = dict()
    for index, title in news.items():
        if title not in unique_news.values():
            unique_news[index] = title
    
    return unique_news

def display_news(news):
    for index, title in news.items():
        if title != 'Failed to fetch title':
            print(f'{index}. {title}')
            print()

def get_news(div_elements):
    news = dict()
    i = 0
    for title in div_elements:
        news[f'{i}'] = title.find('h4').text if title.find('h4') else 'Failed to fetch title'
        i += 1
    
    return news

news = get_news(div_elements)

news = remove_duplicates(news)

analyzed_news = analyze_sentiments(news)

user_mood = input('Enter your mood (good, neutral, bad)>>> ')

if user_mood == 'good':
    display_news(analyzed_news[0])
elif user_mood == 'neutral':
    display_news(analyzed_news[1])
elif user_mood == 'bad':
    display_news(analyzed_news[2])
else:
    display_news(news)

article_index = input('Enter the index of the article you want to read>>> ')

get_article(article_index)