from flask import render_template, request
from app import app
import json
import datetime
import utilities
from utilities import connect_to_database, close_connection, json_object_reddit,json_object_sentiment,json_object_category,json_object_views,json_object_gender,json_object_year,json_object_views

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

    # Instantiate json objects.

    json_politics = []
    json_news = []
    json_worldnews = []
    json_thedonald = []
                                   
    # Populate JSON objects.

    json_object_reddit(json_politics, "politics", interval, now, cur)
    json_object_reddit(json_news, "news", interval, now, cur)
    json_object_reddit(json_worldnews, "worldnews", interval, now, cur)
    json_object_reddit(json_thedonald, "the_donald", interval, now, cur)

    close_connection(cur, conn)



    return render_template('reddit.html',
                    argument=argument, 
                    politics=json.dumps(json_politics), 
                    news=json.dumps(json_news), 
                    the_donald=json.dumps(json_thedonald), 
                    worldnews = json.dumps(json_worldnews))

@app.route('/superbowl')
def superbowl():

    argument = request.args['year']
    if argument == '2017':
        html = '/superbowl/2017/superbowl.html'
    else:
        html = '/superbowl/2018/superbowl.html'
    return render_template(html)

@app.route('/erowid/sentiment')
def sentiment():
    conn = connect_to_database()
    cur = conn.cursor()

    #Instantiate JSON objects

    both = []
    female = []
    male = []

    cannabis = []
    amphetamines = []
    lsd = []
    mushrooms = []
    mdma = []
    ketamine = []
    cocaine = []
    

    # Both gendered sentiment query.

    json_object_sentiment("cannabis",both,None,cur)
    json_object_sentiment("amphetamines",both,None,cur)
    json_object_sentiment("lsd",both,None,cur)
    json_object_sentiment("mushrooms",both,None,cur)
    json_object_sentiment("mdma",both,None,cur)
    json_object_sentiment("ketamine",both,None,cur)
    json_object_sentiment("cocaine",both,None,cur)

    # Female gendered sentiment query.

    json_object_sentiment("cannabis",female,'\'Female\'',cur)
    json_object_sentiment("amphetamines",female,'\'Female\'',cur)
    json_object_sentiment("lsd",female,'\'Female\'',cur)
    json_object_sentiment("mushrooms",female,'\'Female\'',cur)
    json_object_sentiment("mdma",female,'\'Female\'',cur)
    json_object_sentiment("ketamine",female,'\'Female\'',cur)
    json_object_sentiment("cocaine",female,'\'Female\'',cur)

    # Male gendered sentiment query. 

    json_object_sentiment("cannabis",male,'\'Male\'',cur)
    json_object_sentiment("amphetamines",male,'\'Male\'',cur)
    json_object_sentiment("lsd",male,'\'Male\'',cur)
    json_object_sentiment("mushrooms",male,'\'Male\'',cur)
    json_object_sentiment("mdma",male,'\'Male\'',cur)
    json_object_sentiment("ketamine",male,'\'Male\'',cur)
    json_object_sentiment("cocaine",male,'\'Male\'',cur)  

    # Category query.

    json_object_category("cannabis",cannabis,cur)
    json_object_category("amphetamines",amphetamines,cur)
    json_object_category("lsd",lsd,cur)
    json_object_category("mushrooms",mushrooms,cur)
    json_object_category("mdma",mdma,cur)
    json_object_category("ketamine",ketamine,cur)
    json_object_category("cocaine",cocaine,cur)

    close_connection(cur, conn)

    return render_template('erowid/sentiment.html', 
                        both = json.dumps(both), 
                        female= json.dumps(female),
                        male = json.dumps(male),
                        cannabis=json.dumps(cannabis),
                        amphetamines=json.dumps(amphetamines),
                        lsd=json.dumps(lsd),
                        mushrooms=json.dumps(mushrooms),
                        mdma=json.dumps(mdma), 
                        ketamine=json.dumps(ketamine), 
                        cocaine=json.dumps(cocaine)
                        )

@app.route('/erowid/users')
def users():
    conn = connect_to_database()
    cur = conn.cursor()

    genders = []
    years = []
    views = []

    json_object_gender(genders, cur)
    json_object_year(years, cur)
    json_object_views(views, cur)

    close_connection(cur, conn)

    return render_template('erowid/users.html', 
                    genders=json.dumps(genders), 
                    years=json.dumps(years), 
                    views=json.dumps(views))
