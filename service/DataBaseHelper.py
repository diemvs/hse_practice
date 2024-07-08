import psycopg
import os
from dotenv import load_dotenv 

class DataBaseHelper:
    def __init__(self):
        load_dotenv()
        
        conninfo = " ".join([
            f'dbname={os.getenv("DATABASE_NAME")}',
            f'user={os.getenv("DATABASE_USER")}',
            f'password={os.getenv("DATABASE_PASSWORD")}',
            f'host={os.getenv("DATABASE_HOST")}',
            f'port={os.getenv("DATABASE_PORT")}',
        ])

        
        self.conn = psycopg.connect(conninfo=conninfo)
            
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (name, surname, patronymic) 
                VALUES ('Test', 'Testov', 'Testovich');
            """)
            
            self.conn.commit()
            
            self.conn.close()
        