import psycopg2


def connect_to_database():
    return psycopg2.connect("dbname=postgres")

def close_connection(cur, conn):
    cur.close()
    conn.close()
    return