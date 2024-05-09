from flask import Flask, render_template, g, request
import sqlite3
from datetime import datetime

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

@app.route('/', methods=['GET', 'POST'])
def index():
  db = get_db()
  if request.method == 'POST':
    date = request.form['date']  #assume YYYY-MM-DD format
    dt = datetime.strptime(date, '%Y-%m-%d')
    database_date = dt.strftime('%Y%m%d')
    db.execute('insert into log_date (entry_date) values (?)', [database_date])
    db.commit()

  cur = db.execute('select entry_date from log_date order by entry_date desc')
  results = cur.fetchall()

  pretty_results = []
  for i in results:
    single_date = {}
    d = datetime.strptime(str(i['entry_date']), '%Y%m%d')
    single_date['entry_date'] = datetime.strftime(d, '%B %d, %Y')
    pretty_results.append(single_date)

  return render_template('home.html', results=pretty_results)

@app.route('/view/<date>', methods=['GET', 'POST']) #date in database format YYYYMMDD
def view(date):
  if request.method == 'POST':
    return f'<h1>The food item added is #{request.form['food-select']}</h1>'
  db = get_db()
  cur = db.execute('select entry_date from log_date where entry_date = ?', [date])
  result = cur.fetchone()

  # return f'<h1>The date is {result['entry_date']}</h1>'
  d = datetime.strptime(str(result['entry_date']), '%Y%m%d')
  pretty_date = datetime.strftime(d, '%B %d, %Y')

  food_cur = db.execute('select id, name from food')
  food_results = food_cur.fetchall()

  return render_template('day.html', date=pretty_date, food_results=food_results)

@app.route('/food', methods=['GET', 'POST'])
def food():
  db = get_db()
  if request.method == 'POST':
    name = request.form['food-name']
    protein = int(request.form['protein'])
    carbohydrates = int(request.form['carbohydrates'])
    fat = int(request.form['fat'])

    calories = protein * 4 + carbohydrates * 4 + fat * 9

    db.execute('insert into food (name, protein, carbohydrates, fat, calories) values (?, ? ,? ,? ,?)', [name, protein, carbohydrates, fat, calories])
    db.commit()

  cur = db.execute('select name, protein, carbohydrates, fat, calories from food')
  results = cur.fetchall()

    # return f"<h1>Name: {request.form['food-name']} Protein: {request.form['protein']} Carbs: {request.form['carbohydrates']} Fat: {request.form['fat']} </h1>"
  return render_template('add_food.html', results = results)


if __name__ == '__main__':
  app.run(debug=True)

