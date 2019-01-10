#!/usr/bin/env python

class book:
	
	book_counter = 0
	
	def __init__(self, author, title, date):
		self.author=author
		self.title=title
		self.date=date
		self.identifier = book.book_counter
		book.book_counter +=1
		
	def insert_book(self):
		name = input("Name = ")
		booktitle = input("Title = ")
		bookyear = input("Date = ")
		print("a")
		book(name,booktitle, bookyear)
		
class BookDatabase:
	
	def __init__(self):
		self.DB = []
		
	
			
	def show_book(self, identifier):
				
		desired_id = input("Which is the id of your book?")
			
		if (self.identifier == desired_id):
			
			print("Book requested = %s" % self.identifier) 
			print("Book requested = %s" % self.title) 


book.insert_book

b1 = book("joao","titulo", 2016)
b2 = book("ines","titulo2", 2015)
b3 = book("alguem","titulo3", 2017)	
