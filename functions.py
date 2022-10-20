import os, time

import aiohttp
import asyncio

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import uuid

import constants

# technically you should be able to scale this pretty well
# even with the free version because you could theoretically
# host multiple copies of the same model and get around the 
# 2 imgs per second bottleneck. Maybe that's why they don't 
# allow you to host custom models? 


# making async requests call
async def fetch(session, url, data,i):
    print("Request #" + str(i) + " Sent")
    async with session.post(url,headers=constants.HEADERS, data=data) as response:
        resp = await response.text()
        print("Request #"+ str(i) + " Complete")
        return resp

# Setting up for batch requests, F0 resources can only call 2 imgs a time
async def fetch_all(byteImages):
    conn = aiohttp.TCPConnector(limit=len(byteImages)+1)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        i = 0
        for image in byteImages:
            i = i+1
            if i%2 == 0:
                time.sleep(3)
            tasks.append( fetch(session, constants.ENDPOINT, image, i) )

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

# this should use get_files to get the files and then 
# bytes(img) for img in folder
def images2bytes(path:str) -> list : 
    ''' Get all the images in a directory and return their byte versions.
    Params:
        path (str): path of the root folder
    Returns:
        list: list of byte images
    Author:
        Natasha
    Date:
        2022/10/05
    '''
    img_bytes = get_files(path)
    for idx, img in enumerate(img_bytes):
        with open(os.path.join(img), "rb") as img:
            b = bytearray(img.read())
            img_bytes[idx] = b
    return img_bytes

def get_files(path:str) -> list : 
    ''' Get all the images in a directory and return full paths.
    Params:
        path (str): path of the root folder
    Returns:
        list: list of full path image files
    Author:
        Natasha
    Date:
        2022/10/05
    '''
    files_list = []
    for roots, _, files in os.walk(path):
        imgs = [os.path.normpath(os.path.join(roots, file))
                for file in files 
                if file.endswith((".jpeg", ".jpg", ".png"))]

        files_list.extend(imgs)
    return files_list


def xy2yolo(size, box):
    ''' Convert the NORMALIZED [x1,y1,x2,y2] bounding box coordinates
        to the YOLO format [xc, yc, h, w].
    Params:
        size: list or tuple (h, w)
        box:  list or tuple (x1, y1, x2, y2)

    '''
    xc = (box[0] + box[2])/2
    yc = (box[1] + box[3])/2
    h = abs(box[1]-box[3])
    w = abs(box[0]-box[2])
    return [xc,yc,h,w]


def authenticate():
    credentials = ApiKeyCredentials(in_headers={"Training-key": constants.TRAINING.KEY})
    trainer = CustomVisionTrainingClient(constants.TRAINING.ENDPOINT, credentials)
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": constants.PREDICTION.KEY})
    predictor = CustomVisionPredictionClient(constants.PREDICTION.ENDPOINT, prediction_credentials)
    return trainer, predictor

if __name__ == "__main__":
    path = r"D:\_Innospire\data\vehicle_recognition_test"
    