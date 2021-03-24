# Webserver

from aiohttp import web
from datetime import datetime
import aiohttp_jinja2
import jinja2
import sqlite3
import requests


@aiohttp_jinja2.template('Homepage.html.jinja2')
async def home(request):
    return {
        "name": "Eamonn"
    }

@aiohttp_jinja2.template('Locations.html.jinja2')
async def locations(request):
    return {
        "location_1": "Devil's Lake",
        "location_2": "Jackson Falls",
        "location_3": "Annapolis Rock"
    }

#@aiohttp_jinja2.template('Classes.html.jinja2')
async def classes(request):
    conn = sqlite3.connect('tweet_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tweets ORDER BY Likes DESC")
    results = cursor.fetchall()
    context = {"results": results,
               "price_1": 30,
               "price_2": 45,
               "price_3": 60,
               "tweets": results
               }
    response = aiohttp_jinja2.render_template('Classes.html.jinja2',
                                              request,
                                              context)
    response.set_cookie('logged_in', 'yes')
    return response

@aiohttp_jinja2.template('Safety.html.jinja2')
async def safety(request):
    return {
        "protections": ["Helmets","Harnesses","Carabiners","Belay Devices"]
    }

async def add_tweet(request):
    data = await request.post()
    content = data['content']

    # Getting the user location
    target = request.remote
    # target = "8.8.8.8"
    print("User is coming from %s" % target)
    location = get_location(target)
    print("User is at: %s " % location)

    # Date-time info: The time isn't in the correct timezone for the AWS site :(
    now = datetime.now()
    current_time = now.strftime("%B %d, %Y at %I:%M %p")

    # INSERT INTO Tweets(content,likes) VALUES ("new tweet!",0);
    conn = sqlite3.connect('tweet_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tweets (Content,TimeStamp,Likes,Location) VALUES (?,?,0,?)", (content,current_time,location))
    conn.commit()
    print("The user tweeted:  %s" % data['content'])
    raise web.HTTPFound('/Classes')

async def like(request):
    conn = sqlite3.connect('tweet_db.db')
    cursor = conn.cursor()
    tweet_id = request.query['id']
    query = "SELECT Likes FROM Tweets WHERE id=?", (tweet_id,)
    print("Query:  %s" % query)
    cursor.execute(query)
    like_count = cursor.fetchone()[0]
    # add 1 to the like count and save it
    cursor.execute("UPDATE Tweets SET Likes=? WHERE id=?", (like_count + 1, tweet_id))
    conn.commit()
    conn.close()
    raise web.HTTPFound('/Classes')

async def like_json(request):
    conn = sqlite3.connect('tweet_db.db')
    cursor = conn.cursor()
    tweet_id = request.query['id']
    cursor.execute("SELECT Likes FROM Tweets WHERE id=?", (tweet_id,))
    like_count = cursor.fetchone()[0]
    # add 1 to the like count and save it
    cursor.execute("UPDATE Tweets SET Likes=? WHERE id=?", (like_count + 1, tweet_id))
    conn.commit()
    conn.close()
    return web.json_response(data={"like_count": like_count+1})

def get_location(target):
    api_key = "15e4c318fe79628787ed5571ea69f63f"
    result = requests.get("http://api.ipstack.com/%s?access_key=%s" % (target, api_key))
    ip_address_info = result.json()
    return ip_address_info["city"]



def main():

    app = web.Application()

    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates'))

    app.add_routes([web.get('/', home),
                    web.get('/Homepage', home),
                    web.get('/Locations', locations),
                    web.get('/Classes', classes),
                    web.get('/Safety', safety),
                    web.static('/static','static',show_index=False),
                    web.post('/tweet', add_tweet),
                    web.get('/like',like),
                    web.get('/like.json',like_json)])

    print("Hi!!! Welcome to Webserver 1.0")
    web.run_app(app, host="0.0.0.0",port=80)



main()