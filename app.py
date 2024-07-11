from service.DataBaseHelper import DataBaseHelper
from service.utils import save_file

from fastapi import FastAPI, Request, UploadFile, File, HTTPException

import uvicorn

db_helper = DataBaseHelper()

app = FastAPI()

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
    
    print(tools_image_path)
    print(face_image_path)
    
if __name__ == '__main__':
    uvicorn.run(app, port=3000)