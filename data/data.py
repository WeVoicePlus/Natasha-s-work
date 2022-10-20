import http.client, urllib.request, urllib.parse, urllib.error, base64
from os.path import exists, split
import argparse, uuid
from tqdm import tqdm
from msrest.exceptions import HttpOperationError
import json

from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region

from vehicles import Vehicles
import functions


'''
    To make a new custom detection dataset:
    class Dataset:
        def __init__(self, **kwargs):
            # initialize data into a dict of dicts
            self.data = {"sample1": 
                            {"path":   "path/to/img.(jpeg, png, bmp)",
                             "bboxes": [{"top":  float(0-1),
                                         "left": float(0-1),
                                         "h":    float(0-1),
                                         "w":    float(0-1)} for box in sample]
                                    }
                        }
        
        def __len__(self):
            return len(self.data)

        def __getitem__(self, idx):
            return data[data.keys()[idx]]
'''

def parse_args():
    parser = argparse.ArgumentParser(description='Data args')
    parser.add_argument('--project_name', type=str, help='Name of project', 
                        default="test_1005")
    parser.add_argument('--img_src', type=str, help='Path to vehicle image data', 
                    default=r"D:\_Innospire\data\nyc3dcars\images")
    parser.add_argument('--anno_src', type=str, help='Path to vehicle annotation data', 
                    default=r"D:\_Innospire\data\nyc3dcars\nyc3dcars-csv\\")
    args = parser.parse_args()
    return args


def upload_dataset(project_name, dataset):
    trainer, _ = functions.authenticate()

    # first check if the project exists
    # if not, make a new one
    projects = trainer.get_projects()
    project = [trainer.get_project(p.id) for p in projects if p.name == project_name]
    if not project:
        print("The project doesn't exist, making a new one now...")
        project = trainer.create_project(project_name)
    else: project = project[0]


    # check if the tag already exists
    # if not, we make a new one
    tags = {}
    curr_tags = {tag.name:tag.id for tag in trainer.get_tags(project.id)}
    for class_name in dataset.classes:
        if class_name not in curr_tags:
            tag = trainer.create_tag(project.id, class_name)
        else:
            tag = trainer.get_tag(project.id, curr_tags[class_name])
        
        tags[class_name] = tag

    errors = []
    #Iterate the rows for each image in the dataframe
    print("Uploading files now...")
    for data in tqdm(dataset):
        img_path = data["path"] 
        assert exists(img_path), f"File does not exist: {img_path}"

        #Create a region object for each bounding box in the dataset 
        regions = []
        for obj in data["bboxes"]:

            regions.append(Region(
                    tag_id=tags[obj["lbl"]].id, 
                    left=obj["left"],
                    top=obj["top"],
                    width=obj["w"],
                    height=obj["h"]
                )
            )


        #Create an object with the image and all of the annotations for that image
        img_filename = split(img_path)[-1]
        with open(img_path, mode="rb") as image_contents:
            image_and_annotations = [ImageFileCreateEntry(name=img_filename, contents=image_contents.read(), regions=regions)] #

        #Upload the image and all annnotations for that image
        batch = ImageFileCreateBatch(images=image_and_annotations)
        try:
            upload_result = trainer.create_images_from_files(
                    project.id, 
                    batch
                )
        except HttpOperationError as e:
            print(e.response.text)
            exit(-1)



        #If upload is not successful, print details about that image for debugging 
        if not upload_result.is_batch_successful:
             for image in upload_result.images:
                err = { "path": img_path,
                        "status": image.status,
                        "img_h": data["h"],
                        "img_w": data["w"],
                        "boxes": data["bboxes"]}
                errors.append(err)

        
    if errors:
        with open(f'log/error.json', 'w') as f:
            json.dump(errors, f, indent=4)
            
        print(f"Broken annotation files: {len(errors)}.")
        print("See log/error.json for more information.")

    #This will take a few minutes 
    print("Upload complete")



if __name__ == "__main__":
    args = parse_args()
    dataset = Vehicles(args.img_src, args.anno_src)
    upload_dataset(args.project_name, dataset)