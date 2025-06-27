import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'stackstats.db'


def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create minute_stats table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS minute_stats
                   (
                       minute
                       TEXT
                       PRIMARY
                       KEY,
                       total_accepted_answers
                       INTEGER
                       DEFAULT
                       0,
                       accepted_answers_score_sum
                       INTEGER
                       DEFAULT
                       0,
                       answer_count
                       INTEGER
                       DEFAULT
                       0,
                       question_count
                       INTEGER
                       DEFAULT
                       0,
                       created_at
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   """)

    # Create top_answers table for storing top 10 answers per minute
    cursor.execute('''
CREATE TABLE IF NOT EXISTS top_answers
(
   id
   INTEGER
   PRIMARY
   KEY
   AUTOINCREMENT,
   minute
   TEXT,
   answer_id
   TEXT,
   score
   INTEGER,
   comment_count
   INTEGER,
   FOREIGN
   KEY
(
   minute
) REFERENCES minute_stats
(
   minute
)
   )
                   ''')

    conn.commit()
    conn.close()


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

if __name__ == '__main__':
    init_db()
