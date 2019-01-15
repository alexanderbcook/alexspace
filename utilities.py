import psycopg2
import datetime
import itertools

# General utilites

def connect_to_database():
    return psycopg2.connect("dbname=postgres")

def close_connection(cur, conn):
    cur.close()
    conn.close()
    return

# Reddit top words page

def json_object_reddit(obj, subreddit, interval, now, cur):
    if now != None:
	query = cur.execute("SELECT word, sum, total FROM " + interval + "_" + subreddit + ";") 
    else:
        query = cur.execute("SELECT word, SUM(count) as sum, (SELECT total FROM count_"+subreddit+" WHERE DATE_TRUNC('day',day) = '"+ interval +"') as total FROM reddit."+subreddit+" WHERE DATE_TRUNC('day',day) = '"+interval+"' GROUP BY word ORDER BY sum DESC limit 10;")
    
    results = cur.fetchall()
    for result in results:
        obj.append(
            {
                "word":result[0],
                "count":result[1],
                "total":result[2]
            }
        )
    return obj

# Reddit search page

def json_object_search(obj, subreddit, word, cur):
    query = cur.execute("SELECT day::date, SUM(count) as count FROM reddit."+subreddit+" WHERE word = '"+word+"' GROUP BY day::date UNION ALL SELECT date_trunc('day', dd):: date,0 FROM generate_series( '2018-03-24'::timestamp, '"+datetime.datetime.now().strftime('%Y-%m-%d')+"'::timestamp, '1 day'::interval) dd WHERE (SELECT date_trunc('day', dd):: date) NOT IN (SELECT day::date FROM reddit."+subreddit+" WHERE word = '"+word+"' GROUP BY day::date) ORDER BY day")
    results = cur.fetchall()
    query = cur.execute("SELECT day::date, SUM(count) as total FROM reddit."+subreddit+" GROUP BY day::date UNION ALL SELECT date_trunc('day', dd):: date,0 FROM generate_series( '2018-03-24'::timestamp, '"+datetime.datetime.now().strftime('%Y-%m-%d')+"'::timestamp, '1 day'::interval) dd WHERE (SELECT date_trunc('day', dd):: date) NOT IN (SELECT day::date FROM reddit."+subreddit+" GROUP BY day::date) ORDER BY day")
    totals = cur.fetchall()

    i = 0
    while i < len(results):

        obj.append(
            {
                "date":results[i][0],
                "count": results[i][1],
                "total": totals[i][1]
            }
        )
        i += 1

    return obj


# Erowid sentiment page

def json_object_sentiment(substance, obj, gender,cur):
    if gender != None:
        query = cur.execute("SELECT avg(sentiment) FROM erowid."+substance+" WHERE gender="+gender)
    else:
        query = cur.execute("SELECT avg(sentiment) FROM erowid."+substance)

    result = cur.fetchone()
    obj.append({
            "substance": substance,
            "sentiment": result
               })
    return obj

def json_object_category(substance,obj,cur):
    query = cur.execute("SELECT avg(sentiment), category FROM erowid."+substance+" WHERE category NOT IN ('Not Applicable','Various', 'General', 'Music Discussion', 'Personal Preparation', 'Poetry', 'Preparation / Recipes', 'Cultivation / Synthasis', 'Guides / Sitters','HPPD / Lasting Visuals','Unknown Context') GROUP BY category ORDER by avg(sentiment) desc;")
    categories = cur.fetchall()
    for category in categories:
        obj.append({
            "category":category[1],
            "sentiment":category[0]
                })
    return obj

# Erowid user page

def json_object_gender(obj, substance, cur):
    if substance == None:
        query = cur.execute("SELECT DISTINCT gender, count(gender) FROM erowid.main GROUP BY gender") 

    else:
        query = cur.execute("SELECT DISTINCT gender, count(gender) FROM erowid."+substance+" GROUP BY gender;")

    results = cur.fetchall()

    if substance == None:
        query = cur.execute("SELECT count(id) FROM erowid.main;") 

    else:
        query = cur.execute("SELECT count(id) FROM erowid."+substance+";")

    total = cur.fetchone()

    for result in results:
        obj.append({
            "gender": result[0],
            "count": result[1],
            "total": total
                    })
    return obj


def json_object_year(obj, substance, cur):
    if substance == None:
        query = cur.execute("SELECT EXTRACT(YEAR from date::DATE) AS extracted_year, count(EXTRACT(YEAR from date::DATE)) FROM erowid.main WHERE EXTRACT(YEAR from date::DATE) NOT IN ('1969', '2017') GROUP BY extracted_year ORDER BY extracted_year;")
    else:
        query = cur.execute("SELECT EXTRACT(YEAR from date::DATE) AS extracted_year, count(EXTRACT(YEAR from date::DATE)) FROM erowid."+substance+" WHERE EXTRACT(YEAR from date::DATE) NOT IN ('1969', '2017') GROUP BY extracted_year ORDER BY extracted_year;")
    results = cur.fetchall()
    for result in results:
        obj.append({
               "year":int(result[0]),
                "count":result[1]
                    })
    return obj

def json_object_view(obj, substance, cur):
    if substance == None:
        query = cur.execute("SELECT EXTRACT(YEAR from date::DATE) AS extracted_year, sum(REPLACE(views,',','')::INT) FROM erowid.main WHERE EXTRACT(YEAR from date::DATE) NOT IN ('1969', '2017') GROUP BY extracted_year ORDER BY extracted_year;")
    else:
        query = cur.execute("SELECT EXTRACT(YEAR from date::DATE) AS extracted_year, sum(REPLACE(views,',','')::INT) FROM erowid."+substance+" WHERE EXTRACT(YEAR from date::DATE) NOT IN ('1969', '2017') GROUP BY extracted_year ORDER BY extracted_year;")
    results = cur.fetchall()
    for result in results:
        obj.append({
                   "year":int(result[0]),
                    "views":result[1]
                    })
    return obj
