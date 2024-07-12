import psycopg
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi import FastAPI, HTTPException

from service.FaceRecognitionHelper import FaceRecognitionHelper

class DataBaseHelper:
    def __init__(self):
        load_dotenv()
        
        if not  os.path.isdir('resources/images'):
            os.makedirs('resources/images')
        
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
            
    def add_inventory_change_events(self, user_id, events_dict):
        tools_dict = self.get_tools_dictionary()
        with self.conn.cursor() as cur:
            for tool, count in events_dict['brought'].items():
                if tool in tools_dict:
                    for _ in range(count):
                        cur.execute("""
                                    INSERT INTO tools_journal (datetime, tool_id, user_id, status) 
                                    VALUES (%s, %s, %s, %s) RETURNING id;
                            """, (datetime.now().isoformat(), tools_dict[tool], user_id, 'взял'))

            for tool, count in events_dict['took_away'].items():
                if tool in tools_dict:
                    for _ in range(count):
                        cur.execute("""
                                    INSERT INTO tools_journal (datetime, tool_id, user_id, status) 
                                    VALUES (%s, %s, %s, %s) RETURNING id;
                            """, (datetime.now().isoformat(), tools_dict[tool], user_id, 'вернул'))

        self.conn.commit()

    def find_user_id_by_embedding(self, embedding):
        with self.conn.cursor() as cur:
            embedding_str = ','.join(map(str, embedding[0]))
            embedding_array = "{" + embedding_str + "}"
            cur.execute("""
                            SELECT 
                                user_id,
                                embedding,
                                euclidean_distance(embedding, %s ::numeric[]) AS distance
                            FROM 
                                users_images
                            ORDER BY 
                                distance
                            LIMIT 1
                        """, (embedding_array,))
            user_id, _, dist = cur.fetchone()

            return user_id if dist < 0.6 else 1 # if dist less than 0.6 than user_id else id = 1 (unknown)

    def get_users_dict(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM users")

            dict = {}

            for row in cur:
                id, name, surname, patronymic = row
                dict[id] = f'{name} {surname} {patronymic}'

            return dict

    def get_journal(self):
        result = []
        users_dict = self.get_users_dict()
        tools_dict = self.get_tools_dictionary()
        tools_dict = {id: tool for tool, id in tools_dict.items()}
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM tools_journal")

            for row in cur:
                dict = {}
                _, date_time, tool_id, user_id, status = row
                dict['datetime'] = date_time
                dict['tool'] = tools_dict[tool_id]
                dict['user'] = users_dict[user_id]
                dict['status'] = status
                result.append(dict)

            return result