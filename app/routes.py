from flask import render_template, request, url_for
from app import app
import json
import datetime
import random
import utilities
from utilities import connect_to_database, close_connection, json_object_reddit,json_object_search,json_object_sentiment,json_object_category,json_object_view,json_object_gender,json_object_year,json_object_time_series,json_object_events

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/sffpc')
def sffpc():
    return render_template('sffpc.html')
    
@app.route('/reddit/performance')
def performance():
    return render_template('/reddit/performance.html')

@app.route('/reddit/outages')
def outages():
    return render_template('/reddit/outages.html')

@app.route('/reddit/topwords', methods=['GET','POST']) 
def topwords():
    conn = connect_to_database()
    cur = conn.cursor()

    if request.args['interval']:
        argument = request.args['interval']

    # Instantiate data arrays.

    json_custom_politics = []
    json_custom_news = []
    json_custom_worldnews = []

    json_day_politics = []
    json_day_news = []
    json_day_worldnews = []

    json_month_politics = []
    json_month_news = []
    json_month_worldnews = []

    json_year_politics = []
    json_year_news = []
    json_year_worldnews = []

    interval = ''

    if request.method == 'GET':
                                       
        # Populate data arrays with JSON objects

        json_object_reddit(json_day_politics, "politics", "day", "default", cur)
        json_object_reddit(json_day_news, "news", "day", "default", cur)
        json_object_reddit(json_day_worldnews, "worldnews", "day", "default", cur)

        json_object_reddit(json_month_politics, "politics", "month", "default", cur)
        json_object_reddit(json_month_news, "news", "month", "default", cur)
        json_object_reddit(json_month_worldnews, "worldnews", "month", "default", cur)

        json_object_reddit(json_year_politics, "politics", "year", "default", cur)
        json_object_reddit(json_year_news, "news", "year", "default", cur)
        json_object_reddit(json_year_worldnews, "worldnews", "year", "default", cur)

    if request.method == 'POST':

        # Form custom interval object.

        interval = request.form['year'] + '-' + request.form['month'] + '-' + request.form['day']

        # Populate data arrays with JSON objects

        json_object_reddit(json_custom_politics, "politics", interval, "custom", cur)
        json_object_reddit(json_custom_news, "news", interval, "custom", cur)
        json_object_reddit(json_custom_worldnews, "worldnews", interval, "custom", cur)

        json_object_reddit(json_day_politics, "politics", "day", "default", cur)
        json_object_reddit(json_day_news, "news", "day", "default", cur)
        json_object_reddit(json_day_worldnews, "worldnews", "day", "default", cur)

        json_object_reddit(json_month_politics, "politics", "month", "default", cur)
        json_object_reddit(json_month_news, "news", "month", "default", cur)
        json_object_reddit(json_month_worldnews, "worldnews", "month", "default", cur)

        json_object_reddit(json_year_politics, "politics", "year", "default", cur)
        json_object_reddit(json_year_news, "news", "year", "default", cur)
        json_object_reddit(json_year_worldnews, "worldnews", "year", "default", cur)

    close_connection(cur, conn)

    return render_template('/reddit/topwords.html',
                    interval=interval,
                    argument=argument, 
                    custom_politics=json.dumps(json_custom_politics), 
                    custom_news=json.dumps(json_custom_news), 
                    custom_worldnews = json.dumps(json_custom_worldnews),
                    day_politics=json.dumps(json_day_politics), 
                    day_news=json.dumps(json_day_news), 
                    day_worldnews = json.dumps(json_day_worldnews),
                    month_politics=json.dumps(json_month_politics), 
                    month_news=json.dumps(json_month_news), 
                    month_worldnews = json.dumps(json_month_worldnews),
                    year_politics=json.dumps(json_year_politics), 
                    year_news=json.dumps(json_year_news), 
                    year_worldnews = json.dumps(json_year_worldnews))


