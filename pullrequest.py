import requests
import pandas as pd
import requestmain as rm
import schedule
import engine
from datetime import timedelta, datetime
from time import sleep

# get unix time code for one week prior to the call
def timestamp():
    currtime = datetime.datetime.now()
    day7 = currtime - timedelta(days = 7)
    unixtime = int(day7.timestamp())
    return unixtime

# pull the top 50 games for the week based on ratings
def gamespull():
    gamedata = requests.post(rm.base_url + 'games', **{
        'headers': rm.headers,
        'data': 'fields aggregated_rating, first_release_date, follows, genres, keywords, name, rating, rating_count, slug, tags, themes, total_rating, url; where date >' + timestamp + '& category = 0 & total_rating > 70; sort total_rating desc; limit 50;'
        }
    )
    gamejson = gamedata.json();
    gamecsv = pd.read_json(gamejson, convert_dates = True)
    return gamecsv

# pull the genres and their identifiers (already in postgres)
def genrepull():
    genredata = requests.post(rm.base_url + 'genres', **{
        'headers': rm.headers,
        'data': 'fields *; limit 60;'
        }
    )
    genrejson = genredata.json();
    genrecsv = pd.read_json(genrejson, convert_dates = True)
    return genrecsv

# post the request, create csv, and push the data to postgres
def fetch():
    if requests.status_code == 200:
        curweekgames = gamespull()
        curweekgames.to_sql('games', engine.engine, if_exists = 'append', index = False)
    else:
        print('Failed to fetch data from the API')

# schedule a weekly fetch
schedule.every().monday.at('08:00').do(fetch())

# have the program check only every 12 hours if it's time to make a call
while True:
    schedule.run_pending()
    sleep(43200)