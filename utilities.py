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
        query = cur.execute(
            "SELECT avg(sentiment) FROM erowid."+substance+" WHERE gender="+gender)
    else:
        query = cur.execute("SELECT avg(sentiment) FROM erowid."+substance)

    result = cur.fetchone()
    obj.append({
        "substance": substance,
        "sentiment": result
    })

    return obj


def json_object_category(substance, obj, cur):
    query = cur.execute("SELECT avg(sentiment), category FROM erowid."+substance +
                        " WHERE category NOT IN ('Not Applicable','Various', 'General', 'Music Discussion', 'Personal Preparation', 'Poetry', 'Preparation / Recipes', 'Cultivation / Synthasis', 'Guides / Sitters','HPPD / Lasting Visuals','Unknown Context') GROUP BY category ORDER by avg(sentiment) desc;")

    categories = cur.fetchall()

    for category in categories:
        obj.append({
            "category": category[1],
            "sentiment": category[0]
        })

    return obj

# Erowid user page


def json_object_gender(obj, substance, cur):
    if substance == None:
        query = cur.execute(
            "SELECT DISTINCT gender, count(gender) FROM erowid.main GROUP BY gender")

    else:
        query = cur.execute(
            "SELECT DISTINCT gender, count(gender) FROM erowid."+substance+" GROUP BY gender;")

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
        query = cur.execute("SELECT EXTRACT(YEAR from date::DATE) AS extracted_year, count(EXTRACT(YEAR from date::DATE)) FROM erowid." +
                            substance+" WHERE EXTRACT(YEAR from date::DATE) NOT IN ('1969', '2017') GROUP BY extracted_year ORDER BY extracted_year;")

    results = cur.fetchall()

    for result in results:
        obj.append({
            "year": int(result[0]),
            "count": result[1]
        })
    return obj


def json_object_view(obj, substance, cur):
    if substance == None:
        query = cur.execute("SELECT EXTRACT(YEAR from date::DATE) AS extracted_year, sum(REPLACE(views,',','')::INT) FROM erowid.main WHERE EXTRACT(YEAR from date::DATE) NOT IN ('1969', '2017') GROUP BY extracted_year ORDER BY extracted_year;")
    else:
        query = cur.execute("SELECT EXTRACT(YEAR from date::DATE) AS extracted_year, sum(REPLACE(views,',','')::INT) FROM erowid." +
                            substance+" WHERE EXTRACT(YEAR from date::DATE) NOT IN ('1969', '2017') GROUP BY extracted_year ORDER BY extracted_year;")

    results = cur.fetchall()

    for result in results:
        obj.append({
                   "year": int(result[0]),
                   "views": result[1]
                   })
    return obj
