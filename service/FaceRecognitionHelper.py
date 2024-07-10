import face_recognition

class FaceRecognitionHelper:
    def __init__(self):
        pass
    
    def get_image_embeddings(self, path: str):
        image = face_recognition.load_image_file(path)
        return face_recognition.face_encodings(image)