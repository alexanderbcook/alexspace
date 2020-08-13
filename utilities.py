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


def json_object_reddit(obj, subreddit, interval, requestType, cur):
    if requestType == "default":
        query = cur.execute(
            "SELECT word, sum, subreddit, total, interval  FROM " + interval + "_" + subreddit + ";")
    else:
        query = cur.execute("SELECT word, SUM(count) as sum, 'reddit."+subreddit+"', (SELECT total FROM count_"+subreddit+" WHERE day = '" +
                            interval + "') as total FROM reddit."+subreddit+" WHERE day = '"+interval+"' GROUP BY word ORDER BY sum DESC limit 10;")

    results = cur.fetchall()
    for result in results:
        obj.append(
            {
                "word": result[0],
                "count": result[1],
                "total": result[3],
            }
        )

    return obj

# Reddit search page


def json_object_search(obj, subreddit, word, cur):
    startDate = str(datetime.datetime.now() - datetime.timedelta(days=365))

    query = cur.execute("SELECT day, SUM(count) FROM (SELECT day, SUM(count) as count FROM reddit."+subreddit+" WHERE word ='"+word+"' GROUP BY day UNION SELECT generate_series(timestamp '" +
                        startDate+"', timestamp '"+datetime.datetime.now().strftime('%Y-%m-%d')+"', '1 day'):: DATE as day, 0) AS union_series GROUP BY union_series.day ORDER BY union_series.day LIMIT 365;")
    results = cur.fetchall()
    query = cur.execute("SELECT day, SUM(total) FROM (SELECT day, total FROM count_"+subreddit+" UNION SELECT generate_series(timestamp '"+startDate+"', timestamp '" +
                        datetime.datetime.now().strftime('%Y-%m-%d')+"', '1 day'):: DATE as day, 0) AS union_series GROUP BY union_series.day ORDER BY union_series.day LIMIT 365;")
    totals = cur.fetchall()

    i = 0
    while i < len(results):
        obj.append(
            {
                "date": results[i][0],
                "count": results[i][1],
                "total": totals[i][1]
            }
        )
        i += 1

    return obj

# Portland events page


def json_object_events(obj, cur):
    query = cur.execute(
        "SELECT id, createdate, address, incident_type FROM twitter.default ORDER BY createdate DESC LIMIT 15;")
    results = cur.fetchall()

    i = 0
    while i < len(results):

        obj.append(
            {
                "id": results[i][0],
                "createdate": results[i][1],
                "address": results[i][2],
                "incident": results[i][3]
            }
        )
        i += 1

    return obj

# 2019 Superbowl page


def json_object_time_series(obj, subject, cur):
    query = cur.execute(
        "SELECT interval::time, count,event FROM twitter."+subject+"  ORDER BY interval ASC;")
    results = cur.fetchall()

    i = 0
    while i < len(results):

        obj.append(
            {
                "date": results[i][0],
                "count": results[i][1],
                "event": results[i][2]
            }
        )
        i += 1
    return obj


# Erowid sentiment page

def json_object_sentiment(substance, obj, gender, cur):
    if gender != None:
        query = cur.execute("SELECT avg(sentiment_polarity) FROM erowid.experiences WHERE gender="+gender+" AND primary_substance='"+substance+"';")
    else:
        query = cur.execute("SELECT avg(sentiment_polarity) FROM erowid.experiences WHERE primary_substance='"+substance+"';")

    result = cur.fetchone()
    obj.append({
        "substance": substance,
        "sentiment": result
    })

    return obj


def json_object_category(substance, obj, cur):
    query = cur.execute("SELECT c.name, avg(e.sentiment_polarity) FROM erowid.experiences e INNER JOIN erowid.categories c ON e.primary_category_id = c.id WHERE e.primary_substance = '"+substance+"' GROUP BY c.name ORDER BY avg(e.sentiment_polarity) DESC;")

    categories = cur.fetchall()

    for category in categories:
        obj.append({
            "category": category[0],
            "sentiment": category[1]
        })

    return obj


