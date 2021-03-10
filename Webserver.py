# Webserver

from aiohttp import web
import aiohttp
import aiohttp_jinja2
import jinja2
import sqlite3


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

@aiohttp_jinja2.template('Classes.html.jinja2')
async def classes(request):
    conn = sqlite3.connect('tweet_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tweets ORDER BY Likes DESC")
    results = cursor.fetchall()
    return {
        "price_1": 30,
        "price_2": 45,
        "price_3": 60,

        "tweets": results
    }

@aiohttp_jinja2.template('Safety.html.jinja2')
async def safety(request):
    return {
        "protections": ["Helmets","Harnesses","Carabiners","Belay Devices"]
    }

async def add_tweet(request):
    data = await request.post()
    content = data['content']
    # INSERT INTO Tweets(content,likes) VALUES ("new tweet!",0);
    query = "INSERT INTO Tweets (content, likes) VALUES (\"%s\",0)" % content
    print("Query:  %s" % query)
    conn = sqlite3.connect('tweet_db.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print("The user tweeted:  %s" % data['content'])
    raise web.HTTPFound('/Classes')

async def like(request):
    conn = sqlite3.connect('tweet_db.db')
    cursor = conn.cursor()
    tweet_id = request.query['id']
    cursor.execute("SELECT Likes FROM Tweets WHERE id=%s" % tweet_id)
    like_count = cursor.fetchone()[0]
    # add 1 to the like count and save it
    cursor.execute("UPDATE Tweets SET Likes=%d WHERE id=%s" % (like_count + 1, id))
    conn.commit()
    conn.close()
    raise web.HTTPFound('/Classes')



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
                    web.get('/like',like)])

    print("Hi!!! Welcome to Webserver 1.0")
    web.run_app(app, host="127.0.0.1",port=3000)



main()