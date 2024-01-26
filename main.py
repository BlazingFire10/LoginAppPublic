from flask import Flask, render_template, request, request
import sqlite3

from werkzeug.utils import redirect

app = Flask(__name__)

conn = sqlite3.connect('passw.db', check_same_thread=False)
c = conn.cursor()

def create_table():
  sql = '''
  CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
  )
  '''
  c.execute(sql)


def addAcct(user, pas):
  sql = "INSERT INTO passwords (username, password) VALUES (?,?)"
  c.execute(sql, (user,pas))
  conn.commit()

@app.route('/logout') 
def logout():
  return redirect('/')

@app.route('/login', methods = ['POST', 'GET'])
def login():
  if request.method == 'GET':
    return redirect('/')
  else:
    sql = 'SELECT username FROM passwords WHERE username = (?)'
    sql2 = 'SELECT password FROM passwords WHERE username = (?)'
    
    if c.execute(sql, (request.form['username'],)).fetchone() != None and c.execute(sql2, (request.form['username'],)).fetchone()[0] == request.form['password']:
      return redirect(f'/home/{request.form["username"]}')
    else:
      return render_template('login.html', message = "Username and password do not match (or there is no account tied to this username)")

@app.route('/register', methods = ['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')

  else:
    sql = "SELECT username from passwords WHERE username = (?)"
    if request.form['confirm-password'] != request.form['password']:
      return render_template('register.html', message = "Passwords don't match")
    if c.execute(sql, (request.form['username'],)).fetchone() != None:
      return render_template('register.html', message = "Username already taken")
    else:
      addAcct(request.form['username'], request.form['password'])
      return redirect(f'/home/{request.form["username"]}')

@app.route('/home/<username>')
def home(username):
  return render_template('index.html', username = username)
  
@app.route('/')
def main():
  create_table()
  return render_template('login.html')

app.run(host='0.0.0.0', port=81)

