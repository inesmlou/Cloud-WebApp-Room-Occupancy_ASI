#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import json

# [END imports]

# Protocolo - guarda o template e envia-o para o HTML
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
	
class User(ndb.Model):
	"""A main model for representing an individual AvRoom entry."""
	user_id = ndb.StringProperty(indexed=True, repeated=False)
	user_name = ndb.StringProperty(indexed=True, repeated=False)
	
class Room(ndb.Model):
	"""A main model for representing an individual AvRoom entry."""
	room_campus = ndb.StringProperty(repeated=True) #indexed = True
	room_edificio = ndb.StringProperty(repeated=True)
	room_piso = ndb.StringProperty(repeated=True)
	room_capacidade = ndb.StringProperty(repeated=True)
	room_sala = ndb.StringProperty(repeated=True)
	room_user = ndb.StructuredProperty(User,repeated=True)

def layout(self):
	# guarda informacao do utilizador
	user = users.get_current_user()
	if user:
		url = users.create_logout_url(self.request.uri)
		url_linktext = 'Logout'
	else:
		url = users.create_login_url(self.request.uri)
		url_linktext = 'Login'
	return url, url_linktext, user

# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
    	[url, url_linktext, user] = layout(self)

        link = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces'
        out_campus = json.load(urllib.urlopen(link))
        out_available = Room.query().fetch()
    	# administrator_logged_in
        if (users.is_current_user_admin()) and user:
       		out_edificios = json.load(urllib.urlopen(link))
       		out_pisos = json.load(urllib.urlopen(link))
       		out_salas = json.load(urllib.urlopen(link))
       		template = JINJA_ENVIRONMENT.get_template('admin.html')
       		template_values = {
	            'user': user,
	            'greetings': greetings,
	            'guestbook_name': urllib.quote_plus(guestbook_name),
	            'url': url,
	            'url_linktext': url_linktext,
	            'out_campus': out_campus, 
	            'out_edificios' : out_edificios,
	            'out_pisos' : out_pisos,
	            'out_salas' : out_salas,
	        }
	        
	    # student_logged_in
        if (not users.is_current_user_admin()) and user:
        	user_exists = User()
        	user_exists.user_id = users.get_current_user().user_id()
        	user_exists.user_name = users.get_current_user().email()
        	flag = 0
        	for i_rooms in out_available:
        		if user_exists in i_rooms.room_user:
        			flag = 1
        			choice_sala = i_rooms.key.id()
        			chosen_room = ndb.Key('Room', choice_sala).get()
        			template = JINJA_ENVIRONMENT.get_template('student.html')
		        	[url, url_linktext, user] = layout(self)
		        	template_values = {'user': user,'url': url,'url_linktext': url_linktext,'choice_room' : chosen_room,'flag' : flag,'out_available' : out_available,}
		        	break
			else:
				template = JINJA_ENVIRONMENT.get_template('student.html')
	        	[url, url_linktext, user] = layout(self)
	        	template_values = {'user': user,'url': url,'url_linktext': url_linktext,'flag' : flag,'out_available' : out_available,}
		
		# no_user_logged_in
        if not user:
        	template = JINJA_ENVIRONMENT.get_template('index.html')
        	template_values = {'user': user,'greetings': greetings,'guestbook_name': urllib.quote_plus(guestbook_name),'url': url,'url_linktext': url_linktext,}
        self.response.write(template.render(template_values))
	    
# [END main_page]

class Getedificios(webapp2.RequestHandler):
    def post(self):	# answers to the command get given by the form in html
    
        campus = self.request.get('campus')
        campus = eval(campus)
        
        link = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
        out_edificios = json.load(urllib.urlopen(link + campus['id']))
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        out_pisos = json.load(urllib.urlopen(link))
        out_salas = json.load(urllib.urlopen(link))
        # Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina.
        [url, url_linktext, user] = layout(self)
        	
        template_values = {
            'user': user,
#            'greetings': greetings,
#            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            'out_edificios': out_edificios,  
            'out_pisos': out_pisos,   
            'out_salas' : out_salas,
            'campus' : campus,
        }
        self.response.write(template.render(template_values))
        
        
class Getpisos(webapp2.RequestHandler):
    def post(self):	# answers to the command get given by the form in html
        
        building = self.request.get('building')
        building = eval(building)
        campus = self.request.get('campus')
        campus = eval(campus)
        link = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
        out_edificios = json.load(urllib.urlopen(link + campus['id']))
        out_pisos = json.load(urllib.urlopen(link + building['id']))
        out_salas = json.load(urllib.urlopen(link))
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        
        # Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina. 
        [url, url_linktext, user] = layout(self)
        
        template_values = {
            'user': user,
#           'greetings': greetings,
#           'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            'out_edificios': out_edificios,  
            'out_pisos': out_pisos,
            'out_salas' : out_salas,
            'campus' : campus,
            'building' : building,
        }
        self.response.write(template.render(template_values))
        
       
