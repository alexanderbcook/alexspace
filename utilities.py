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