import time
import psycopg2

while True:
    try:
        conn = psycopg2.connect(
            dbname="nevup",
            user="postgres",
            password="postgres",
            host="db",
            port="5432"
        )
        conn.close()
        break
    except:
        print("Waiting for DB...")
        time.sleep(2)