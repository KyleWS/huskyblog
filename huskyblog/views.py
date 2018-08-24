from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound
from datetime import datetime
from cached_property import cached_property
import pymongo
from bson.json_util import dumps

# view for returning jinja2 template
@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
	#return HTTPFound(location='posts')
	return {"status": "home", "time": str(datetime.now())}

# View for returning simple json
@view_config(route_name="data", renderer="json")
def data_handler(request):
	return {'url': request.url, 'time': str(datetime.now())}

# views for experiementing with view classes using both views
# and json returns
@view_defaults(route_name='posts')
class PostView:
	def __init__(self, request):
		self.request = request	
		self.view_name = 'PostViews'
		self.db = request.db
		self.collection = self.db['test_messages']


	@cached_property
	def name_topic(self):
		name = self.request.matchdict['name']
		topic = self.request.matchdict['topic']
		return name + " " + topic
		
	# Inaccessible with /posts in current setup :shrug:	
	# have to pass some value for {name} and {topic}
	@view_config(renderer='templates/post_home.jinja2')
	def post_home(self):
		name = self.request.params.get('name', 'No Name Provided')
		body = 'URL %s with name: %s' % (self.request.url, name)
		print(self.request.current_route_url())
		return {'name': name, 'page_title': 'POST HOME'}
		#return Response(content_type="text/plain", body=body)

	#Somehow the request_param parameter lets us specify the need
	# for something to be in the request body in order to
	# run :¯\_(ツ)_/¯ :
	@view_config(request_method='POST', request_param="form.edit", renderer="templates/edit.jinja2")
	def edit(self):
		new_name = self.request.params['new_name']
		return {'page_title': 'EDIT POST', 'new_name': new_name}

	@view_config(request_method='POST', request_param="form.delete", renderer="templates/delete.jinja2")
	def delete(self):
		print('deleted')
		return {'page_title': 'DELETE POST'}

	@view_config(request_method="POST", request_param="db.submit", renderer="templates/post_home.jinja2")
	def db_write(self):
		data_to_write = self.request.params['user_data']
		new_post_id = 0
		if len(data_to_write) > 0:
			print("Debugging DB write")
			print(data_to_write)
			post = {"time": datetime.now(), "user": "admin", "data": data_to_write}
			new_post_id = self.collection.insert_one(post).inserted_id
			print("Post successful")
			print(new_post_id)
		return {"page_title": new_post_id}



	@view_config(request_method="GET", request_param="db.get", renderer="json")
	def db_read(self):
		recent_5_posts = self.collection.find({}, limit=5)
		print(recent_5_posts)
		return {"data": dumps(recent_5_posts)}












