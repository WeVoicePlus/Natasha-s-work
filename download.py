import os
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
import json
import urllib.request as request

import functions
 
###################################################################
# Replace with a valid key of the TARGET Custom Vision
###################################################################
ENDPOINT = "https://southeastasia.api.cognitive.microsoft.com/"
training_key = "put your training key here"
projectid = "put your project id here"
storeImageDirectry = "put your save folder here"
###################################################################
###################################################################
 
'''
Image Classification JSONs look like
    {"fileName": "1.jpg","tags":["Negative"]}
 
Object Detection JSONs look like:
    {"fileName": "1.jpg", 
     "regions": [
        {"tag_name": "Closed", 
         "left": 0.00104166672, 
         "top": 0.00208333344, 
         "width": 0.288541675, 
         "height": 0.5104167}
     ]
    }
'''
 
trainer, _ = functions.authenticate()
currentFileNumber = 0
allTags = []
 
while currentFileNumber < trainer.get_tagged_image_count(project_id=projectid):
    for image in trainer.get_tagged_images(project_id=projectid, take=1, skip=currentFileNumber):
        currentFileNumber = currentFileNumber + 1
        configJSON = json.loads("{}")
        configJSON["fileName"] = str(currentFileNumber) + ".jpg"
        if image.regions != None:               # for Object Detection
            returnedRegions = []
            for region in image.regions:
                if region.tag_name not in allTags:
                    allTags.append(region.tag_name)
                returnedRegion = {}
                returnedRegion["tag_name"] = region.tag_name
                returnedRegion["left"] = region.left
                returnedRegion["top"] = region.top
                returnedRegion["width"] = region.width
                returnedRegion["height"] = region.height
                returnedRegions.append(returnedRegion)
            configJSON["regions"] = returnedRegions
        else:                                   # for Image Classification
            tags = []
            for tag in image.tags:
                tags.append(tag.tag_name)
                if tag.tag_name not in allTags:
                    allTags.append(tag.tag_name)
            configJSON["tags"] = tags
        
        if not os.path.exists(storeImageDirectry):
            os.mkdir(storeImageDirectry)
        myfile = os.open(os.path.join(storeImageDirectry, str(currentFileNumber) + ".json"), os.O_TRUNC|os.O_RDWR|os.O_CREAT)
        os.write(myfile, str.encode(json.dumps(configJSON)))
        os.close(myfile)
        request.urlretrieve(url=image.original_image_uri, filename=os.path.join(storeImageDirectry, str(currentFileNumber) + ".jpg"))
 
myfile = os.open(os.path.join(storeImageDirectry, "allTags.json"), os.O_TRUNC|os.O_RDWR|os.O_CREAT)
os.write(myfile, str.encode(json.dumps(allTags)))
os.close(myfile)