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
       		occ_vec = countUsers(self)
       		template = JINJA_ENVIRONMENT.get_template('admin.html')
       		template_values = {
       		    'user': user,
       		    'url': url,
       		    'url_linktext': url_linktext,
       		    'out_campus': out_campus, 
       		    'out_edificios' : out_edificios,
       		    'out_pisos' : out_pisos,
       		    'out_salas' : out_salas,
       		    'out_available' : out_available,
       		    'occ_vec' : occ_vec,
				'len_occ_vec' : len(occ_vec),
       		}
       		self.response.write(template.render(template_values))
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
        			self.response.write(template.render(template_values))
        			break
        	else:
        		template = JINJA_ENVIRONMENT.get_template('student.html')
        		[url, url_linktext, user] = layout(self)
        		template_values = {'user': user,'url': url,'url_linktext': url_linktext,'flag' : flag,'out_available' : out_available,}
        		self.response.write(template.render(template_values))
        # no_user_logged_in
        if not user:
        	template = JINJA_ENVIRONMENT.get_template('index.html')
        	template_values = {'user': user,'url': url,'url_linktext': url_linktext,'out_available' : out_available,}
        	self.response.write(template.render(template_values))

# [END main_page]

class Getedificios(webapp2.RequestHandler):
	def get(self):
		[url, url_linktext, user] = layout(self)
		if not user:
			template = JINJA_ENVIRONMENT.get_template('index.html')
			template_values = {
				'user': user,
				'url': url,
				'url_linktext': url_linktext,
			}
			self.response.write(template.render(template_values))

	def post(self):	# answers to the command get given by the form in html
		link1 = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces'
		out_campus = json.load(urllib.urlopen(link1))
		out_available = Room.query().fetch()
		campus = self.request.get('campus')
		campus = eval(campus)
		link = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
		out_edificios = json.load(urllib.urlopen(link + campus['id']))
		template = JINJA_ENVIRONMENT.get_template('admin.html')
		out_pisos = json.load(urllib.urlopen(link))
		out_salas = json.load(urllib.urlopen(link))
		occ_vec = countUsers(self)
		# Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina.
		[url, url_linktext, user] = layout(self)
		print campus 
		print campus['id']
		template_values = {'user': user,'url': url,'url_linktext': url_linktext,'out_edificios': out_edificios,  
			'out_pisos': out_pisos,   
			'out_salas' : out_salas,
			'campus' : campus,
			'selected_value_campus' : campus,
			'out_campus' : out_campus,
			'out_available' : out_available,
			'occ_vec' : occ_vec,
			'len_occ_vec' : len(occ_vec),
		}
		self.response.write(template.render(template_values))
		
		
class Getpisos(webapp2.RequestHandler):
	def post(self):	# answers to the command get given by the form in html
		link1 = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces'
		out_campus = json.load(urllib.urlopen(link1))
		out_available = Room.query().fetch()
		building = self.request.get('building')
		building = eval(building)
		campus = self.request.get('campus')
		campus = eval(campus)
		link = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
		out_edificios = json.load(urllib.urlopen(link + campus['id']))
		out_pisos = json.load(urllib.urlopen(link + building['id']))
		out_salas = json.load(urllib.urlopen(link))
		occ_vec = countUsers(self)
		template = JINJA_ENVIRONMENT.get_template('admin.html')
		
		# Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina. 
		[url, url_linktext, user] = layout(self)
		
		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'selected_value_building' : building,
			'selected_value_campus' : campus,			
			'out_campus' : out_campus,
			'out_edificios': out_edificios,  
			'out_pisos': out_pisos,
			'out_salas' : out_salas,
			'campus' : campus,
			'building' : building,
			'out_available' : out_available,
			'occ_vec' : occ_vec,
			'len_occ_vec' : len(occ_vec),
		}
		self.response.write(template.render(template_values))
		
	   
class Getsalas(webapp2.RequestHandler):
	def post(self):	# answers to the command get given by the form in html
		link1 = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces'
		out_campus = json.load(urllib.urlopen(link1))
		out_available = Room.query().fetch()
		out_users = User.query().fetch()
		#out_users = out_available.room_user #NL

		user_to_show = User()
#		user_to_show.user_id = users.get_current_user().user_id()
#		user_to_show.user_name = users.get_current_user().email()
#			if user_to_show in chosen_room.room_user:
#				idx = chosen_room.room_user.index(user_to_show)
#				del chosen_room.room_user[idx]
#				chosen_room.put()
#		choice_sala = self.request.get('choice_out')
#		chosen_room = ndb.Key('Room', eval(choice_sala)).get()

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
		occ_vec = countUsers(self)
		template = JINJA_ENVIRONMENT.get_template('admin.html')
		
		# Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina. 
		[url, url_linktext, user] = layout(self)
		
		template_values = {
			'user': user,
			'url': url,
			'url_linktext': url_linktext,
			'selected_value_pisos' : floor,
			'selected_value_building' : building,
			'selected_value_campus' : campus,			
			'out_campus' : out_campus,
			'out_edificios': out_edificios,  
			'out_pisos': out_pisos,	
			'out_salas' : out_salas,
			'campus' : campus,
			'building' : building,
			'floor' : floor,
			'out_available' : out_available,
			'occ_vec' : occ_vec,
			'len_occ_vec' : len(occ_vec),
		}
		self.response.write(template.render(template_values))
		
