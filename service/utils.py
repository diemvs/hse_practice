from fastapi import UploadFile

async def save_file(uploaded_file: UploadFile) -> str:
    file = await uploaded_file.read()
    
    path = f'resources/images/{uploaded_file.filename}'
    
    with open(path, "wb+") as file_object:
        file_object.write(file)
        
    return path