@app.route('/reddit/search', methods=['GET','POST']) 
def search():
    conn = connect_to_database()
    cur = conn.cursor()

    json_politics = []
    json_news = []
    json_worldnews = []
    json_thedonald = []

    if request.method == 'GET':
        
        words = ['coronavirus']
        index = len(words)
        word = words[index-1]

    if request.method == 'POST':

        word = request.form['word'].lower()

    json_object_search(json_politics, "politics", word,  cur)
    json_object_search(json_news, "news", word,  cur)
    json_object_search(json_worldnews, "worldnews", word,  cur)

    close_connection(cur, conn)

    return render_template('/reddit/search.html',   
                    word = word,                
                    politics=json.dumps(json_politics, default=str), 
                    news=json.dumps(json_news, default=str), 
                    worldnews = json.dumps(json_worldnews, default=str))


@app.route('/twitter/scalability')
def scalability():
    return render_template('twitter/scalability.html')

@app.route('/twitter/pdxdashboard', methods=['GET','POST'])
def pdxdashboard():
    conn = connect_to_database()
    cur = conn.cursor()

    json_events = []

    json_object_events(json_events, cur)

    dump = json.dumps(json_events, default=str)
    json_events = json.loads(dump)

    close_connection(cur, conn)

    return render_template('twitter/pdxdashboard.html',
                            events=json_events)


@app.route('/superbowl/2019')
def superbowl2019():
    conn = connect_to_database()
    cur = conn.cursor()

    json_aggregate_patriots     = []
    json_shit_patriots          = []
    json_fuck_patriots          = []
    json_maroon_5_patriots      = []
    json_goff_patriots          = []
    json_punt_patriots          = []
    json_touchdown_patriots     = []
    json_brady_patriots         = []

    json_aggregate_rams         = []
    json_shit_rams              = []
    json_fuck_rams              = []
    json_maroon_5_rams          = []
    json_goff_rams              = []    
    json_punt_rams              = []
    json_touchdown_rams         = []
    json_brady_rams             = []



    json_object_time_series(json_aggregate_patriots, "patriots_aggregate", cur)
    json_object_time_series(json_shit_patriots, "patriots_shit", cur)
    json_object_time_series(json_fuck_patriots, "patriots_fuck", cur)
    json_object_time_series(json_maroon_5_patriots, "patriots_maroon_5", cur)
    json_object_time_series(json_goff_patriots, "patriots_goff", cur)
    json_object_time_series(json_touchdown_patriots, "patriots_touchdown", cur)
    json_object_time_series(json_punt_patriots, "patriots_punt", cur)
    json_object_time_series(json_brady_patriots, "patriots_brady", cur)

    json_object_time_series(json_aggregate_rams, "rams_aggregate", cur)
    json_object_time_series(json_shit_rams, "rams_shit", cur)
    json_object_time_series(json_fuck_rams, "rams_fuck", cur)
    json_object_time_series(json_maroon_5_rams, "rams_maroon_5", cur)
    json_object_time_series(json_goff_rams, "rams_goff", cur)
    json_object_time_series(json_touchdown_rams, "rams_touchdown", cur)
    json_object_time_series(json_punt_rams, "rams_punt", cur)
    json_object_time_series(json_brady_rams, "rams_brady", cur)

    close_connection(cur, conn)

    return render_template('twitter/2019.html',
                                json_aggregate_patriots=json.dumps(json_aggregate_patriots, default=str),
                                json_shit_patriots=json.dumps(json_shit_patriots, default=str),
                                json_fuck_patriots=json.dumps(json_fuck_patriots, default=str),
                                json_goff_patriots=json.dumps(json_goff_patriots, default=str),
                                json_punt_patriots=json.dumps(json_punt_patriots, default=str),
                                json_touchdown_patriots=json.dumps(json_touchdown_patriots, default=str),
                                json_brady_patriots=json.dumps(json_brady_patriots, default=str),
                                json_maroon_5_patriots=json.dumps(json_maroon_5_patriots, default=str),
                                json_aggregate_rams=json.dumps(json_aggregate_rams, default=str),
                                json_shit_rams=json.dumps(json_shit_rams, default=str),
                                json_fuck_rams=json.dumps(json_fuck_rams, default=str),
                                json_goff_rams=json.dumps(json_goff_rams, default=str),
                                json_punt_rams=json.dumps(json_punt_rams, default=str),
                                json_touchdown_rams=json.dumps(json_touchdown_rams, default=str),
                                json_brady_rams=json.dumps(json_brady_rams, default=str),
                                json_maroon_5_rams=json.dumps(json_maroon_5_rams, default=str))



