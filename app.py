from service.DataBaseHelper import DataBaseHelper
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

if __name__ == '__main__':
    uvicorn.run(app, port=3000)