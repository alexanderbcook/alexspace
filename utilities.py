import psycopg2

# General utilites

def connect_to_database():
    return psycopg2.connect("dbname=postgres")

def close_connection(cur, conn):
    cur.close()
    conn.close()
    return

# Reddit page

def json_object_reddit(obj, subreddit, interval, now, cur):
    query = cur.execute("SELECT word, SUM(count) FROM reddit."+subreddit+" WHERE day < %s AND day >= %s GROUP BY word ORDER BY SUM(count) DESC limit 10;", (now,interval))
    results = cur.fetchall()
    for result in results:
        obj.append(
            {
                "word":result[0],
                "count":result[1],
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
    query = cur.execute("SELECT avg(sentiment), category FROM erowid."+substance+" WHERE category NOT IN ('Not Applicable','Preparation / Recipes','Unknown Context','Poetry','Therapeutic Intent or Outcome', 'Performance Enhancement', 'Personal Preparation','Various','Second Hand Report', 'Music Discussion', 'What Was in That?', 'Combinations','HPPD / Lasting Visuals','Entities / Beings', 'Guides / Sitters', 'Loss of Magic', 'General', 'Health Beneftis') GROUP BY category ORDER by avg(sentiment) desc;")
    categories = cur.fetchall()
    for category in categories:
        obj.append({
            "category":category[1],
            "sentiment":category[0]
                })
    return obj

# Erowid user page

def json_object_gender(obj,cur):
    query = cur.execute("SELECT DISTINCT gender, count(gender) FROM erowid.main GROUP BY gender;") 
    results = cur.fetchall()
    for result in results:
        obj.append({
        "gender": result[0],
        "count": result[1]
                    })
    return obj


def json_object_year(obj, cur):
    query = cur.execute("SELECT EXTRACT(YEAR from date::DATE) AS extracted_year, count(EXTRACT(YEAR from date::DATE)) FROM erowid.main WHERE EXTRACT(YEAR from date::DATE) NOT IN ('1969', '2017') GROUP BY extracted_year ORDER BY extracted_year;")
    results = cur.fetchall()
    for result in results:
        obj.append({
                   "year":int(result[0]),
                    "count":result[1]
                    })
    return obj

def json_object_views(obj,cur):
    query = cur.execute("SELECT EXTRACT(YEAR from date::DATE) AS extracted_year, sum(REPLACE(views,',','')::INT) FROM erowid.main WHERE EXTRACT(YEAR from date::DATE) NOT IN ('1969', '2017') GROUP BY extracted_year ORDER BY extracted_year;")
    results = cur.fetchall()
    for result in results:
        obj.append({
                   "year":int(result[0]),
                    "views":result[1]
                    })
    return obj
