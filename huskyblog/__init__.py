from pyramid.config import Configurator
from pymongo import MongoClient

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

#def pregenerator(request, elements, keywords):
#	keywords.setdefault('name', '')
#	return elements, keywords


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_dogpile_cache')

    # Configure views.py:my_view,
    config.add_route('home', '/')

    # Simply returns some data with application/json header
    config.add_route('data', '/data.json')

    # handle requests to posts paths
    config.add_route('posts', '/posts/{name}/{topic}')
    # pregenerator param may be useful at some point
    
    # serve static assets from 'static' folder
    config.add_static_view(name='static', path='huskyblog:static', cache_max_age=3600)

    # mongo_db stuff
    db_url = urlparse(settings['mongo_uri'])
    config.registry.db = MongoClient(host=db_url.hostname, port=db_url.port)
    #request methods for db??
    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db
    config.add_request_method(add_db, 'db', reify=True)

    # Make .views available to the app overall?
    config.scan('.views')
    print("Starting to listen...")
    return config.make_wsgi_app()
