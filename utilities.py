import psycopg2

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
        query = cur.execute("SELECT word, SUM(count) FROM reddit."+subreddit+" WHERE day < %s AND day >= %s GROUP BY word ORDER BY SUM(count) DESC limit 10;", (now,interval))
    else:
        query = cur.execute("SELECT word, SUM(count) FROM reddit."+subreddit+" WHERE day::varchar LIKE '%"+ interval +"%' GROUP BY word ORDER BY SUM(count) DESC limit 10;")
    
    results = cur.fetchall()
    for result in results:
        obj.append(
            {
                "word":result[0],
                "count":result[1],
            }
        )
    return obj

# Reddit search page

def json_object_search(obj, subreddit, word, cur):
    query = cur.execute("SELECT day::date, SUM(count) FROM reddit."+subreddit+" WHERE word = '"+word+"' GROUP BY day::date;")

    results = cur.fetchall()
    for result in results:
        obj.append(
            {
                "date":result[0],
                "count":result[1]
            }
        )
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
