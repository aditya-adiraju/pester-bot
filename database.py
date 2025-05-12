import sqlite3
from logging import *

CONNECTION_STRING = './data/pester.db'


def setup():
    cx = sqlite3.connect(CONNECTION_STRING)
    cur = cx.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id TEXT PRIMARY KEY, 
                    next_timestamp TEXT NOT NULL, 
                    expired BOOLEAN 
                )
                """)   

    cur.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    option TEXT PRIMARY KEY, 
                    value TEXT NOT NULL
                )
                """)   

    cur.execute("INSERT INTO config (option, value) VALUES('previous_run', current_timestamp)")
    cx.commit()
    debug(f"DB setup successfully!")
    cx.close()

def update_last_run():
    cx = sqlite3.connect(CONNECTION_STRING)
    cur = cx.cursor()
    cur.execute("UPDATE config SET value = current_timestamp WHERE option='previous_run'")
    cx.commit()
    debug("Updated last run time on db.")
    cx.close()

def get_last_run():
    cx = sqlite3.connect(CONNECTION_STRING)
    cur = cx.cursor()
    res = cur.execute("SELECT value FROM config WHERE option='previous_run'").fetchone()
    res = res[0]
    cx.close()
    return res
    

def expire_message(message_id):
    cx = sqlite3.connect(CONNECTION_STRING)
    cur = cx.cursor()
    cur.execute("UPDATE messages SET expired = 1 WHERE message_id=?", (message_id,))
    cx.commit()
    debug("Updated last run time on db.")
    cx.close()

def get_unexpired_messages():
    cx = sqlite3.connect(CONNECTION_STRING)
    previous_run = get_last_run()
    cur = cx.cursor()
    res = cur.execute("""
                SELECT message_id FROM messages
                WHERE expired = 0 
                AND next_timestamp < ?
                """, (previous_run,))
    results = res.fetchal()
    message_ids = [x[0] for x in results]
    cx.close()
    return message_ids