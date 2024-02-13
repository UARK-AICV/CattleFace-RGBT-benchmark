import json
import os

#Opens raw data json files and creates their respective json objects
with open('data/train_outputs/test/inference/coco_instances_results.json', 'r') as f:
    raw_data = json.load(f)
with open('datasets/keypoints/coco_format/annotations/test_infer.json', 'r') as g:
    id_data = json.load(g)

#Creates empty list to add dictionaries to
convert_data = []
image_name = {}
idList= []
ids = id_data["images"]

for dict in id_data["images"]:
    image_id = {dict["id"]: dict["file_name"].replace(".jpg","")}
    image_name.update(image_id)

for dict in raw_data:
    #Rounds all float elements to integers
    current = dict
    image_id = current['image_id']
    keypoints = current['keypoints']
    if not(image_id in idList):
        idList.append(image_id)
        for i in range(13): 
            keypoints[i*3] = round(keypoints[i*3])
            keypoints[i*3+1] = round(keypoints[i*3+1])  
            keypoints[i*3+2] = 1 
        for i in range(4):
            current['bbox'][i] = round(current['bbox'][i])
        #Adds a dictionary containing the keypoints and box data for each image to the list 'convert data' 
        convert_data.append({'id' : image_name[image_id], 'points': keypoints, 'box' : current['bbox']})

#Sorts the file by the name of the image
convert_data = sorted(convert_data, key=lambda x: x['id'])

#Overwrites raw data with new data
with open('data/train_outputs/test/inference/metadata_csharp.json', 'w') as j:
    json.dump(convert_data, j, indent =4) 