@app.route('/superbowl/2017')
def superbowl2017():
    return render_template('twitter/2017.html')


@app.route('/erowid/sentiment')
def sentiment():
    conn = connect_to_database()
    cur = conn.cursor()

    #Instantiate data arrays.

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
    

    # Populate data arrays with JSON objects

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

    # Instantiate data arrays.

    genders = []
    genders_cannabis = []
    genders_amphetamines = []
    genders_lsd = []
    genders_mushrooms = []
    genders_mdma = []
    genders_ketamine = []
    genders_cocaine = []

    years = []
    years_cannabis = []
    years_amphetamines = []
    years_lsd = []
    years_mushrooms = []
    years_mdma = []
    years_ketamine = []
    years_cocaine = []

    views = []
    views_cannabis = []
    views_amphetamines = []
    views_lsd = []
    views_mushrooms = []
    views_mdma = []
    views_ketamine = []
    views_cocaine = []

    # Populate data arrays with JSON objects

    json_object_gender(genders, None, cur)
    json_object_gender(genders_cannabis, "cannabis", cur)
    json_object_gender(genders_amphetamines,"amphetamines",cur)
    json_object_gender(genders_lsd,"lsd",cur)
    json_object_gender(genders_mushrooms,"mushrooms",cur)
    json_object_gender(genders_mdma,"mdma",cur)
    json_object_gender(genders_ketamine,"ketamine",cur)
    json_object_gender(genders_cocaine,"cocaine",cur)

    json_object_year(years, None, cur)
    json_object_year(years_cannabis, "cannabis", cur)
    json_object_year(years_amphetamines, "amphetamines", cur)
    json_object_year(years_lsd, "lsd", cur)
    json_object_year(years_mushrooms, "mushrooms", cur)
    json_object_year(years_mdma, "mdma", cur)
    json_object_year(years_ketamine, "ketamine", cur)
    json_object_year(years_cocaine, "cocaine", cur)

    json_object_view(views, None, cur)
    json_object_view(views_cannabis, "cannabis", cur)
    json_object_view(views_amphetamines, "amphetamines", cur)
    json_object_view(views_lsd, "lsd", cur)
    json_object_view(views_mushrooms, "mushrooms", cur)
    json_object_view(views_mdma, "mdma", cur)
    json_object_view(views_ketamine, "ketamine", cur)
    json_object_view(views_cocaine, "cocaine", cur)

    close_connection(cur, conn)

    return render_template('erowid/users.html', 
                    genders=json.dumps(genders),
                    genders_cannabis=json.dumps(genders_cannabis), 
                    genders_amphetamines=json.dumps(genders_amphetamines),
                    genders_lsd=json.dumps(genders_lsd),
                    genders_mushrooms=json.dumps(genders_mushrooms),
                    genders_mdma=json.dumps(genders_mdma),
                    genders_ketamine=json.dumps(genders_ketamine),
                    genders_cocaine=json.dumps(genders_cocaine),
                    years=json.dumps(years),
                    years_cannabis=json.dumps(years_cannabis), 
                    years_amphetamines=json.dumps(years_amphetamines),
                    years_lsd=json.dumps(years_lsd),
                    years_mushrooms=json.dumps(years_mushrooms),
                    years_mdma=json.dumps(years_mdma),
                    years_ketamine=json.dumps(years_ketamine),
                    years_cocaine=json.dumps(years_cocaine),
                    views=json.dumps(views),
                    views_cannabis=json.dumps(views_cannabis), 
                    views_amphetamines=json.dumps(views_amphetamines),
                    views_lsd=json.dumps(views_lsd),
                    views_mushrooms=json.dumps(views_mushrooms),
                    views_mdma=json.dumps(views_mdma),
                    views_ketamine=json.dumps(views_ketamine),
                    views_cocaine=json.dumps(views_cocaine))
                    


