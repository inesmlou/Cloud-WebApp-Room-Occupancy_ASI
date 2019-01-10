from bottle import Bottle, run, template, request
import library

class storage:
	def __init__ (self):
		self.data = []
	def store(self, query):
		self.data.append(query)
	def show(self):
		return self.data


app = Bottle()
st = storage()
@app.route('/')

@app.route('/listAuthors')
def listAuthors():
	aux = library.library('mylib')
	listaA = aux.listAuthors()
	return template(tempAuthor, listA = listaA["authors"])
	
tempAuthor = """ <ul>
   %for nameA in listA:
    <li>{{nameA}}</li>
   %end
</ul>"""

@app.route('/listBooks')
def listBooks():
	aux = library.library('mylib')
	listaB = aux.listBooks()
	return template(tempBook, listB = listaB["books"])
	
tempBook = """ <ul>
   %for titleB in listB:
    <li>{{titleB}}</li>
   %end
</ul>"""

@app.route('/api/books')
def listBooksAPI():
	print request.headers.get('Accept')
	aux = library.library('mylib')
	listaB = aux.listBooks()
	return listaB




@app.route('/query')
def query_function():
	if len(request.query) == 0:
		return template(temp, list=st.show())
	for a in request.query:
		print a, request.query[a]
		st.store(a+"="+request.query[a])
	return "just inserted the query<br>ss"





run(app, host='localhost', port=8080)
