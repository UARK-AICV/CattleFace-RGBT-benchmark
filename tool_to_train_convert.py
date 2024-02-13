import json
import os
from os import listdir

with open("datasets/keypoints/coco_format/annotations/corrected.json", 'r') as f:
    tool_data = json.load(f)

images = []
annotations = []
categories = [{"supercategory": "cow", "id": 1,"name": "cattle",  "keypoints": ["p1","p2","p3","p4", "p5","p6","p7","p8","p9","p10","p11","p12","p13" ],"skeleton": [ [1,2],
                [1,3],[2,4],[3,5],[4,6],[5,7],[6,8],[7,9],[8,10],[9,11],[10,12],[11,13],[12,13]]}]
id = 0



for dict in tool_data:
    current_image = dict
    area = current_image["box"][2] * current_image["box"][3]
    images.append({"license": None, "file_name": current_image["id"] + ".jpg" ,"coco_url": None, "height": 1440, "width": 2560, "id": id})
    annotations.append({"segmentation": None, "num_keypoints": 13, "area": area, "iscrowd": 0, "keypoints": current_image["points"], "image_id": id, "bbox": current_image["box"], "category_id": 1, "id": id, "inmodal_bbox": None, "inmodal_seg": None})
    id += 1

data = {"images": images, "annotations": annotations, "categories": categories}

with open("datasets/keypoints/coco_format/annotations/train.json", 'w') as f:
    json.dump(data, f, indent = 4)