from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import keywords
import database
from datetime import datetime, timedelta
import datetime as dt

class Data(BaseModel):
    key: str
    value: str

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {
    'keywords': {},
    'news': {},
    'todayNews': {}
} 

@app.get("/")
def default():
    return "Fast API News Server"

@app.get("/test/")
async def load_test():
    """
    Perform a load test by doing computationally demanding operations to showcase
    autoscaling of the server

    Returns:
        dict: A dictionary with a message indicating that the load test is completed.
    """

    return {"message": "Load Test Completed!!"}

def get_today_news():
    today = datetime.now(dt.UTC).strftime("%Y-%m-%d")
    cached_data = cache['todayNews'].get(today)

    if cached_data:
        return cached_data
    else:
        data = database.get_news_by_date()
        cache['todayNews'][today] = data
        return data

@app.get("/news/")
async def get_news():
    """
    Get aggregated news data for the current day by category from dynamodb, and send it to the frontend

    Returns:
        aggregated news data by category
    """
    return get_today_news()

def fetch_and_cache_keywords(category):
    """
    get keyword analysis based on cache
    """
    if category == "total":
        articles = database.get_all_news()
    else: 
        articles = database.get_news_by_category(category)
    analysis = keywords.get_analysis(articles)
    cache['keywords'][category] = {
        "data": analysis,
        "timestamp": datetime.now(dt.UTC)
    }

@app.get("/keywords/{category}/")
async def get_keywords_analysis(category="total"):
    """
    Get the keyword analysis
    """
    # update or invalidate cache
    if category not in cache['keywords'] or (datetime.now(dt.UTC) - cache['keywords'][category]["timestamp"]) > timedelta(hours=24):
        fetch_and_cache_keywords(category)
    return cache['keywords'][category]['data']
