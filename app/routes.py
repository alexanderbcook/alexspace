from flask import render_template, request
from app import app
import json
import datetime
import utilities
from utilities import connect_to_database, close_connection, json_object_reddit

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/reddit') 
def reddit():
    conn = connect_to_database()
    cur = conn.cursor()

    argument = request.args['interval']

    # Calculate time intervals via query string params.
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if argument == 'month':
        interval = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
    elif argument == 'year':
        interval = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        interval = (datetime.datetime.now() - datetime.timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')

    # SQL queries.

    query = cur.execute("SELECT word, SUM(count) FROM reddit.politics WHERE day < %s AND day >= %s GROUP BY word ORDER BY SUM(count) DESC limit 10;", (now,interval))
    politics = cur.fetchall()
    query = cur.execute("SELECT word, SUM(count) FROM reddit.news WHERE day < %s AND day >= %s GROUP BY word ORDER BY SUM(count) DESC limit 10;", (now,interval))
    news = cur.fetchall()
    query = cur.execute("SELECT word, SUM(count) FROM reddit.the_donald WHERE day < %s AND day >= %s GROUP BY word  ORDER BY SUM(count) DESC limit 10;", (now,interval))
    thedonald = cur.fetchall()
    query = cur.execute("SELECT word, SUM(count) FROM reddit.worldnews WHERE day < %s AND day >= %s GROUP BY word ORDER BY SUM(count) DESC limit 10;", (now,interval))
    worldnews = cur.fetchall()

    close_connection(cur, conn)

    # Instantiate json objects.

    json_politics = []
    json_news = []
    json_worldnews = []
    json_thedonald = []
                                   
    # JSONify sql queries.

    json_object_reddit(json_politics, politics)
    json_object_reddit(json_news, news)
    json_object_reddit(json_worldnews, worldnews)
    json_object_reddit(json_thedonald, thedonald)


    return render_template('reddit.html', argument=argument, politics=json.dumps(json_politics), news=json.dumps(json_news), the_donald=json.dumps(json_thedonald), worldnews = json.dumps(json_worldnews))

@app.route('/superbowl')
def superbowl():

    argument = request.args['year']
    if argument == '2017':
        html = 'superbowl_2017.html'
    else:
        html = 'superbowl_2018.html'
    return render_template(html)
