#!/usr/bin/env python

import urllib2
import json

def main():
 
	
	exit = False
	while not exit:
		l = raw_input("add? search? list? quit? listbooks?")
		l = l.split()
		
		if len(l)==1:
			command = l[0].upper()
			if command=='QUIT':
				exit = True
			elif command == 'ADD':
				l = raw_input('Insert author title and date separated by # :\n')
				processed_line = l.split('#')
				if len(processed_line) ==3:
					pass
			elif command == 'SEARCH':
				l = raw_input('Insert id :\n')
				processed_line = l.split()
				print processed_line
				if len(processed_line) ==1:
					pass
				if len(processed_line) ==0:
					data = urllib2.urlopen('http://localhost:8080/api/books').read()
					d = json.loads(data)
					print data
					
					
			elif command == 'LIST':			
				l = raw_input('Insert name :\n')
				processed_line = l.split()
				print processed_line[0]
				if len(processed_line) ==1:
					pass
					
			elif command == 'LISTBOOKS':			
				data = urllib2.urlopen('http://localhost:8080/api/books').read()
				d = json.loads(data)
				print data
				
			else:
				pass			
		
		if len(l)==1 and l[0]=='quit':
			exit = True
    
    

if __name__=="__main__":
    main() 
