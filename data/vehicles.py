import os
import csv
import cv2
import functions


class Vehicles:
    ''' Dataset class for the NYC3Dcars dataset.
        http://nyc3d.cs.cornell.edu/
    '''
    
    def __init__(self, img_src, anno_src): 
        ROOT = anno_src
        METADATA = ROOT+"photos.csv"
        ANNOTATION = ROOT+"vehicles.csv"
        IMAGES = img_src


        self.img_paths = functions.get_files(IMAGES)
        self.classes = {"car": 1,
                        "bus": 2,
                        "tram": 3,
                        "bicycle": 4,
                        "motorcycle": 5}
        self.data = {}
        
        with open(ANNOTATION) as f:
            file = csv.reader(f)
            next(file, None) # skip the header
            for row in file:
                img_id = row[1]
                if img_id not in self.data: # if the file hasn't already been initialized
                    self.data[img_id] = {
                        "path": None,
                        "h": None,
                        "w": None,
                        "bboxes": []}


                self.data[img_id]["bboxes"].append(
                    {"x1": float(row[5]),
                    "y1": float(row[6]),
                    "x2": float(row[7]),
                    "y2": float(row[8]),
                    "lbl": "car"})


        with open(METADATA) as f:
            file = csv.reader(f)
            for row in file:
                img_id = row[0]
                path = os.path.normpath(os.path.join(IMAGES, row[1]))
                if path in self.img_paths and img_id in self.data:
                    self.data[img_id]["path"] = path
                    self.data[img_id]["h"] = int(row[12])
                    self.data[img_id]["w"] = int(row[11])
        
        self.keys = list(self.data.keys())

    def __len__(self):
        return len(self.keys)

    def __getitem__(self, idx):
        sample = self.data[self.keys[idx]]
        size = sample["h"], sample["w"]
        for i, bbox in enumerate(sample["bboxes"]):
            top = min(bbox["y1"], bbox["y2"])
            left = min(bbox["x1"], bbox["x2"])
            h = abs(bbox["y1"] - bbox["y2"])
            w = abs(bbox["x1"] - bbox["x2"])
            sample["bboxes"][i] = {"top":top, "left":left, "h":h, "w":w, "lbl":bbox["lbl"]}
        return sample

    def _get_data(self, idx):
        return self.data[self.keys[idx]]
    
    def display(self, idx):
        data = self._get_data(idx)
        img = cv2.imread(data["path"])
        for bbox in data["bboxes"]:
            x1 = int(bbox["x1"]*data["w"])
            y1 = int(bbox["y1"]*data["h"])
            x2 = int(bbox["x2"]*data["w"])
            y2 = int(bbox["y2"]*data["h"])
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    dataset = Vehicles(
                img_src=r"D:\_Innospire\data\nyc3dcars\images\\",
                anno_src=r"D:\_Innospire\data\nyc3dcars\nyc3dcars-csv\\")
    for i in range(5):
        dataset.display(i)
