import json
import requests
import os
import uuid
import boto3
from datetime import datetime

client = boto3.client('dynamodb')


def format_article_for_db(article):
    item = {
        "author": {
            "S": article['author'] or "not_available"
        },
        "description": {
            "S": article['description'] or "not_available"
        },
        "content": {
            "S": article['content'] or "not_available"
        },
        "publishedAt": {
            "S": article['publishedAt'] or "not_available"
        },
        "source": {
            "S": article['source']['name'] or "not_available"
        },
        "title": {
            "S": article['title'] or "not_available"
        },
        "url": {
            "S": article['title'] or "not_available"
        },
        "urlToImage": {
            "S": article['urlToImage'] or "not_available"
        }
    }
    return item


def write_to_database(category, result_obj):
    if not result_obj:
        return 
    
    new_id = str(uuid.uuid4())
    today_date = datetime.today().strftime('%Y-%m-%d')

    articles = result_obj['articles']
    articles_list_for_db = []
    for article in articles:
        formatted_article_obj = format_article_for_db(article)
        articles_list_for_db.append({ "M": formatted_article_obj})

    try:   
        client.put_item(
            TableName = 'news_table_us-east-2',
            Item = {
                "id": {
                    "S": new_id
                },
                "date_created": {
                    "S": today_date
                },
                "category": {
                    "S": category
                },
                "articles": {
                    "L":  articles_list_for_db
                }
            }
        )
        print(f"success saving {category} articles\n")
    except Exception as e:
        print(f'error saving article {article["title"]}: ', e)

        
    
def call_news_url(category, url):
    
    result = None
    
    try:
        result = requests.get(url).json()
        print(f"{category} articles count: ", len(result['articles']))
    except Exception as e:
        print(f"error fetching {category}: ", e )
        
    return result

    
def lambda_handler(event, context):
    
    NEWS_API_KEY = os.environ["NEWS_API_KEY"]
    
    # get general top headlines
    category = "topHeadlines"
    url_top_headlines = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    result_obj = call_news_url(category, url_top_headlines)
    write_to_database(category, result_obj)
   
    # get business articles
    category = "business"
    url_business = f'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={NEWS_API_KEY}'
    result_obj = call_news_url(category, url_business)
    write_to_database(category, result_obj)
    
    # get entertainment articles
    category = "entertainment"
    url_entertainment = f'https://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey={NEWS_API_KEY}'
    result_obj = call_news_url(category, url_business)
    write_to_database(category, result_obj)
    
    # get health articles
    category = "health"
    url_health = f'https://newsapi.org/v2/top-headlines?country=us&category=health&apiKey={NEWS_API_KEY}'
    result_obj = call_news_url(category, url_business)
    write_to_database(category, result_obj)
    
    # get scieence articles
    category = "science"
    url_health = f'https://newsapi.org/v2/top-headlines?country=us&category=science&apiKey={NEWS_API_KEY}'
    result_obj = call_news_url(category, url_business)
    write_to_database(category, result_obj)
    
    # get sports articles
    category = "sports"
    url_health = f'https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey={NEWS_API_KEY}'
    result_obj = call_news_url(category, url_business)
    write_to_database(category, result_obj)
    
    # get technology articles
    category = "technology"
    url_health = f'https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={NEWS_API_KEY}'
    result_obj = call_news_url(category, url_business)
    write_to_database(category, result_obj)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