class Insertsalas(webapp2.RequestHandler):
	def post(self):	# answers to the command get given by the form in html
		out_available = Room.query().fetch()
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
		
			# Nao deixa adicionar salas repetidas
			for space in out_available:
				if space.room_sala:
					#print space.room_sala[0]
					if space.room_sala[0] == sala['id']:
						print 'YESSSSS'
						existing_room = 1
						break
			else:
				existing_room = 0
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
			'url': url,
			'url_linktext': url_linktext,
			'out_edificios': out_edificios,  
			'out_pisos': out_pisos,	
			'out_salas' : out_salas,
			'out_available' : out_available,
			'existing_room' : existing_room,
		}
		self.response.write(template.render(template_values))
		
		
		
class Checkinuser(webapp2.RequestHandler):
#	def get(self):
#		[url, url_linktext, user] = layout(self)
#		print user
#		if not user:
#			template = JINJA_ENVIRONMENT.get_template('index.html')
#			# Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina. 
#			template_values = {
#				'user': user,
#				'url': url,
#				'url_linktext': url_linktext,
#			}
#			self.response.write(template.render(template_values))
		
	def post(self):	# answers to the command get given by the form in html
		choice_sala = self.request.get('choice')
		chosen_room = ndb.Key('Room', eval(choice_sala)).get()
		flag = 1
		out_available = Room.query().fetch()
		[url, url_linktext, user] = layout(self)
		if user:
			entity = User()
			entity.user_id = users.get_current_user().user_id()
			entity.user_name = users.get_current_user().email()
			# Procura se o estudante ja esta checked in noutra sala
			for spaces in out_available:
				# Se sim, faz o check out nessa sala
				if entity in spaces.room_user:
					idx = spaces.room_user.index(entity)
					del spaces.room_user[idx]
					spaces.put()
					break
			# E o check in na nova
			chosen_room.room_user.append(entity)
			chosen_room.put()
			template = JINJA_ENVIRONMENT.get_template('student.html')
			# Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina. 
			template_values = {
				'user': user,
				'url': url,
				'url_linktext': url_linktext,
				'choice_room' : chosen_room,
				'flag' : flag,
				'out_available' : out_available,
			}
		if not user:
			template = JINJA_ENVIRONMENT.get_template('index.html')
			template_values = {'user': user,'url': url,'url_linktext': url_linktext,'out_available' : out_available,}
		self.response.write(template.render(template_values))


class Checkoutuser(webapp2.RequestHandler):
	def get(self):	# answers to the command get given by the form in html
		
		choice_sala = self.request.get('choice_out')
		chosen_room = ndb.Key('Room', eval(choice_sala)).get()
		flag = 0
		[url, url_linktext, user] = layout(self)
		out_available = Room.query().fetch()
		if user:
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
		if not user:
			template = JINJA_ENVIRONMENT.get_template('index.html')
			template_values = {'user': user,'url': url,'url_linktext': url_linktext,'out_available' : out_available,}
		self.response.write(template.render(template_values))
			

def countUsers(self):
	occ_vec= []	
	out_available = Room.query().fetch()
	for space in out_available:
		occ_vec.append(len(space.room_user))
	return occ_vec


class ListUsers(webapp2.RequestHandler):
	def get(self):
		studList = []
		find_user = 0
		sala_users = self.request.get('roomUsers')
		flag=0
		flag1=0
		if sala_users:
			flag=2
			print 'ROOM USERS'
			chosen_room = ndb.Key('Room', eval(sala_users)).get()
			for people in chosen_room.room_user:
				studList.append(people.user_name)
		else:
			studList = 0
			flag=3
			find_user = self.request.get('username')
			if find_user:
				out_available = Room.query().fetch()
				print 'FIND USER'
				
				for place in out_available:
					if flag1==1:
						break
					else:
						for studs in place.room_user:
							if find_user == studs.user_name:
								chosen_room = place
								print 'Encontrei'
								print chosen_room
								flag1=1
								break
				#the user is not logged in
				else:
					chosen_room = []
					print "the user is not logged in"
			
			
		template = JINJA_ENVIRONMENT.get_template('StudentList.html')
		# Passa as informacoes guardadas do utilizador, para o HTML. o template e a troca entre o codigo e a pagina.
		template_values = {
			'choice_room' : chosen_room,
			'studList' : studList,
			'find_user' : find_user,
			'flag' : flag,
		}
		self.response.write(template.render(template_values))


class Home(webapp2.RequestHandler):
    def get(self):
		self.response.write('Login with Facebook or ')
	
# [START app]
# actions that are called when an action is selected in the page
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/edificios', Getedificios),	# quando a variavel edificios que vem de carregar no select do form e ativada, chama a class getedificios
	('/pisos', Getpisos),
	('/salas', Getsalas),
	('/fim', Insertsalas),
	('/checkin', Checkinuser),
	('/checkout', Checkoutuser),
	('/goBack', MainPage),
	('/listUsers', ListUsers),
	('/findUsers', ListUsers),
	
#	webapp2.Route(r'/login/<:.*>', Login, handler_method='any'),
	webapp2.Route(r'/home', Home),
	
], debug=True)
# [END app]
