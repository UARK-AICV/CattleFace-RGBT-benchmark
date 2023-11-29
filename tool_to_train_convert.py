import json
import os
from os import listdir

with open("datasets/keypoints/coco_format/annotations/corrected.json", 'r') as f:
    tool_data = json.load(f)

images = []
annotations = []
id = 0



for dict in tool_data:
    current_image = tool_data[id]
    area = current_image["box"][2] * current_image["box"][3]
    images.append({"license": None, "file_name": current_image["id"] + ".jpg" ,"coco_url": None, "height": 1440, "width": 2560, "id": id})
    annotations.append({"segmentation": None, "num_keypoints": 13, "area": area, "iscrowd": 0, "keypoints": current_image["points"], "image_id": id, "bbox": current_image["box"], "category_id": 1, "id": id, "inmodal_bbox": None, "inmodal_seg": None})
    id += 1

data = {"images": images, "annotations": annotations}

with open("datasets/keypoints/coco_format/annotations/train.json", 'w') as f:
    json.dump(data, f, indent = 4)