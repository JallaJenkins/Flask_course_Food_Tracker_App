from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

def connect_db():
  sql = sqlite3.connect('food_log.db')
  sql.row_factory = sqlite3.Row
  return sql

def get_db():
  if not hasattr(g, 'sqlite3_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

@app.teardown_appcontext
def close(error):
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/view_day')
def view():
  return render_template('day.html')

@app.route('/add_food')
def food():
  return render_template('add_food.html')


if __name__ == '__main__':
  app.run(debug=True)

