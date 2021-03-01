# Webserver

from aiohttp import web
import aiohttp
import aiohttp_jinja2
import jinja2


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
    return {
        "price_1": 30,
        "price_2": 45,
        "price_3": 60
    }

@aiohttp_jinja2.template('Safety.html.jinja2')
async def safety(request):
    return {
        "protections": ["Helmets","Harnesses","Carabiners","Belay Devices"]
    }



def main():

    app = web.Application()

    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('templates'))

    app.add_routes([web.get('/', home),
                    web.get('/Homepage', home),
                    web.get('/Locations', locations),
                    web.get('/Classes', classes),
                    web.get('/Safety', safety),
                    web.static('/static','static',show_index=False)])

    print("Hi!!! Welcome to Webserver 1.0")
    web.run_app(app, host="127.0.0.1",port=3000)



main()