def json_object_ratio(substance, obj, set, cur):
    if set == 'negative':
        query = cur.execute("SELECT count(id), primary_substance FROM erowid.experiences WHERE primary_substance = '"+substance+"' AND primary_category_id IN (6,7) GROUP BY primary_substance;")
        numerator = cur.fetchone()
        query = cur.execute("SELECT count(id), primary_substance FROM erowid.experiences WHERE primary_substance = '"+substance+"' GROUP BY primary_substance;")
        denominator = cur.fetchone()

    if set == 'positive':
        query = cur.execute("SELECT count(id), primary_substance FROM erowid.experiences WHERE primary_substance = '"+substance+"' AND primary_category_id IN (4,9) GROUP BY primary_substance;")
        numerator = cur.fetchone()
        query = cur.execute("SELECT count(id), primary_substance FROM erowid.experiences WHERE primary_substance = '"+substance+"' GROUP BY primary_substance;")
        denominator = cur.fetchone()

    if set == 'bodily harm':
        query = cur.execute("SELECT count(id), primary_substance FROM erowid.experiences WHERE primary_substance = '"+substance+"' AND primary_category_id IN (27,10) GROUP BY primary_substance;")
        numerator = cur.fetchone()
        query = cur.execute("SELECT count(id), primary_substance FROM erowid.experiences WHERE primary_substance = '"+substance+"' GROUP BY primary_substance;")
        denominator = cur.fetchone()

    obj.append(
        {
            "ratio": numerator[0]/denominator[0],
            "substance": substance
        }
    )

    return obj

# Erowid user page


def json_object_gender(obj, substance, cur):
    if substance == None:
        query = cur.execute(
            "SELECT DISTINCT gender, count(gender) FROM erowid.experiences GROUP BY gender;")

    else:
        query = cur.execute(
            "SELECT DISTINCT gender, count(gender) FROM erowid.experiences WHERE primary_substance='"+substance+"' GROUP BY gender;")

    results = cur.fetchall()

    if substance == None:
        query = cur.execute("SELECT count(id) FROM erowid.experiences;")

    else:
        query = cur.execute("SELECT count(id) FROM erowid.experiences WHERE primary_substance='"+substance+"';")

    total = cur.fetchone()

    for result in results:
        obj.append({
            "gender": result[0],
            "count": result[1],
            "total": total
        })
    return obj


def json_object_year_published(obj, substance, cur):
    if substance == None:
        query = cur.execute("SELECT EXTRACT(YEAR from published_date) AS year, count(id) FROM erowid.experiences WHERE EXTRACT(YEAR from published_date) NOT IN ('1995') GROUP BY EXTRACT(YEAR from published_date) ORDER BY EXTRACT(YEAR from published_date);")
    else:
        query = cur.execute("SELECT EXTRACT(YEAR from published_date) AS year, count(id) FROM erowid.experiences WHERE EXTRACT(YEAR from published_date) NOT IN ('1995') AND primary_substance = '"+substance+"' GROUP BY EXTRACT(YEAR from published_date) ORDER BY EXTRACT(YEAR from published_date);")
    results = cur.fetchall()

    for result in results:
        obj.append({
            "year": int(result[0]),
            "count": result[1]
        })
    return obj


def json_object_year_experienced(obj, substance, cur):
    if substance == None:
        query = cur.execute("SELECT experience_year, count(id) FROM erowid.experiences WHERE experience_year NOT IN ('1995') GROUP BY experience_year ORDER BY experience_year;")
    else:
        query = cur.execute("SELECT experience_year, count(id) FROM erowid.experiences WHERE experience_year NOT IN ('1995') AND primary_substance = '"+substance+"' GROUP BY experience_year ORDER BY experience_year;")
    results = cur.fetchall()

    for result in results:
        obj.append({
            "year": int(result[0]),
            "count": result[1]
        })
    return obj
