import psycopg2


def connect_to_database():
    return psycopg2.connect("dbname=postgres")

def close_connection(cur, conn):
    cur.close()
    conn.close()
    return

def json_object_reddit(subreddit, query):
    for word in query:
        subreddit.append(
            {
                "word":word[0],
                "count":word[1],
            }
        )
    return subreddit

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