import psycopg
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from service.FaceRecognitionHelper import FaceRecognitionHelper

class DataBaseHelper:
    def __init__(self):
        load_dotenv()
        
        self.face_recon_helper = FaceRecognitionHelper()
        
        conninfo = " ".join([
            f'dbname={os.getenv("DATABASE_NAME")}',
            f'user={os.getenv("DATABASE_USER")}',
            f'password={os.getenv("DATABASE_PASSWORD")}',
            f'host={os.getenv("DATABASE_HOST")}',
            f'port={os.getenv("DATABASE_PORT")}',
        ])

        
        self.conn = psycopg.connect(conninfo=conninfo)
            
    def add_user(self, surname: str, name: str, patronymic: str):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (surname, name, patronymic) 
                VALUES ('{}', '{}', '{}') RETURNING id;
            """.format(surname, name, patronymic))
            
            res = cur.fetchone()
            
            self.conn.commit()
            
            return res[0]
        
    def add_user_image(self, user_id: int, file: bytes, filename: str):
        path = f'resources/images/{filename}'
        
        with open(path, "wb+") as file_object:
            file_object.write(file)
        
        with self.conn.cursor() as cur:
            
            cur.execute("""
                INSERT INTO files (name) 
                VALUES ('{}') RETURNING id;
            """.format(path))
            
            file_id = cur.fetchone()[0]
            
            embeddings = self.face_recon_helper.get_image_embeddings(path)

            if len(embeddings) == 0:
                raise HTTPException(status_code=400, detail='embedding is empty')
            
            embedding = embeddings[0].tolist()
            
            cur.execute("""
                INSERT INTO users_images (file_id, user_id, embedding) 
                VALUES (%s, %s, %s) RETURNING id;
            """, (file_id, user_id, embedding))
            
            self.conn.commit()
            
            return file_id
        
    def get_tools_dictionary(self): 
        with self.conn.cursor() as cur:
            
            cur.execute("SELECT * FROM tools")
            
            dict = {}
            
            for row in cur:
                id, name = row
                dict[name] = id
                
            return dict
            
            