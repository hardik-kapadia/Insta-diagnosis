from tensorflow import keras
import cv2
import numpy as np

import os

def predict_covid_noncovid(img_path) -> str:
    
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models/model_covid_noncovid.h5')
    model = keras.models.load_model(path)
    
    img = cv2.imdecode(np.frombuffer(img_path.read(), np.uint8), 1)
    img = cv2.resize(img,(256,256))
    img=np.array([img])
    pred = model.predict([img])
    if pred>0.5:
        x=pred[0]
        return f"Non-covid with probability : {x[0]*100} %"
    else:
        x=pred[0]
        return f"Covid with probability : {100 - x[0]*100} %"

def predict_brain_tumor(img_path):
    
    img = cv2.imdecode(np.frombuffer(img_path.read(), np.uint8), 1)
    # img = cv2.imread(image_path)
    img1 = cv2.resize(img,(150,150))
    
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models/brain_tumor_model.h5')
    model = keras.models.load_model(path)
    
    pred = np.array([img1])
    pred = model.predict(pred)
    pred1 = np.argmax(pred,axis=1)
    labels = ['glioma_tumor','no_tumor','meningioma_tumor','pituitary_tumor']
    return f"{labels[pred1[0]]} with probability : {pred[0,pred1[0]]*100}%"