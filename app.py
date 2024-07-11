from service.DataBaseHelper import DataBaseHelper
from service.utils import save_file
from service.FaceRecognitionHelper import FaceRecognitionHelper

from fastapi import FastAPI, Request, UploadFile, File, HTTPException

import uvicorn

from ultralytics import YOLO
from collections import Counter

db_helper = DataBaseHelper()

app = FastAPI()

model = YOLO('./best.pt').to('cpu')
initial_state = None

face_recognition = FaceRecognitionHelper() # for test

def tools_after_visit(before, after):
    before_counter = Counter(before)
    after_counter = Counter(after)

    brought = {}
    took_away = {}

    # Find out which tools were brought
    for tool, count in after_counter.items():
        if count > before_counter[tool]:
            brought[tool] = count - before_counter[tool]

    # Find out which tools were taken away
    for tool, count in before_counter.items():
        if count > after_counter[tool]:
            took_away[tool] = count - after_counter[tool]

    return {
        "brought": dict(brought),
        "took_away": dict(took_away)
    }

@app.post("/add-user")
async def add_user(surname: str, name: str, patronymic: str):
    return db_helper.add_user(surname, name, patronymic)

@app.post("/user/{user_id}")
async def add_user_image(user_id: int, image: UploadFile = File(...)):
    file = await image.read()
    return db_helper.add_user_image(user_id, file, image.filename)

@app.get("/tools")
async def get_tools_dict():
    return db_helper.get_tools_dictionary()

@app.post("/detection")
async def detection(tools_image: UploadFile = File(...), face_image: UploadFile = File(...)):
    tools_image_path = await save_file(tools_image)
    face_image_path = await save_file(face_image)

    global initial_state
    detection_result = model.track(tools_image_path)
    actual_state = list(detection_result[0].names[k.item()] for k in detection_result[0].boxes.cls)

    if initial_state is None:
        initial_state = actual_state
    else:
        state_change = tools_after_visit(initial_state, actual_state)
        # тут должно быть вычисление пользователя по эмбеддингу
        print(state_change)
        db_helper.add_inventory_change_events(1, state_change)

@app.post('/get_user_id_by_photo')
async def get_user_id(face_image: UploadFile = File(...)):
    face_image_path = await save_file(face_image)
    emb = face_recognition.get_image_embeddings(face_image_path)
    return db_helper.find_user_id_by_embedding(emb)



if __name__ == '__main__':
    uvicorn.run(app, port=3000)