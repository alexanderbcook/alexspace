from flask import render_template, request
from app import app
import json
import datetime
import utilities
from utilities import connect_to_database, close_connection

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/reddit') 
def reddit():
    conn = connect_to_database()
    cur = conn.cursor()

    argument = request.args['interval']

    # Instantiate json objects.

    json_politics = []
    json_news = []
    json_worldnews = []
    json_donald = []

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
    the_donald = cur.fetchall()
    query = cur.execute("SELECT word, SUM(count) FROM reddit.worldnews WHERE day < %s AND day >= %s GROUP BY word ORDER BY SUM(count) DESC limit 10;", (now,interval))
    world_news = cur.fetchall()

    # JSONify sql queries.

    for word in politics:
        json_politics.append(
            {
                "word":word[0],
                "count":word[1],
            }
        )
    for word in news:
        json_news.append(
            {
                "word":word[0],
                "count":word[1],
            }
        )
    for word in world_news:
        json_worldnews.append(
           {
                "word":word[0],
                "count":word[1],
            }
        )
    for word in the_donald:
        json_donald.append(
            {
                "word":word[0],
                "count":word[1],
            }
        )

    close_connection(cur, conn)

    return render_template('reddit.html', argument=argument, politics=json.dumps(json_politics), news=json.dumps(json_news), the_donald=json.dumps(json_donald), worldnews = json.dumps(json_worldnews))
