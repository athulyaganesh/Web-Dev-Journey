from flask import Flask,session, url_for, redirect, render_template, request, make_response, abort, jsonify, flash
from markupsafe import escape
from werkzeug.utils import secure_filename
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import request


app = Flask(__name__) 


#Routing 
@app.route('/')
def index():
   return 'Index page'

@app.route('/hello')
def hello():
   return 'Hello World'



#Variable Rules
@app.route('/user/<user>')
def show_user_profile(user):
#Show the user profile for that user
   return 'User '+ user

#Unique URLS / Redirection Behaviour
@app.route('/projects/')
def projects():
   return 'The projects page'
#these functions differ because of the trailing slash

@app.route('/about')
def about():
   return 'The about page'


#HTTP Methods and Static Files


#open login.html in myproj

@app.route('/yes/<name>')
def yes(name):
   return "Success! Welcome "+ name

@app.route('/login', methods =['POST','GET'])
def login():
   if request.method=='POST':
      user = request.form['nm']
      return redirect(url_for('yes',name=user))
   else:
      user=request.args.get('nm')
      return redirect(url_for('yes',name=user))


# Rendering templates

@app.route('/hello/')
def hello1(name=None):
   return render_template('hello.html', name=name)

#Request object

@app.route('/login2', methods=['POST','GET'])
def login2():
   error = None
   if request.method == 'POST':
      if valid_login(request.form['username'],
                     request.form['password']):
         return log_the_user_in(request.form['username'])
      else:
         error = 'invalid id/password'

   return render_template('login.html', error = error) 


#File Upload
@app.route('/upload')
def upload_files():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'



#Cookies
@app.route('/cookie')
def index1():
   return render_template('index.html')
#form is published to /setcookie URL, and associated view function sets the
#cookie name userID and renders anothr page readcookie.html that leads to /getcookie URL
@app.route('/setcookie',methods=['POST','GET'])
def setcookie():
   if request.method=='POST':
      user = request.form['nm']

      resp = make_response(render_template('readcookie.html'))
      resp.set_cookie('userID', user)
   return resp

@app.route('/getcookie')
def getcookie():
   name=request.cookies.get('userID')
   return 'Welcome ' + name  



#Redirects and errors..
@app.route('/loginerror')
def login3():
   abort(403)
   this_is_never_executed()
   
@app.route('/redirect')
def index2():
   return redirect(url_for('login3'))
 




#API's with JSON
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]# test data for the catalog as a list of dictionaries 


@app.route('/api', methods =['GET'])
def home():
   return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
   return jsonify(books)




#Sessions --> Stores information specidic to a user from one request to the next

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/session')
def index4():
   if 'username' in session:
      return 'Logged in as %s' % escape(session['username'])
   return 'Not logged in..'

@app.route('/login3', methods=['GET','POST'])
def login5():
   if request.method == 'POST':
      session['username'] = request.form['username']
      return redirect(url_for('index'))
   return '''
      <form method = "post">
         <p><input type = text name= username>
         <p><input type = submit value = Login>
      </form>
      '''
@app.route('/logout')
def logout():
   #remove the username from the session if its there
   session.pop('username', None)
   return redirect(url_for('index'))




#Message Flashing---?

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/flash')
def index6():
   return render_template('i.html')

@app.route('/loginagain', methods=['GET', 'POST'])
def login6():
   error = None
   if request.method == 'POST':
      if request.form['username'] != 'admin' or \
            request.form['password'] != 'secret':
         flash('Invalid Password/username provided', 'error')
         error = 'invalid credentials'
         
      else:
         flash('You were successfully logged in')
         return redirect(url_for('index'))
   return render_template('l.html', error = error)




#Logging
@app.route('/log')
def foo():
   app.logger.warning('A warning occured (%d apples)', 42)
   app.logger.error('An error occurred')
   app.logger.info('Info')
   return "foo"

if __name__ == '__main__':
   handler = RotatingFileHandler('foo.log',maxBytes=10000, backupCount=1)
   handler.setLevel(logging.INFO)
   app.logger.addHandler(handler)
   app.run(debug = True)




    

    