class Getsalas(webapp2.RequestHandler):
    def post(self):	# answers to the command get given by the form in html
    	
    	building = self.request.get('building')
    	building = eval(building)
        campus = self.request.get('campus')
        campus = eval(campus)
        floor = self.request.get('floor')
        floor = eval(floor)
        link = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
        out_edificios = json.load(urllib.urlopen(link + campus['id']))
        out_pisos = json.load(urllib.urlopen(link + building['id']))
        out_salas = json.load(urllib.urlopen(link + floor['id']))
        
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        
        # Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina. 
        [url, url_linktext, user] = layout(self)
        
        template_values = {
            'user': user,
#           'greetings': greetings,
#           'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            'out_edificios': out_edificios,  
            'out_pisos': out_pisos,    
            'out_salas' : out_salas,
            'campus' : campus,
            'building' : building,
            'floor' : floor,
        }
        self.response.write(template.render(template_values))
        
class Insertsalas(webapp2.RequestHandler):
    def post(self):	# answers to the command get given by the form in html
    
    	building = self.request.get('building')
    	building = eval(building)
        campus = self.request.get('campus')
        campus = eval(campus)
        
        floor = self.request.get('floor')
        floor = eval(floor)
        sala = self.request.get('room')
        sala = eval(sala)
        
        room = Room()
        if users.get_current_user():
            room.room_campus = [campus['id'], campus['name'], campus['type']]
            room.room_edificio = [building['id'], building['name'], building['type']]
            room.room_piso = [floor['id'], floor['name'], floor['type']]
            room.room_sala = [sala['id'], sala['name'], sala['type']]
            
        room.put()
        query_params = {'room': room}
        self.redirect('/?' + urllib.urlencode(query_params))
        link = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces'
        out_campus = json.load(urllib.urlopen(link))
        out_edificios = json.load(urllib.urlopen(link))
        out_pisos = json.load(urllib.urlopen(link))
        out_salas = json.load(urllib.urlopen(link))
        
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        
        # Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina. 
        [url, url_linktext, user] = layout(self)
        template_values = {
            'user': user,
#           'greetings': greetings,
#           'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
            'out_edificios': out_edificios,  
            'out_pisos': out_pisos,    
            'out_salas' : out_salas,
        }
        self.response.write(template.render(template_values))
        
        
        
class Checkinuser(webapp2.RequestHandler):
    def post(self):	# answers to the command get given by the form in html
    	
    	choice_sala = self.request.get('choice')
    	chosen_room = ndb.Key('Room', eval(choice_sala)).get()
        flag = 1
        entity = User()
        entity.user_id = users.get_current_user().user_id()
        entity.user_name = users.get_current_user().email()
        chosen_room.room_user.append(entity)
        chosen_room.put()
        
        template = JINJA_ENVIRONMENT.get_template('student.html')
        
        # Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina. 
        [url, url_linktext, user] = layout(self)
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
			'choice_room' : chosen_room,
			'flag' : flag,
        }
        self.response.write(template.render(template_values))
		
		
class Checkoutuser(webapp2.RequestHandler):
    def get(self):	# answers to the command get given by the form in html
		
		choice_sala = self.request.get('choice_out')
		chosen_room = ndb.Key('Room', eval(choice_sala)).get()
		flag = 0
		
		out_available = Room.query().fetch()
		
		user_to_delete = User()
		user_to_delete.user_id = users.get_current_user().user_id()
		user_to_delete.user_name = users.get_current_user().email()
		
		if user_to_delete in chosen_room.room_user:
			idx = chosen_room.room_user.index(user_to_delete)
			del chosen_room.room_user[idx]
			chosen_room.put()
			
		template = JINJA_ENVIRONMENT.get_template('student.html')
		
		# Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina.
		
		[url, url_linktext, user] = layout(self)
			
		template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
			'choice_room' : chosen_room,
			'flag' : flag,
			'out_available' : out_available,
		}
		
		self.response.write(template.render(template_values))
        
        
        
        
# [START app]
# actions that are called when an action is selected in the page
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/edificios', Getedificios),	# quando a variavel edificios que vem de carregar no select do form e ativada, chama a class getedificios
	('/pisos', Getpisos),
	('/salas', Getsalas),
	('/fim', Insertsalas),
	('/checkin', Checkinuser),
	('/checkout', Checkoutuser),
], debug=True)
# [END app]
