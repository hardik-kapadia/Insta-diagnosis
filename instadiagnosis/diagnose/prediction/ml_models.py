
from tensorflow import keras
import cv2


import os
from skimage import morphology
import numpy as np
from scipy import ndimage

def remove_noise(img):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
    
    segmentation = morphology.dilation(image, np.ones((1, 1)))
    labels, label_nb = ndimage.label(segmentation)
    
    label_count = np.bincount(labels.ravel().astype(np.int))
    label_count[0] = 0

    mask = labels == label_count.argmax()
 
    mask = morphology.dilation(mask, np.ones((1, 1)))
    mask = ndimage.morphology.binary_fill_holes(mask)
    mask = morphology.dilation(mask, np.ones((3, 3)))
    masked_image = mask * image
    image = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2BGR)
    return image

def predict_covid_noncovid(img_path) -> str:
    
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models/model_covid_noncovid.h5')
    model = keras.models.load_model(path)
    
    img = cv2.imdecode(np.frombuffer(img_path.read(), np.uint8), 1)
    img = cv2.resize(img,(256,256))
    img = remove_noise(img)
    img=np.array([img])
    pred = model.predict([img])
    if pred>0.5:
        x=pred[0]
        return "Non-covid with probability : {:.4f} %".format(x[0]*100) 
    else:
        x=pred[0]
        return "Covid with probability : {:.4f} %".format(100-x[0]*100) 

def predict_brain_tumor(img_path):
    
    img = cv2.imdecode(np.frombuffer(img_path.read(), np.uint8), 1)
    # img = cv2.imread(image_path)
    img1 = cv2.resize(img,(150,150))
    img1 = remove_noise(img1)
    
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models/brain_tumor_model.h5')
    model = keras.models.load_model(path)
    
    pred = np.array([img1])
    pred = model.predict(pred)
    pred1 = np.argmax(pred,axis=1)
    labels = ['glioma_tumor','no_tumor','meningioma_tumor','pituitary_tumor']
    return "{} with probability : {:.4f}%".format(labels[pred1[0]],pred[0,pred1[0]]*100)

def predict_knee_arthritis(img_path):
    
    
    img = cv2.imdecode(np.frombuffer(img_path.read(), np.uint8), 1)
    
    # img = cv2.imread(image_path)
    img1 = cv2.resize(img,(150,150))
    # model = keras.models.load_model(model_path)
    
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models/knee_arthritis_model.h5')
    
    model = keras.models.load_model(path)
    pred = np.array([img1])
    pred = model.predict(pred)
    pred1 = np.argmax(pred,axis=1)
    labels = ['0','1','2','3','4']
    return f"Grade {labels[pred1[0]]} arthritis with probability : {pred[0,pred1[0]]*100}%"
