from .. import schemas, models, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from .. database import get_db
from werkzeug.utils import secure_filename
import os
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras.models import load_model # untuk menggunakan fungsi load_model()
from keras.preprocessing.image import load_img, img_to_array # untuk menggunakan fungsi load_img()
from PIL import Image
from io import BytesIO



upload_folder = './backend/images'
file_path = ''
image_size = (256, 256)
model = load_model('./backend/model/pld_model.h5')

router = APIRouter(
    prefix="/diagnose"
)

def predict(image_path):
    Class = ''

    img = load_img(image_path, target_size=image_size)
    x = img_to_array(img)
    x /= 255 # normalize the pixel values of the image to be between 0 and 1
    x = np.expand_dims(x, axis=0) # add an extra dimension to match the input shape of the model
    images = np.vstack([x]) # stack the single image array into a batch of images

    prediction = model.predict(images, batch_size=10)
    predicted_class = np.argmax(prediction)

    if predicted_class == 0:
        Class = 'Early Blight'
    elif predicted_class == 1:
        Class = 'Healthy'
    else:
        Class = 'Late Blight'

    os.remove(image_path)
    return Class

@router.post('/', status_code=status.HTTP_200_OK)
def diagnose(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user),
    file: UploadFile = File(...) # file: is the key
): 
    if not file:
        raise HTTPException(status_code=400, detail="File not found!!!")
    
    try:
        content = Image.open(BytesIO(file.file.read())) # In this way the uploaded file become not in binary
        file_name = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, file_name)
        
        content.save(file_path)
        
        prediction = predict(file_path)
        return JSONResponse(content={"prediction": prediction})
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))